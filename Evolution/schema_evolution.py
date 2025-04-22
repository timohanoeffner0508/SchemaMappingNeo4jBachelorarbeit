import re
from Database_Classes.SqlDatabase import *
from Database_Classes.Neo4jDatabase import *
from config import *

# Funktion, um aus einer Cypher-Anfrage einen SQL-Befehl zu generieren
def cypher_parser(cypher_query):
    """
    Wandelt eine Cypher-Query in eine entsprechende SQL-Query um,
    indem REMOVE (Löschen von Spalten), ADD (Hinzufügen von Spalten), RETYPE (Ändern des Datentyps) und RENAME (Umbenennen von Spalten) erkannt wird.
    merge (Zusammenführen), copy (Duplizieren), move (Verschieben) or split (Aufteilen).
    :param cypher_query: Die Cypher-Query als String
    :return: Generierte SQL-Query oder eine Fehlermeldung
    """
    cypher_query = cypher_query.strip()

        # Remove (Attribute entfernen)
    remove_part = re.search(r"MATCH\s*\(\s*(\w+):(\w+)\s*\)\s*REMOVE\s+\1\.(\w+)", cypher_query, re.IGNORECASE)

    # Delete (Knoten löschen)
    delete_part = re.search(r"MATCH\s*\(\s*(\w+):(\w+)\s*\)\s*DETACH\s+DELETE\s+\1", cypher_query, re.IGNORECASE)

    # Rename (Umbenennen eines Attributs)
    rename_part = re.search(r"MATCH\s*\(\s*(\w+):(\w+)\s*\)\s*SET\s+\1\.(\w+)\s*=\s*\1\.(\w+)\s*REMOVE\s+\1\.\4", cypher_query,
                            re.IGNORECASE)

    # Add (Neue Spalte hinzufügen)
    add_part = re.search(r"MATCH\s*\(\s*(\w+):(\w+)\s*\{\s*id\s*:\s*(\d+)\s*\}\)\s*SET\s+\1\.(\w+)\s*=\s*(\d+)", cypher_query,
                         re.IGNORECASE)

    # Copy (Knoten duplizieren)
    copy_part = re.search(
        r"MATCH\s*\(\s*(\w+):(\w+)\s*\)\s*CREATE\s*\(\s*(\w+):(\w+)\)",
        cypher_query, re.IGNORECASE)

    if remove_part:
        table_name = remove_part.group(2)
        column_name = remove_part.group(3)
        sql_query = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"


    elif delete_part:
        table_name = delete_part.group(2)
        sql_query = f"DROP TABLE {table_name} CASCADE;"

    elif rename_part:
        table_name = rename_part.group(2)
        new_column_name = rename_part.group(3)
        old_column_name = rename_part.group(4)
        sql_query = f"ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name};"

    elif add_part:

        table_name = add_part.group(2)
        id_value = add_part.group(3)
        column_name = add_part.group(4)
        value = add_part.group(5)
        sql_query = (
        f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} INT;\n"
        f"UPDATE {table_name} SET {column_name} = {value} WHERE id = {id_value};")

    elif copy_part:
        table_name_old = copy_part.group(4)
        table_name_new = copy_part.group(2)
        sql_query = f"COPY TABLE {table_name_old} AS SELECT * FROM {table_name_new};"

    else:
        sql_query = "Ungültige Cypher-Anweisung"

    print(sql_query)
    return sql_query

# Funktion um auf beiden Datenbanken die Evolution durchführen zu können
def execute_queries_for_schema_evolution(cypher_query, sql_query):
    """
    Führt die jeweiligen Graphdatenbank-Query und SQL-Query auf der Graphdatenbank und relationalen Datenbank aus und
    führt somit die Schema-Evolution durhc
    :param cypher_query: Graphdatenbank-Query als String
    :param sql_query: Sql-Query als String
    :return: Print-Statement, ob Schema-Evolution erfolgreich war
    """
    db = SqlDatabase(user,password,new_db_name)
    conn, cursor = db.db_connection()
    neo4j_db = Neo4jDatabase(URL, USER, PASSWORD)
    try:

        neo4j_db.run_query(cypher_query)
        try:
            cursor.execute(sql_query)
            conn.commit()

        except Exception as e:
            print(f"SQL: {e}")

    except Exception as e:
        print(f"Cypher: {e}")

if __name__ == '__main__':

    remove_cypher = "MATCH (c:City) REMOVE c.name"
    remove_sql = cypher_parser(remove_cypher)

    delete_cypher = "MATCH (c:City) DETACH DELETE c"
    delete_sql = cypher_parser(delete_cypher)

    rename_cypher = "MATCH (c:City) SET c.cityName = c.name REMOVE c.name"
    rename_sql = cypher_parser(rename_cypher)

    add_cypher = "MATCH (c:Country {id:0}) SET c.population = 83000000"

    add_sql = cypher_parser(add_cypher)

    copy_cypher = "MATCH (c:City) CREATE (n2:CopyCity) SET c= n2"
    copy_sql = cypher_parser(copy_cypher)


    #execute_queries_for_schema_evolution(remove_cypher,remove_sql)
    #execute_queries_for_schema_evolution(delete_cypher,delete_sql)
    #execute_queries_for_schema_evolution(add_cypher,add_sql)
    #execute_queries_for_schema_evolution(copy_cypher,copy_sql)
    #execute_queries_for_schema_evolution(rename_cypher,rename_sql)
