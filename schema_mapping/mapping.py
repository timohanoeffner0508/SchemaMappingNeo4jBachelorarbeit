
import json
from config import *
from Database_Classes.SqlDatabase import SqlDatabase
global new_db_name
documentation_queries = open(documentation_queries_mapping, 'w')
import csv


def determine_type(values):
    """
    Bestimmt den geeignetsten Datentyp basierend auf einer Liste von Werten.
    Falls Werte unterschiedliche Typen haben, wird der kompatibelste Typ gewählt.
    """

    # Prüfe, ob alle Werte Boolean sind (d.h. nur True/False oder 0/1)
    if all(isinstance(v, bool) or (isinstance(v, int) and v in {0, 1}) for v in values):
        return "BOOLEAN"

    # Falls alle Werte Integer sind, prüfe auf BIGINT oder INT
    if all(isinstance(v, int) for v in values):
        return "BIGINT" if any(abs(v) > 2147483647 for v in values) else "INTEGER"

    # Falls alle Werte Float oder Integer sind, wird FLOAT genutzt
    if all(isinstance(v, (int, float)) for v in values):
        return "DECIMAL(10, 2)"

    # Falls alle Werte Strings sind, nutze string
    if all(isinstance(v, str) for v in values):
        max_length = max(len(v) for v in values)
        return "TEXT" if max_length > 255 else "VARCHAR(255)"

    # Standardfall: TEXT für gemischte Werte
    return "TEXT"


def extract_table_properties(schema):
    """
    Extrahiert die Tabellen-Eigenschaften basierend auf dem JSON-Schema der Graphdatenbank.
    :param schema: Extrahiertes Graphdatenbankschema im JSON-Format
    :return: Dictionary mit den Tabellen und ihren jeweiligen Spalten inklusive Datentypen.
    """

    def select_best_properties(entities):
        """
        Wählt die Entität mit den meisten Attributen aus.
        Falls mehrere Entitäten gleich viele Attribute haben, werden alle Attribute gesammelt und auf ein
         gemeinsames Set geprüft.
        Falls ein Attribut in einer Entität fehlt, wird es ergänzt.
        """
        all_properties = {}

        for entity in entities:
            properties = entity.get("properties", {})
            for prop_name, prop_value in properties.items():
                if prop_name not in all_properties:
                    all_properties[prop_name] = []
                all_properties[prop_name].append(prop_value)


        best_entity = {"properties": {}}
        for prop_name, values in all_properties.items():
            best_entity["properties"][prop_name] = determine_type(values)

        return best_entity

    table_properties = {}
    table_data = {}

    for table_name, table_details in schema.items():

        properties_set = set()


        if table_name == "Supertypes":
            for supertype_entry in table_details:
                supertype_name = supertype_entry.get("Supertype")
                if not supertype_name:
                    continue

                if "data" in supertype_entry and supertype_entry["data"]:
                    best_entity = select_best_properties(supertype_entry["data"])
                    if best_entity and "properties" in best_entity:
                        properties_set = {(prop, best_entity["properties"][prop]) for prop in best_entity["properties"]}

                # **Hier sicherstellen, dass `id` immer enthalten ist**
                if properties_set and "id" not in {prop[0] for prop in properties_set}:
                    properties_set.add(("id", "integer"))


                if properties_set:
                    table_properties[supertype_name] = list(properties_set)

                if "data" in supertype_entry and supertype_entry["data"]:
                    if supertype_name not in table_data:
                        table_data[supertype_name] = []
                    table_data[supertype_name].extend(supertype_entry["data"])
            continue  # Nicht als eigene Tabelle speichern

        # **Verarbeitung für normale Labels**
        if isinstance(table_details, list) and table_details:
            all_have_belongs_to = all("belongs_to" in entry for entry in table_details)

            if all_have_belongs_to:
                # Dann: Eigenschaften vom zugehörigen Supertype verwenden
                belongs_to_targets = {
                    target for entry in table_details for target in entry.get("belongs_to", [])
                }

                if len(belongs_to_targets) == 1:
                    # Exakt ein Supertype: okay
                    supertype_name = list(belongs_to_targets)[0]

                    # Supertypedaten finden und übernehmen
                    supertype_data = schema.get("Supertypes", [])
                    matching_supertypes = [
                        st for st in supertype_data if st.get("Supertype") == supertype_name
                    ]
                    if matching_supertypes:
                        supertype_entry = matching_supertypes[0]
                        supertype_entities = supertype_entry.get("data", [])
                        best_entity = select_best_properties(supertype_entities)

                        # Typen extrahieren
                        if best_entity and "properties" in best_entity:
                            properties_set = {
                                (prop, best_entity["properties"][prop])
                                for prop in best_entity["properties"]
                            }

                            # Werte aus Supertype übernehmen
                            supertype_lookup = {e["id"]: e for e in supertype_entities}
                            for entry in table_details:
                                properties = entry.setdefault("properties", {})
                                super_entity = supertype_lookup.get(entry["id"])
                                if super_entity:
                                    for prop in best_entity["properties"]:
                                        if prop not in properties:
                                            value = super_entity.get("properties", {}).get(prop)
                                            properties[prop] = value

                        # id sicherstellen
                        if properties_set and "id" not in {prop[0] for prop in properties_set}:
                            properties_set.add(("id", "integer"))

                        table_properties[table_name] = list(properties_set)
                        table_data[table_name] = table_details
                    else:
                        print(f"Warnung: Kein passender Supertype für {table_name} gefunden.")
                else:
                    print(f"Warnung: Mehrere Supertypen gefunden in belongs_to für {table_name}")
                continue  # kein eigener Property-Scan nötig

            # Fall: mindestens ein Eintrag hat KEIN belongs_to
            best_entity = select_best_properties(table_details)
            properties_set = set()
            if best_entity and "properties" in best_entity:
                properties_set = {
                    (prop, best_entity["properties"][prop])
                    for prop in best_entity["properties"]
                }

            if properties_set and "id" not in {prop[0] for prop in properties_set}:
                properties_set.add(("id", "integer"))

            table_properties[table_name] = list(properties_set)
            table_data[table_name] = table_details



    return table_properties, table_data
