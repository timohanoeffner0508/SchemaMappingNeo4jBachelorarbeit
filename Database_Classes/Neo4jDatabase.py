from neo4j import GraphDatabase
import json
from config import back_extraction_cypher_file

# Klasse zur Verwaltung der Verbindung und Abfragen von Neo4j
# https://neo4j.com/docs/getting-started/languages-guides/neo4j-python/
class Neo4jDatabase:
    def __init__(self, uri, user, password, database = "neo4j"):
        """
        Initialisiert die Verbindung zur Neo4j-Datenbank
        :param uri: URI der Neo4j-Datenbank
        :param user: Benutzername für die Authentifizierung
        :param password: Passwort für die Authentifizierung
        :param database: Name der zu verwendenden Datenbank (Standard: "neo4j")
        """
        self.uri = uri
        self.user = user
        self.password = password
        self.database = database
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """
        Schließt die Verbindung zur Neo4j-Datenbank
        :return:
        """
        self.driver.close()

    def run_query(self, query, parameters=None):
        """
        Führt eine Cypher-Abfrage in der Neo4j-Datenbank aus
        :param query: Cypher-Query als Zeichenkette
        :param parameters: Optionales Dictionary mit Parametern für die Abfrage
        :return: List der zurückgegebenen Datensätze
        """
        with self.driver.session(database=self.database) as session:
            return list(session.run(query,parameters))

    def import_json_to_neo4j(self, json_file, cypher_file=back_extraction_cypher_file):
        """
        Importiert Daten aus einer JSON-Datei in Neo4j und speichert die generierten Cypher-Queries in einer Datei.
        :param json_file: Pfad zur JSON-Datei
        :param cypher_file: Name der Datei, in die die Queries gespeichert wird
        """

        # JSON-Datei öffnen und Daten laden
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Liste zur Speicherung aller generierten Queries
        queries = []

        with (self.driver.session(database=self.database) as session):

            sorted_nodes = []
            # Extrahieren aller Knoten
            for labels, nodes in data.items():
                sorted_nodes.extend([(labels, node) for node in nodes])
            # Knoten nach ID aufsteigend sortieren
            sorted_nodes.sort(key=lambda x: x[1]["id"])

            # Verarbeitung der Knoten
            for labels, node in sorted_nodes:
                label_list = [label.capitalize() for label in labels.split(",")] if labels and labels != "Unlabeled" else []
                node_id = node["id"]
                properties = node.get("properties", {})
                if labels == "unlabeled" or not label_list:
                    merge_part = "MERGE (n{id: $id})"
                else:
                    merge_part = f"MERGE (n:{':'.join(label_list)} {{id: $id}})"
                # Cypher-Query für Knoten mit oder ohne Properties
                if properties:
                    properties_str = ", ".join(f"n.{key} = ${key}" for key in properties.keys())
                    print(properties_str)

                    query = f"""
                    {merge_part}
                    SET {properties_str}
                    """
                    params = {"id": node_id, **properties}

                else:
                    query = f"""
                    {merge_part}
                    """
                    params = {"id": node_id}

                full_query = query.replace("$id", str(node["id"]))
                for key, value in properties.items():
                    full_query = full_query.replace(f"${key}", f"'{value}'" if isinstance(value, str) else str(value))
                queries.append(full_query)

                # Query in Neo4j ausführen
                session.run(query, params)

            sorted_relationships = []
            # Extrahieren aller Beziehungen aus der JSON-Datei
            for label, nodes in data.items():
                start_labels = [label.capitalize() for label in label.split(",")]
                for node in nodes:
                    if "edges" in node:
                        for edge in node["edges"]:
                            sorted_relationships.append((start_labels, node["id"], edge))


            sorted_relationships.sort(key=lambda x: x[1])

            # Verarbeitung der Beziehungen
            for start_labels, start_id, edge in sorted_relationships:

                target_label = ':'.join(label.capitalize() for label in edge["target_label"]) if isinstance(edge["target_label"],
                                                                            list) else edge["target_label"].capitalize()

                properties = edge.get("properties", {})
                properties_str = ", ".join(
                    f"r.{key} = '{value}'" if isinstance(value, str) else f"r.{key} = {value}"
                    for key, value in properties.items()
                )

                properties_cypher = f"SET {properties_str}" if properties else ""

                # Cypher-Query für das Erstellen oder Aktualisieren einer Beziehung
                query = f"""
                MATCH (a:{':'.join(start_labels)} {{id: $start_id}})
                MATCH (b:{target_label} {{id: $end_id}})
                MERGE (a)-[r:{edge['type']}]->(b)
                {properties_cypher}
                """
                params = {
                    "start_id": start_id,
                    "end_id": edge["target_node"],
                    "properties": edge.get("properties", {})
                }


                full_query = query.replace("$start_id", str(start_id)).replace("$end_id", str(edge["target_node"]))
                queries.append(full_query)  # Query zur Liste hinzufügen

                # Query ausführen und speichern
                print("Beziehung:", query, params)

                session.run(query, params)

            # Speichert alle generierten Queries in einer `.cypher` Datei
            with open(cypher_file, "w", encoding="utf-8") as f:
                f.write("\n".join(queries))