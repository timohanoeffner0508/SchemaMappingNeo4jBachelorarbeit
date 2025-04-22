# Hier werden alle Queries gespeichert die für die Evaluation benötigt werden:

# Multilabels (Aggregation)
sql_detect_multilabel ="""
SELECT id, string_agg(s_t, ',') AS tables
FROM (
    SELECT id, 'City' AS s_t FROM City
    UNION ALL
    SELECT id, 'State' AS s_t FROM State
    UNION ALL
    SELECT id, 'Country' AS s_t FROM Country
    UNION ALL
    SELECT id, 'EconomicHub' AS s_t FROM EconomicHub
) AS all_labels
GROUP BY id
HAVING COUNT(*) > 1;
"""

cypher_detect_multilabel = """
MATCH (n)
WITH n.id AS Id, labels(n) AS allLabels
WHERE size(allLabels) > 1
RETURN nodeId, allLabels"""
# Verbund
sql_verbund_capital_true = """
SELECT DISTINCT s.*
FROM State s
JOIN has_State_to_City h ON s.id = h.start_id
WHERE h.capital = TRUE;
"""

cypher_verbund_capital_true = """
MATCH (s:State)-[h:has]->(c:City)
WHERE h.capital = true
RETURN DISTINCT s;
"""


sql_detect_more_city_temp = """
SELECT s.name AS state_name,
c1.name AS capital_city,
c2.name AS warm_city
FROM State s
JOIN has_State_to_City h1 ON s.id = h1.start_id
JOIN City c1 ON h1.end_id = c1.id AND h1.capital = TRUE
JOIN has_State_to_City h2 ON s.id = h2.start_id
JOIN City c2 ON h2.end_id = c2.id
JOIN data_City_to_City d ON d.start_id = c2.id AND d.month = 'January'
WHERE d.temp > 2.0 AND c1.id != c2.id;
"""

cypher_detect_more_city_temp = """
MATCH (s:State)-[r1:has]->(c1:City)
WHERE r1.capital = true
MATCH (s)-[r2:has]->(c2:City)
WHERE c1.id <> c2.id
MATCH (c2)-[d:data]->(c2)
WHERE d.month = 'January' AND d.temp > 2.0
RETURN  s.name AS state_name, c1.name AS capital_city, c2.name AS warm_city
"""

