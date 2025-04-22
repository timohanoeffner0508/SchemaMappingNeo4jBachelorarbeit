from decimal import Decimal
import csv
from timeit import repeat
import psycopg2
from Database_Classes.Neo4jDatabase import *
from config import *




def extract_db_schema(user, password, db_name, host="localhost", port=5432):
    """
    Extrahiert die Datenbankstruktur aus einer relationalen Datenbank.
    :param user: Username für den Zugang zur Datenbank
    :param password: Passwort für den Zugang zur Datenbank
    :param db_name: Name der Datenbank
    :param host: Aufrufen der Datenbank
    :param port: Port der Datenbank
    :return: graph_data Datenbankstruktur
    """
    try:
        conn = psycopg2.connect(
            user=user,
            password=password,
            dbname=db_name,
            host=host,
            port=port
        )
        cursor = conn.cursor()


        cursor.execute("""
            SELECT table_name
            FROM information_schema.table_constraints
            WHERE constraint_type = 'FOREIGN KEY'
            GROUP BY table_name
            HAVING COUNT(*) = 2;
        """)
        relation_tables = {table[0] for table in cursor.fetchall()}

        cursor.execute("""
        SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)

        all_tables = {table[0] for table in cursor.fetchall()}

        entity_tables = all_tables - relation_tables



        graph_data = {}


        for original_table in entity_tables:
            cursor.execute(f"SELECT * FROM {original_table}")
            rows = cursor.fetchall()

            column_names = [desc[0] for desc in cursor.description]
            graph_data[original_table] = []

            for row in rows:

                node = {
                    "id": row[column_names.index("id")],
                    "properties": {col: row[i] for i, col in enumerate(column_names) if col != "id"},
                    "edges": []
                }
                graph_data[original_table].append(node)
                print(graph_data[original_table])


        for table in relation_tables:
            parts = table.split("_")
            rel_type = "_".join(parts[:-3])
            start_label = parts[-3]
            end_label =  parts[-1]

            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            for row in rows:
                start_id = row[column_names.index("start_id")]
                end_id = row[column_names.index("end_id")]
                properties = {
                    col: (float(row[i]) if isinstance(row[i], Decimal) else row[i])
                    for i, col in enumerate(column_names)
                    if col not in ["start_id", "end_id"]
                }

                for node in graph_data.get(start_label, []):

                    if node["id"] == start_id:
                        node["edges"].append({
                            "type": rel_type,
                            "target_node": end_id,
                            "target_label": [end_label],
                            "properties": properties
                        })

        print(graph_data)
        return graph_data

    except Exception as e:
        print(f"Fehler beim Extrahieren der Graphstruktur: {e}")
        return None

    finally:
        if conn:
            cursor.close()
            conn.close()


def detect_multilabels(graph_data):
    """
    Erkennt Multilabel-Knoten in den extrahierten Graphdaten.
    Falls mehrere Knoten dieselbe ID haben, werden ihre Labels zusammengeführt.

    :param graph_data: Extrahierte Graphdatenbank als Dictionary
    :return: Aktualisierte Graphdatenbank mit zusammengeführten Multilabel-Knoten
    """
    id_to_labels = {}
    id_to_nodes = {}


    for label, nodes in graph_data.items():
        for node in nodes:
            node_id = node["id"]

            if node_id not in id_to_labels:
                id_to_labels[node_id] = set()
                id_to_nodes[node_id] = node

            id_to_labels[node_id].add(label)


            existing_node = id_to_nodes[node_id]
            existing_node["properties"].update(node["properties"])
            existing_node["edges"].extend(node["edges"])


    merged_graph_data = {}
    for node_id, labels in id_to_labels.items():
        merged_label = ",".join(sorted(labels))
        if merged_label not in merged_graph_data:
            merged_graph_data[merged_label] = []

        merged_graph_data[merged_label].append(id_to_nodes[node_id])

    return merged_graph_data


def clean_relationships(graph_data):
    """
    Überprüft Beziehungen und entfernt doppelte Einträge mit identischem Zielknoten,
    Beziehungstyp und Beziehungs-ID.
    """
    for label in graph_data:
        for node in graph_data[label]:
            seen_edges = set()
            unique_edges = []
            for edge in node["edges"]:
                edge_id = None
                for key in edge["properties"]:
                    if key.startswith("id"):
                        edge_id = edge["properties"][key]
                        break

                edge_key = (edge["target_node"], edge["type"], edge_id)

                if edge_key not in seen_edges:
                    seen_edges.add(edge_key)
                    unique_edges.append(edge)

            node["edges"] = unique_edges


def save_graph_to_json(graph_data, output_file=back_extracted_jsonfile):
    clean_relationships(graph_data)
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(graph_data, json_file, indent=4, ensure_ascii=False)

def benchmarking():
    times = repeat(
        "main()",
        repeat =10,
        number= 1
        )
    print(times)

    with open("../Evaluation/benchmark_zeiten_back_extraction_extended.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Durchgang", "Zeit_in_Sekunden"])
        for i, zeit in enumerate(times, start=1):
            writer.writerow([i, zeit])

def main():
    print("\n##### Extrahiere Graphstruktur aus der relationalen Datenbank #####")
    graph_data = extract_db_schema(user, password, new_db_name)

    print("\n##### Speichere Graphdatenbank als JSON #####")
    merged_data = detect_multilabels(graph_data)
    save_graph_to_json(merged_data,back_extracted_jsonfile)
    neo4j_db = Neo4jDatabase(URL,USER,PASSWORD)
    neo4j_db.import_json_to_neo4j(back_extracted_jsonfile)
    neo4j_db.close()

if __name__ == '__main__':
    main()
    #benchmarking()
