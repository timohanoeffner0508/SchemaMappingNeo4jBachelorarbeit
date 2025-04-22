import json
from collections import defaultdict
import csv
from config import grouped_nodes_json, unstructured_jsonfile



# Funktion zum Speichern der gruppierten Knoten in einer JSON-Datei (nur zur Kontrolle)
def saving_grouped_nodes(nodes, json_path_output):
    """
    Speichert alle gruppierten Knoten in einer JSON-Datei ab
    :param nodes:
    :param json_path_output:
    :return:
    """
    with open(json_path_output, "w", encoding="utf-8") as json_file:
        json.dump(nodes, json_file, indent=4, ensure_ascii=False)
    print(f"Knoten in '{json_path_output}' gespeichert")

# Funktion zur Gruppierung von Knoten basierend auf ihren Labels
def grouping_nodes_by_label(json_path):

    """
    Gruppiert alle Knoten nach ihren Labels
    :param json_path:
    :return: grouped_nodes
    """
    with open(json_path, "r", encoding="utf-8") as json_file:
        graph_data = json.load(json_file)

    grouped_nodes = defaultdict(list)


    # Indexe erstellen für schnellen Zugriff
    node_index = {node["id"]: node for node in graph_data["nodes"]}
    relationships_by_start = defaultdict(list)
    for r in graph_data["relationships"]:
        relationships_by_start[r["start_node"]].append(r)

    # Gruppierung starten
    for node in graph_data["nodes"]:
        label_set = frozenset(node["labels"]) if node["labels"] else frozenset(["unlabeled"])
        properties = node.get("properties", {}).copy()

        if "id" in properties:
            del properties["id"]

        node_data = {
            "id": node["id"],
            "properties": properties,
            "edges": []
        }

        # Nur durchlaufen, was wirklich zu diesem Knoten gehört
        for relationship in relationships_by_start[node["id"]]:
            props = relationship.get("properties", {}).copy()
            if not any(k.startswith("id_") for k in props):
                props["id_auto"] = relationship.get("id")

            target_node = node_index.get(relationship["end_node"])
            target_label = target_node["labels"] if target_node else []

            node_data["edges"].append({
                "type": relationship["type"],
                "target_node": relationship["end_node"],
                "target_label": target_label,
                "properties": props
            })

        grouped_nodes[label_set].append(node_data)

    grouped_nodes_serializable = {
        ", ".join(sorted(list(label_set))): nodes for label_set, nodes in grouped_nodes.items()
    }
    print(grouped_nodes_serializable)
    return grouped_nodes

# Funktion zur Verarbeitung von Knoten mit mehreren Labels (Multilabels)
def factoring_multilabel(grouped_nodes):
    """
    Verarbeitete alle Multilabels und identifiziert Supertypen
    :param grouped_nodes:
    :return: supertype_data
    """
    from collections import defaultdict

    nodes_multiple_labels = set()
    label_properties = defaultdict(set)
    single_label_properties = {}
    multilabel_properties = {}
    supertype_properties = {}
    supertype_data = {}
    
    # 1. Identifiziere alle Multilabel-Knoten
    for label_set, nodes in grouped_nodes.items():
        if len(label_set) > 1:
            nodes_multiple_labels.add(label_set)


    #  Erstelle Mapping: Label → Set von Label-Kombinationen, in denen es vorkommt
    label_in_combinations = defaultdict(set)
    for label_set in nodes_multiple_labels:
        for label in label_set:
            label_in_combinations[label].add(label_set)

    # Supertype-Kandidaten: Labels, die in mehreren Multilabel-Kombinationen vorkommen
    supertypes_labels = {label for label, combos in label_in_combinations.items() if len(combos) > 1}
    print("Supertype-Kandidaten:", supertypes_labels)

    if not supertypes_labels:
        print("Keine Supertype-Kandidaten gefunden – abbrechen.")
        return

    # Sammle alle Property-Namen pro Label-Set
    for label_set, nodes in grouped_nodes.items():
        for node in nodes:
            label_properties[label_set].update(node["properties"].keys())

    # 5. Splitte in Single-Label und Multilabel
    for label_set, props in label_properties.items():
        if len(label_set) == 1:
            single_label_properties[list(label_set)[0]] = props.copy()
        else:
            multilabel_properties[label_set] = props.copy()

    # Bereinige Multilabel-Eigenschaften mit Single-Label-Eigenschaften
    for label_set, props in multilabel_properties.items():
        print(label_set, props)

        for label in label_set:
            if label in single_label_properties:
                props -= single_label_properties[label]

    # Schnittmengenanalyse: Eigenschaften der Supertypes
    for supertype in supertypes_labels:
        common_props = None
        for label_set, props in multilabel_properties.items():
            if supertype in label_set:
                if common_props is None:
                    common_props = props.copy()
                else:
                    common_props &= props
        if common_props:
            supertype_properties[supertype] = common_props

    print("Ermittelte Supertype-Eigenschaften:")
    for s, p in supertype_properties.items():
        print(f"{s}: {p}")

    # Extrahiere die Daten für die Supertype-Properties
    for supertype, props in supertype_properties.items():
        supertype_data[supertype] = {}
        for prop in props:
            supertype_data[supertype][prop] = []

        for label_set, nodes in grouped_nodes.items():
            if supertype in label_set:
                for node in nodes:
                    for prop in props:
                        if prop in node["properties"]:
                            supertype_data[supertype][prop].append({
                                "id": node["id"],
                                "properties": node["properties"][prop],
                                "edges": node["edges"]
                            })

    print("Supertype-Daten fertig extrahiert.")
    return supertype_data