def creating_tables(cursor, table_properties):
    """
    Erstellt Tabellen dynamisch basierend auf den extrahierten Tabellen-Eigenschaften.

    :param cursor: Datenbank-Cursor für die Ausführung der SQL-Befehle.
    :param table_properties: Dictionary mit Tabellen und ihren Eigenschaften.
    """
    global documentation_queries

    documentation_queries.write("--Erstellen von Tabellen und ihren Eigenschaften:")
    for table_name, properties in table_properties.items():
        columns = []
        primary_keys = []

        for prop_name, prop_type in properties:
            sql_type = prop_type

            if prop_name.startswith("id"):
                primary_keys.append(prop_name)

            columns.append(f"{prop_name} {sql_type}")

        if primary_keys:
            columns.append(f"PRIMARY KEY ({', '.join(primary_keys)})")


        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join(columns)}
        );
        """
        cursor.execute(create_table_sql)

        documentation_queries.write(f"\n\t--Table {table_name} :")
        documentation_queries.write(create_table_sql)


def insert_data(cursor, table_data, table_properties):
    """
    Befüllt die Tabellen mit den Daten aus der vorbereiteten Struktur table_data.
    :param cursor: Datenbank-Cursor für die Ausführung der SQL-Befehle.
    :param table_data: Dictionary mit Tabellen und den zugehörigen Entitäten/Daten.
    :param table_properties: Dictionary mit Tabellen und ihren Spalten sowie Datentypen.
    """
    global documentation_queries
    documentation_queries.write("--Befüllen der Tabellen mit den Daten aus table_data:")

    for table_name, entities in table_data.items():
        for entity in entities:
            columns = []
            values = []

            if "id" in entity:
                columns.append("id")
                values.append(entity["id"])

            for prop_name, prop_value in entity.get("properties", {}).items():

                column_type = next((t for col, t in table_properties.get(table_name, []) if col == prop_name), None)

               # BOOLEAN normalisieren, falls aus Neo4j als 0/1 geliefert
                if column_type == "BOOLEAN" and isinstance(prop_value, int) and prop_value in (0, 1):
                    prop_value = bool(prop_value)

                columns.append(prop_name)
                values.append(prop_value)


            if any(prop_name.startswith("id") and prop_value is None for prop_name, prop_value in zip(columns, values)):
                print(f"Fehlender Wert für Primärschlüssel in Tabelle {table_name}, überspringe Einfügen: {entity}")
                continue

            placeholders = ", ".join(["%s"] * len(values))
            insert_sql = f"""
            INSERT INTO {table_name} ({', '.join(columns)})
            VALUES ({placeholders});
            """

            readable_sql = insert_sql % tuple(repr(v) for v in values)
            try:
                cursor.execute(insert_sql, values)
                documentation_queries.write(f"\n\t--Table {table_name}: {readable_sql}")

            except Exception as e:
                print(f"Fehler beim Einfügen in Tabelle {table_name}: {e}")


def extract_all_relationships(table_data):
    relationships = []
    seen = set()

    # Indexierung für schnellen Zugriff auf Supertype-Entitäten nach ID
    supertype_index = {
        label: {entity["id"]: entity for entity in entities}
        for label, entities in table_data.items()
    }

    for label, entities in table_data.items():
        for entity in entities:
            source_id = entity.get("id")
            belongs_to = entity.get("belongs_to", [])
            if not isinstance(belongs_to, list):
                belongs_to = [belongs_to]

            # Beziehungen des aktuellen Labels
            for edge in entity.get("edges", []):
                rel_type = edge.get("type")
                target_id = edge.get("target_node")
                target_labels = edge.get("target_label", [])
                if not isinstance(target_labels, list):
                    target_labels = [target_labels]
                properties = edge.get("properties", {})

                for target_label in target_labels:
                    key = (label, rel_type, source_id, target_id, target_label)
                    if key not in seen:
                        table = f"{rel_type}_{label}_to_{target_label}"
                        relationships.append({
                            "label": label,
                            "start_id": source_id,
                            "end_id": target_id,
                            "type": rel_type,
                            "target_label": target_label,
                            "properties": properties,
                            "table": table
                        })
                        seen.add(key)

            # Beziehungen aus Supertype holen (sofern vorhanden)
            for supertype in belongs_to:
                sup_entity = supertype_index.get(supertype, {}).get(source_id)
                if not sup_entity:
                    continue

                for edge in sup_entity.get("edges", []):
                    rel_type = edge.get("type")
                    target_id = edge.get("target_node")
                    target_labels = edge.get("target_label", [])
                    if not isinstance(target_labels, list):
                        target_labels = [target_labels]
                    properties = edge.get("properties", {})

                    for target_label in target_labels:
                        for start_label in [label, supertype]:
                            key = (start_label, rel_type, source_id, target_id, target_label)
                            if key not in seen:
                                table = f"{rel_type}_{start_label}_to_{target_label}"
                                relationships.append({
                                    "label": start_label,
                                    "start_id": source_id,
                                    "end_id": target_id,
                                    "type": rel_type,
                                    "target_label": target_label,
                                    "properties": properties,
                                    "table": table
                                })
                                seen.add(key)

    return relationships


def create_relationship_tables(cursor, relationships):
    """
    Erstellt Beziehungstabellen basierend auf den Beziehungen und den generierten Metadaten.

    :param cursor: Datenbank-Cursor für die Ausführung der SQL-Befehle.
    :param relationships: Liste der Beziehungen mit 'start_id', 'end_id', 'type', und 'properties'.
    :param table_metadata: Liste von Dictionaries mit Relationship-Typ, Start-Label und End-Label.
    :return: Dictionary mit den erstellten Beziehungstabellen.
    """
    global documentation_queries
    documentation_queries.write("--Erstellen von Beziehungstabellen:\n")

    relationship_tables = {}
    processed_tables = set()

    for rela in relationships:
        rel_type = rela["type"]
        start_label = rela["label"]
        end_label = rela["target_label"]
        table_name = rela["table"]

        if table_name in processed_tables:

            continue

        processed_tables.add(table_name)

        # Initialisiere die Tabellenstruktur
        id_column = None
        for relationship in relationships:
            if (
                relationship["type"] == rel_type
                and relationship["label"] == start_label
                and relationship["target_label"] == end_label
            ):
                properties = relationship.get("properties", {})
                for prop_name in properties:
                    if prop_name.startswith("id_"):
                        id_column = prop_name
                        break

        if not id_column:
            print(f"Warnung: Keine ID-Spalte für {table_name} gefunden. Überspringe Erstellung.")
            continue

        relationship_tables[table_name] = {
            id_column: "BIGINT",
            "start_id": "INT",
            "end_id": "INT"
        }

        # Zusätzliche Eigenschaften aus den Relationships ableiten
        for relationship in relationships:
            if (
                    relationship["type"] == rel_type
                    and relationship["label"] == start_label
                    and end_label in relationship["target_label"]
            ):

                properties = relationship.get("properties", {})
                for prop_name, prop_value in properties.items():
                    if prop_name.startswith("id_"):
                        continue
                    if isinstance(prop_value, bool):
                        prop_type = "BOOLEAN"
                    elif isinstance(prop_value, int):
                        prop_type = "INT"
                    elif isinstance(prop_value, float):
                        prop_type = "DECIMAL(10, 2)"
                    elif isinstance(prop_value, str):
                        if len(prop_value) > 255:
                            prop_type = "TEXT"
                        else:
                            prop_type = "TEXT"
                    else:
                        prop_type = "TEXT"

                    relationship_tables[table_name][prop_name] = prop_type

        # SQL für Tabellen erstellen
        columns_sql = ", ".join([f"{col_name} {col_type}" for col_name, col_type in relationship_tables[table_name].items()])
        foreign_keys = f"""
            FOREIGN KEY (start_id) REFERENCES {start_label} (id) ON DELETE CASCADE,
            FOREIGN KEY (end_id) REFERENCES {end_label} (id) ON DELETE CASCADE
        """
        sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns_sql},
            {foreign_keys},
            PRIMARY KEY ({id_column})
        );
        """

        try:
            cursor.execute(sql)
            documentation_queries.write(f"\n\t--Relationship-Tabelle {table_name}:\n{sql}\n")

        except Exception as e:
            print(f"Fehler beim Erstellen der Tabelle {table_name}: {e}")
            documentation_queries.write(f"\n\t--Fehler beim Erstellen von {table_name}: {str(e)}\n")


    return relationship_tables

