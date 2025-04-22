
                    MERGE (n:Country:Economichub {id: 0})
                    SET n.gdp = 4200000000000, n.name = 'Germany'
                    

                    MERGE (n:Country {id: 1})
                    SET n.name = 'USA'
                    

                    MERGE (n:Country {id: 2})
                    SET n.name = 'Austria'
                    

                    MERGE (n:Country {id: 3})
                    SET n.name = 'Swiss'
                    

                    MERGE (n:Country {id: 4})
                    SET n.name = 'Italia'
                    

                    MERGE (n:Country {id: 5})
                    SET n.name = 'France'
                    

                    MERGE (n:Country {id: 6})
                    SET n.name = 'Great Britain'
                    

                    MERGE (n:Country {id: 7})
                    SET n.name = 'Canada'
                    

                    MERGE (n:City {id: 8})
                    SET n.name = 'Munich'
                    

                    MERGE (n:City:Economichub {id: 9})
                    SET n.gdp = 1500000000000, n.name = 'New York City'
                    

                    MERGE (n:City {id: 10})
                    SET n.name = 'Vienna'
                    

                    MERGE (n:City {id: 11})
                    SET n.name = 'Delsberg'
                    

                    MERGE (n:City {id: 12})
                    SET n.name = 'Roma'
                    

                    MERGE (n:City {id: 13})
                    SET n.name = 'Paris'
                    

                    MERGE (n:City {id: 15})
                    SET n.name = 'Landshut'
                    

                    MERGE (n:City {id: 16})
                    SET n.name = 'Regensburg'
                    

                    MERGE (n:City {id: 17})
                    SET n.name = 'Passau'
                    

                    MERGE (n:State {id: 18})
                    SET n.name = 'Bavaria'
                    

                    MERGE (n:State {id: 19})
                    SET n.name = 'New York'
                    

                    MERGE (n:State {id: 20})
                    SET n.name = 'Tyrol'
                    

                    MERGE (n:State {id: 21})
                    SET n.name = 'Jura'
                    

                    MERGE (n:State {id: 22})
                    SET n.name = 'Toskana'
                    

                    MERGE (n:State {id: 23})
                    SET n.name = 'Bretagne'
                    

                    MERGE (n:State {id: 24})
                    SET n.name = 'England'
                    

                    MERGE (n:State {id: 25})
                    SET n.name = 'Sachsen'
                    

                    MERGE (n:State {id: 26})
                    SET n.name = 'Hessen'
                    

                    MERGE (n:City:Economichub {id: 28})
                    SET n.gdp = 260000000, n.name = 'Frankfurt am Main'
                    

                    MERGE (n:City {id: 29})
                    SET n.name = 'London'
                    

                    MERGE (n:Unlabeled {id: 31})
                    SET n.name = 'Test'
                    

                MATCH (a:City {id: 8})
                MATCH (b:City {id: 8})
                MERGE (a)-[r:data]->(b)
                SET r.id_d = 4, r.temp = 2.8, r.month = 'January'
                

                MATCH (a:City {id: 10})
                MATCH (b:City {id: 10})
                MERGE (a)-[r:data]->(b)
                SET r.id_d = 6, r.temp = -0.5, r.month = 'January'
                

                MATCH (a:City {id: 11})
                MATCH (b:City {id: 11})
                MERGE (a)-[r:data]->(b)
                SET r.id_d = 8, r.temp = 0.9, r.month = 'January'
                

                MATCH (a:City {id: 12})
                MATCH (b:City {id: 12})
                MERGE (a)-[r:data]->(b)
                SET r.id_d = 5, r.temp = 7.2, r.month = 'January'
                

                MATCH (a:City {id: 13})
                MATCH (b:City {id: 13})
                MERGE (a)-[r:data]->(b)
                SET r.id_d = 7, r.temp = 5.0, r.month = 'January'
                

                MATCH (a:City {id: 15})
                MATCH (b:City {id: 15})
                MERGE (a)-[r:data]->(b)
                SET r.id_d = 1, r.temp = 5.5, r.month = 'January'
                

                MATCH (a:City {id: 16})
                MATCH (b:City {id: 16})
                MERGE (a)-[r:data]->(b)
                SET r.id_d = 2, r.temp = 4.0, r.month = 'January'
                

                MATCH (a:City {id: 17})
                MATCH (b:City {id: 17})
                MERGE (a)-[r:data]->(b)
                SET r.id_d = 3, r.temp = 1.0, r.month = 'January'
                

                MATCH (a:State {id: 18})
                MATCH (b:Country {id: 0})
                MERGE (a)-[r:is_in]->(b)
                SET r.id_is = 1
                

                MATCH (a:State {id: 18})
                MATCH (b:City {id: 8})
                MERGE (a)-[r:has]->(b)
                SET r.id_h = 1, r.capital = True
                

                MATCH (a:State {id: 18})
                MATCH (b:City {id: 15})
                MERGE (a)-[r:has]->(b)
                SET r.id_h = 9, r.capital = False
                

                MATCH (a:State {id: 18})
                MATCH (b:City {id: 16})
                MERGE (a)-[r:has]->(b)
                SET r.id_h = 10, r.capital = False
                

                MATCH (a:State {id: 18})
                MATCH (b:City {id: 17})
                MERGE (a)-[r:has]->(b)
                SET r.id_h = 11, r.capital = False
                

                MATCH (a:State {id: 19})
                MATCH (b:Country {id: 1})
                MERGE (a)-[r:is_in]->(b)
                SET r.id_is = 2
                

                MATCH (a:State {id: 19})
                MATCH (b:City {id: 9})
                MERGE (a)-[r:has]->(b)
                SET r.id_h = 2, r.capital = True
                

                MATCH (a:State {id: 20})
                MATCH (b:Country {id: 2})
                MERGE (a)-[r:is_in]->(b)
                SET r.id_is = 3
                

                MATCH (a:State {id: 20})
                MATCH (b:City {id: 10})
                MERGE (a)-[r:has]->(b)
                SET r.id_h = 3, r.capital = False
                

                MATCH (a:State {id: 21})
                MATCH (b:Country {id: 3})
                MERGE (a)-[r:is_in]->(b)
                SET r.id_is = 4
                

                MATCH (a:State {id: 21})
                MATCH (b:City {id: 11})
                MERGE (a)-[r:has]->(b)
                SET r.id_h = 4, r.capital = True
                

                MATCH (a:State {id: 22})
                MATCH (b:Country {id: 4})
                MERGE (a)-[r:is_in]->(b)
                SET r.id_is = 5
                

                MATCH (a:State {id: 22})
                MATCH (b:City {id: 12})
                MERGE (a)-[r:has]->(b)
                SET r.id_h = 5, r.capital = False
                

                MATCH (a:State {id: 23})
                MATCH (b:Country {id: 5})
                MERGE (a)-[r:is_in]->(b)
                SET r.id_is = 6
                

                MATCH (a:State {id: 23})
                MATCH (b:City {id: 13})
                MERGE (a)-[r:has]->(b)
                SET r.id_h = 6, r.capital = False
                

                MATCH (a:State {id: 24})
                MATCH (b:Country {id: 6})
                MERGE (a)-[r:is_in]->(b)
                SET r.id_is = 7
                

                MATCH (a:State {id: 24})
                MATCH (b:City {id: 29})
                MERGE (a)-[r:has]->(b)
                SET r.id_h = 7, r.capital = True
                

                MATCH (a:State {id: 25})
                MATCH (b:Country {id: 0})
                MERGE (a)-[r:is_in]->(b)
                SET r.id_is = 8
                

                MATCH (a:State {id: 26})
                MATCH (b:Country {id: 0})
                MERGE (a)-[r:is_in]->(b)
                SET r.id_is = 9
                

                MATCH (a:City:Economichub {id: 28})
                MATCH (b:State {id: 26})
                MERGE (a)-[r:is_in]->(b)
                SET r.id_is = 10
                