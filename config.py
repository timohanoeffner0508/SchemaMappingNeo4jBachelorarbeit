import os
#Anmeldedaten für Relationale Datenbank
user = "postgres"
password = "0508"
db_name = "testing"
new_db_name = "mapped_db"
# Anmeldedaten für Graphdatenbankverbindung
URL = "bolt://localhost:7690"
USER = "neo4j"
PASSWORD = "2296209Timo"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Json-Files zur Verarbeitung der Graphdatenbankdaten
unstructured_jsonfile = os.path.join(BASE_DIR, "jsonfiles", "graph_data.json")
grouped_nodes_json = os.path.join(BASE_DIR, "jsonfiles", "grouped_nodes.json")
back_extracted_jsonfile = os.path.join(BASE_DIR, "jsonfiles", "back_extracted.json")

#Dokumentations-Files
documentation_queries_mapping = "../Database/Queries_from_mapping.sql"
back_extraction_cypher_file = "Back_extraction/imported_data.cypher"