def insert_relationship_data(cursor, relationships):
    """
    Fügt Beziehungen aus dem JSON-Schema in die entsprechenden Relationship-Tabellen ein.

    :param cursor: Datenbank-Cursor für die SQL-Befehle.
    :param relationships: Liste der Relationships mit zugehörigen Tabellen-Namen.
    """
    global documentation_queries

    for relationship in relationships:
        table_name = relationship.get("table")
        if not table_name:
            print(f"Warnung: Keine Tabelle für die Beziehung gefunden: {relationship}")
            continue

        # Holen Sie sich die Spalteninformationen aus der Relationship
        properties = relationship.get("properties", {})
        start_id = relationship["start_id"]
        end_id = relationship["end_id"]

        # Werte für die Spalten sammeln
        columns = ["start_id", "end_id"] + list(properties.keys())
        values = [start_id, end_id] + list(properties.values())

        # Überprüfen, ob alle erforderlichen Werte vorhanden sind
        if None in values[:2]:
            print(f"Warnung: Unvollständige Daten für Beziehung {table_name}. Überspringe.")
            continue

        # SQL-INSERT-Befehl dynamisch generieren
        placeholders = ", ".join(["%s"] * len(values))

        insert_sql = f"""
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES ({placeholders});
        """

        readable_sql = insert_sql % tuple(repr(v) for v in values)
        try:
            cursor.execute(insert_sql, values)
            documentation_queries.write(f"\n\t--Table {table_name}: {readable_sql}")
            #print(f"Daten in Tabelle {table_name} eingefügt: {dict(zip(columns, values))}")
        except Exception as e:
            print(f"Fehler beim Einfügen in Tabelle {table_name}: {e}")
            documentation_queries.write(f"FEHLER  {e}")




def main():
    with open(grouped_nodes_json, "r", encoding="utf-8") as json_file:
        schema = json.load(json_file)
    db = SqlDatabase(user, password, new_db_name)
    db.create_database()
    conn, cursor = db.db_connection()
    table_properties, table_data = extract_table_properties(schema)
    creating_tables(cursor, table_properties)
    relationships = extract_all_relationships(table_data)
    insert_data(cursor, table_data, table_properties)
    create_relationship_tables(cursor, relationships)
    insert_relationship_data(cursor, relationships)
    if conn and cursor:
        conn.commit()


def benchmarking():
    import time
    times = []
    for i in range(50):
        start = time.time()
        main()
        duration = time.time() - start
        times.append(duration)
        print(f"Durchlauf {i+1}: {duration:.4f} Sekunden")

    with open("../Evaluation/Benchmark/Movie/benchmark_zeiten_mapping_movie.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Durchgang", "Zeit_in_Sekunden"])
        for i, t in enumerate(times, start=1):
            writer.writerow([i, t])

if __name__ == "__main__":
   main()
   #benchmarking()

