from Database_Classes.Neo4jDatabase import *
from Database_Classes.SqlDatabase import *
from config import *
from Queries_for_testing_mapping import *


def compare_database(sql, cypher):
    db = SqlDatabase(user, password, new_db_name)
    conn, cursor = db.db_connection()
    neo4j_db = Neo4jDatabase(URL,USER,PASSWORD)
    graph_result = neo4j_db.run_query(cypher)
    cursor.execute(sql)
    conn.commit()

    sql_result = cursor.fetchall()



    print("Comparing Database")
    print("SQL-Ergebnis")
    for i in sql_result:
        print(i)

    print("Cypher-Ergebnis")
    for record in graph_result:
        print(record)




if __name__ == "__main__":
    print("1")
    compare_database(sql_verbund_capital_true, cypher_verbund_capital_true)
    print("2")
    compare_database(sql_detect_multilabel, cypher_detect_multilabel)
    print("3")
    compare_database(sql_detect_more_city_temp, cypher_detect_more_city_temp)

