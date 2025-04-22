# Imports die für den Export benötigt werden
from Database_Classes.Neo4jDatabase import *
from config import *
import csv


# Funktion, um alle Daten aus der Graphdatenbank zu extrahieren
def export_graph_data():
    # Instanz der Neo4j-Datenbank
    db = Neo4jDatabase(URL, USER, PASSWORD, database="neo4j")

    try:
        # Cypher-Abfrage, um alle Knoten und Beziehungen zu extrahieren
        match_query = """
            MATCH (n)
            OPTIONAL MATCH (n)-[r]->(m) 
            RETURN n, r, m 
            """
        # Führt die Abfrage aus
        result = db.run_query(match_query)


        # Initialisiert das Datenformat, für die JSON-Ausgabe
        graph_data = {"nodes": [], "relationships": []}
        nodes = {}  # Dictionary, um Duplikate zu vermeiden
        relationships = []  # Liste für Relationships

        # Start-Node n; Verarbeitung der Anfrageergebnisse
        for record in result:
            node_n = record["n"]
            if node_n.id not in nodes:
                nodes[node_n.id] = {
                    "id": node_n.id,
                    "labels": list(node_n.labels),
                    "properties": make_json_serializable(node_n._properties),
                }
            # End-Node m
            node_m = record["m"]
            if node_m is not None:
                if node_m.id not in nodes:
                    nodes[node_m.id] = {
                        "id": node_m.id,
                        "labels": list(node_m.labels),
                        "properties": make_json_serializable(node_m._properties),
                    }

            # Relationship between n&m
            if node_m is not None:
                relationship = record["r"]
                relationships.append({
                    "id": relationship.id,
                    "type": relationship.type,
                    "start_node": relationship.start_node.id,
                    "end_node": relationship.end_node.id,
                    "target_label": list(node_m.labels),
                    "properties": make_json_serializable(relationship._properties),
                })

        graph_data["nodes"] = list(nodes.values())
        graph_data["relationships"] = relationships

        #Speichern der Schemas in einer Json-Datei
        with open(unstructured_jsonfile, "w", encoding="utf-8") as json_file:
            json.dump(graph_data, json_file, indent=4, ensure_ascii=False)
        print("JSON-File Done")


    finally:
        db.close()

# Überprüft Datentypen, damit alle im JSON-Format richtig angezeigt werden
def make_json_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(elem) for elem in obj]
    elif hasattr(obj, "isoformat"):
        return obj.isoformat()
    else:
        return obj

def benchmarking():
    import time
    times = []
    for i in range(50):
        start = time.time()
        export_graph_data()
        duration = time.time() - start
        times.append(duration)
        print(f"Durchlauf {i+1}: {duration:.4f} Sekunden")

    with open("../Evaluation/Benchmark/Fraud/benchmark_zeiten_main_fraud.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Durchgang", "Zeit_in_Sekunden"])
        for i, t in enumerate(times, start=1):
            writer.writerow([i, t])



if __name__ == "__main__":
   #benchmarking()
   export_graph_data()