def parsing_schema(supertype_data, grouped_nodes):
    """
    :param supertype_data: Extrahierte Eigenschaften und Daten der Supertypen
    :param grouped_nodes: Gruppierte Knoten nach Label
    :return: output_json
    """
    output_json = {}
    supertype_json = {"Supertypes": []}
    existing_lookup = {}

    # Nur Supertype-Verarbeitung, wenn Daten vorhanden
    if supertype_data:
        supertype_labels = {s: set(props.keys()) for s, props in supertype_data.items()}
        for supertype, properties in supertype_data.items():
            for prop, entries in properties.items():
                for entry in entries:
                    if entry["id"] in existing_lookup:
                        existing_lookup[entry["id"]]["properties"][prop] = entry["properties"]
                    else:
                        existing_lookup[entry["id"]] = {
                            "id": entry["id"],
                            "properties": {prop: entry["properties"]},
                            "edges": entry["edges"]
                        }
            data_list = list(existing_lookup.values())

            supertype_json["Supertypes"].append({
                "Supertype": supertype,
                "data": data_list
            })
    else:
        supertype_labels = {}

    # Verarbeite normale Labels (Multilabel-Knoten ohne Supertype-Properties)
    for label_set, nodes in grouped_nodes.items():
        for node in nodes:
            labels = set(label_set)
            supertypes_in_node = labels & supertype_labels.keys()

            filtered_properties = node["properties"].copy()
            belongs_to = None

            if supertypes_in_node:
                belongs_to = list(supertypes_in_node)
                for props_st in supertypes_in_node:
                    for prop in supertype_labels[props_st]:
                        filtered_properties.pop(prop, None)
                labels -= supertypes_in_node

            node_obj = {
                "id": node["id"],
                "properties": filtered_properties
            }

            # Nur Knoten ohne belongs_to behalten ihre Kanten
            if not belongs_to:
                node_obj["edges"] = node.get("edges", [])
            else:
                node_obj["belongs_to"] = belongs_to

            for label in labels:
                output_json.setdefault(label, []).append(node_obj)

    # Supertype-Daten hinzufügen (wenn vorhanden)
    output_json.update(supertype_json)

    # Ergebnis speichern
    with open(grouped_nodes_json, "w", encoding="utf-8") as json_file:
        json.dump(output_json, json_file, indent=4, ensure_ascii=False)

    print("Supertypes erfolgreich verarbeitet! JSON gespeichert.")
    return output_json

def benchmarking():
    import time
    times = []
    for i in range(15):
        start = time.time()
        main()
        duration = time.time() - start
        times.append(duration)
        print(f"Durchlauf {i+1}: {duration:.4f} Sekunden")

    with open("../Evaluation/benchmark_zeiten_grouping_wind_small.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Durchgang", "Zeit_in_Sekunden"])
        for i, t in enumerate(times, start=1):
            writer.writerow([i, t])

def main():
    grouped_nodes = grouping_nodes_by_label(unstructured_jsonfile)

    supertype_data =factoring_multilabel(grouped_nodes)
    parsing_schema(supertype_data, grouped_nodes)

if __name__ == "__main__":
    main()
    #benchmarking()
