--Erstellen von Tabellen und ihren Eigenschaften:
	--Table Country :
        CREATE TABLE IF NOT EXISTS Country (
            name VARCHAR(255), id integer, PRIMARY KEY (id)
        );
        
	--Table City :
        CREATE TABLE IF NOT EXISTS City (
            name VARCHAR(255), id integer, PRIMARY KEY (id)
        );
        
	--Table State :
        CREATE TABLE IF NOT EXISTS State (
            name VARCHAR(255), id integer, PRIMARY KEY (id)
        );
        
	--Table unlabeled :
        CREATE TABLE IF NOT EXISTS unlabeled (
            name VARCHAR(255), id integer, PRIMARY KEY (id)
        );
        
	--Table Economichub :
        CREATE TABLE IF NOT EXISTS Economichub (
            gdp BIGINT, id integer, PRIMARY KEY (id)
        );
        --Befüllen der Tabellen mit den Daten aus table_data:
	--Table Country: 
            INSERT INTO Country (id, name)
            VALUES (0, 'France');
            
	--Table Country: 
            INSERT INTO Country (id, name)
            VALUES (1, 'Great Britain');
            
	--Table Country: 
            INSERT INTO Country (id, name)
            VALUES (2, 'Canada');
            
	--Table Country: 
            INSERT INTO Country (id, name)
            VALUES (27, 'USA');
            
	--Table Country: 
            INSERT INTO Country (id, name)
            VALUES (30, 'Austria');
            
	--Table Country: 
            INSERT INTO Country (id, name)
            VALUES (32, 'Swiss');
            
	--Table Country: 
            INSERT INTO Country (id, name)
            VALUES (33, 'Italia');
            
	--Table Country: 
            INSERT INTO Country (id, name)
            VALUES (14, 'Germany');
            
	--Table City: 
            INSERT INTO City (id, name)
            VALUES (3, 'Munich');
            
	--Table City: 
            INSERT INTO City (id, name)
            VALUES (5, 'Vienna');
            
	--Table City: 
            INSERT INTO City (id, name)
            VALUES (6, 'Delsberg');
            
	--Table City: 
            INSERT INTO City (id, name)
            VALUES (7, 'Roma');
            
	--Table City: 
            INSERT INTO City (id, name)
            VALUES (8, 'Paris');
            
	--Table City: 
            INSERT INTO City (id, name)
            VALUES (9, 'Landshut');
            
	--Table City: 
            INSERT INTO City (id, name)
            VALUES (10, 'Regensburg');
            
	--Table City: 
            INSERT INTO City (id, name)
            VALUES (11, 'Passau');
            
	--Table City: 
            INSERT INTO City (id, name)
            VALUES (23, 'London');
            
	--Table City: 
            INSERT INTO City (id, name)
            VALUES (4, 'New York City');
            
	--Table City: 
            INSERT INTO City (id, name)
            VALUES (22, 'Frankfurt am Main');
            
	--Table State: 
            INSERT INTO State (id, name)
            VALUES (12, 'Bavaria');
            
	--Table State: 
            INSERT INTO State (id, name)
            VALUES (13, 'New York');
            
	--Table State: 
            INSERT INTO State (id, name)
            VALUES (15, 'Tyrol');
            
	--Table State: 
            INSERT INTO State (id, name)
            VALUES (16, 'Jura');
            
	--Table State: 
            INSERT INTO State (id, name)
            VALUES (17, 'Toskana');
            
	--Table State: 
            INSERT INTO State (id, name)
            VALUES (18, 'Bretagne');
            
	--Table State: 
            INSERT INTO State (id, name)
            VALUES (19, 'England');
            
	--Table State: 
            INSERT INTO State (id, name)
            VALUES (20, 'Sachsen');
            
	--Table State: 
            INSERT INTO State (id, name)
            VALUES (21, 'Hessen');
            
	--Table unlabeled: 
            INSERT INTO unlabeled (id, name)
            VALUES (24, 'Test');
            
	--Table Economichub: 
            INSERT INTO Economichub (id, gdp)
            VALUES (4, 1500000000000);
            
	--Table Economichub: 
            INSERT INTO Economichub (id, gdp)
            VALUES (22, 260000000);
            
	--Table Economichub: 
            INSERT INTO Economichub (id, gdp)
            VALUES (14, 4200000000000);
            --Erstellen von Beziehungstabellen:

	--Relationship-Tabelle data_City_to_City:

        CREATE TABLE IF NOT EXISTS data_City_to_City (
            id_d BIGINT, start_id INT, end_id INT, temp DECIMAL(10, 2), month TEXT,
            
            FOREIGN KEY (start_id) REFERENCES City (id) ON DELETE CASCADE,
            FOREIGN KEY (end_id) REFERENCES City (id) ON DELETE CASCADE
        ,
            PRIMARY KEY (id_d)
        );
        

	--Relationship-Tabelle is_in_City_to_State:

        CREATE TABLE IF NOT EXISTS is_in_City_to_State (
            id_is BIGINT, start_id INT, end_id INT,
            
            FOREIGN KEY (start_id) REFERENCES City (id) ON DELETE CASCADE,
            FOREIGN KEY (end_id) REFERENCES State (id) ON DELETE CASCADE
        ,
            PRIMARY KEY (id_is)
        );
        

	--Relationship-Tabelle is_in_Economichub_to_State:

        CREATE TABLE IF NOT EXISTS is_in_Economichub_to_State (
            id_is BIGINT, start_id INT, end_id INT,
            
            FOREIGN KEY (start_id) REFERENCES Economichub (id) ON DELETE CASCADE,
            FOREIGN KEY (end_id) REFERENCES State (id) ON DELETE CASCADE
        ,
            PRIMARY KEY (id_is)
        );
        

	--Relationship-Tabelle is_in_State_to_Country:

        CREATE TABLE IF NOT EXISTS is_in_State_to_Country (
            id_is BIGINT, start_id INT, end_id INT,
            
            FOREIGN KEY (start_id) REFERENCES State (id) ON DELETE CASCADE,
            FOREIGN KEY (end_id) REFERENCES Country (id) ON DELETE CASCADE
        ,
            PRIMARY KEY (id_is)
        );
        

	--Relationship-Tabelle is_in_State_to_Economichub:

        CREATE TABLE IF NOT EXISTS is_in_State_to_Economichub (
            id_is BIGINT, start_id INT, end_id INT,
            
            FOREIGN KEY (start_id) REFERENCES State (id) ON DELETE CASCADE,
            FOREIGN KEY (end_id) REFERENCES Economichub (id) ON DELETE CASCADE
        ,
            PRIMARY KEY (id_is)
        );
        

	--Relationship-Tabelle has_State_to_City:

        CREATE TABLE IF NOT EXISTS has_State_to_City (
            id_h BIGINT, start_id INT, end_id INT, capital BOOLEAN,
            
            FOREIGN KEY (start_id) REFERENCES State (id) ON DELETE CASCADE,
            FOREIGN KEY (end_id) REFERENCES City (id) ON DELETE CASCADE
        ,
            PRIMARY KEY (id_h)
        );
        

	--Relationship-Tabelle has_State_to_Economichub:

        CREATE TABLE IF NOT EXISTS has_State_to_Economichub (
            id_h BIGINT, start_id INT, end_id INT, capital BOOLEAN,
            
            FOREIGN KEY (start_id) REFERENCES State (id) ON DELETE CASCADE,
            FOREIGN KEY (end_id) REFERENCES Economichub (id) ON DELETE CASCADE
        ,
            PRIMARY KEY (id_h)
        );
        

	--Table data_City_to_City: 
        INSERT INTO data_City_to_City (start_id, end_id, id_d, temp, month)
        VALUES (3, 3, 4, 2.8, 'January');
        
	--Table data_City_to_City: 
        INSERT INTO data_City_to_City (start_id, end_id, id_d, temp, month)
        VALUES (5, 5, 6, -0.5, 'January');
        
	--Table data_City_to_City: 
        INSERT INTO data_City_to_City (start_id, end_id, id_d, temp, month)
        VALUES (6, 6, 8, 0.9, 'January');
        
	--Table data_City_to_City: 
        INSERT INTO data_City_to_City (start_id, end_id, id_d, temp, month)
        VALUES (7, 7, 5, 7.2, 'January');
        
	--Table data_City_to_City: 
        INSERT INTO data_City_to_City (start_id, end_id, id_d, temp, month)
        VALUES (8, 8, 7, 5.0, 'January');
        
	--Table data_City_to_City: 
        INSERT INTO data_City_to_City (start_id, end_id, id_d, temp, month)
        VALUES (9, 9, 1, 5.5, 'January');
        
	--Table data_City_to_City: 
        INSERT INTO data_City_to_City (start_id, end_id, id_d, temp, month)
        VALUES (10, 10, 2, 4.0, 'January');
        
	--Table data_City_to_City: 
        INSERT INTO data_City_to_City (start_id, end_id, id_d, temp, month)
        VALUES (11, 11, 3, 1.0, 'January');
        
	--Table is_in_City_to_State: 
        INSERT INTO is_in_City_to_State (start_id, end_id, id_is)
        VALUES (22, 21, 10);
        
	--Table is_in_Economichub_to_State: 
        INSERT INTO is_in_Economichub_to_State (start_id, end_id, id_is)
        VALUES (22, 21, 10);
        
	--Table is_in_State_to_Country: 
        INSERT INTO is_in_State_to_Country (start_id, end_id, id_is)
        VALUES (12, 14, 1);
        
	--Table is_in_State_to_Economichub: 
        INSERT INTO is_in_State_to_Economichub (start_id, end_id, id_is)
        VALUES (12, 14, 1);
        
	--Table has_State_to_City: 
        INSERT INTO has_State_to_City (start_id, end_id, capital, id_h)
        VALUES (12, 3, True, 1);
        
	--Table has_State_to_City: 
        INSERT INTO has_State_to_City (start_id, end_id, capital, id_h)
        VALUES (12, 9, False, 9);
        
	--Table has_State_to_City: 
        INSERT INTO has_State_to_City (start_id, end_id, capital, id_h)
        VALUES (12, 10, False, 10);
        
	--Table has_State_to_City: 
        INSERT INTO has_State_to_City (start_id, end_id, capital, id_h)
        VALUES (12, 11, False, 11);
        
	--Table is_in_State_to_Country: 
        INSERT INTO is_in_State_to_Country (start_id, end_id, id_is)
        VALUES (13, 27, 2);
        
	--Table has_State_to_Economichub: 
        INSERT INTO has_State_to_Economichub (start_id, end_id, capital, id_h)
        VALUES (13, 4, True, 2);
        
	--Table has_State_to_City: 
        INSERT INTO has_State_to_City (start_id, end_id, capital, id_h)
        VALUES (13, 4, True, 2);
        
	--Table is_in_State_to_Country: 
        INSERT INTO is_in_State_to_Country (start_id, end_id, id_is)
        VALUES (15, 30, 3);
        
	--Table has_State_to_City: 
        INSERT INTO has_State_to_City (start_id, end_id, capital, id_h)
        VALUES (15, 5, False, 3);
        
	--Table is_in_State_to_Country: 
        INSERT INTO is_in_State_to_Country (start_id, end_id, id_is)
        VALUES (16, 32, 4);
        
	--Table has_State_to_City: 
        INSERT INTO has_State_to_City (start_id, end_id, capital, id_h)
        VALUES (16, 6, True, 4);
        
	--Table is_in_State_to_Country: 
        INSERT INTO is_in_State_to_Country (start_id, end_id, id_is)
        VALUES (17, 33, 5);
        
	--Table has_State_to_City: 
        INSERT INTO has_State_to_City (start_id, end_id, capital, id_h)
        VALUES (17, 7, False, 5);
        
	--Table is_in_State_to_Country: 
        INSERT INTO is_in_State_to_Country (start_id, end_id, id_is)
        VALUES (18, 0, 6);
        
	--Table has_State_to_City: 
        INSERT INTO has_State_to_City (start_id, end_id, capital, id_h)
        VALUES (18, 8, False, 6);
        
	--Table is_in_State_to_Country: 
        INSERT INTO is_in_State_to_Country (start_id, end_id, id_is)
        VALUES (19, 1, 7);
        
	--Table has_State_to_City: 
        INSERT INTO has_State_to_City (start_id, end_id, capital, id_h)
        VALUES (19, 23, True, 7);
        
	--Table is_in_State_to_Country: 
        INSERT INTO is_in_State_to_Country (start_id, end_id, id_is)
        VALUES (20, 14, 8);
        
	--Table is_in_State_to_Economichub: 
        INSERT INTO is_in_State_to_Economichub (start_id, end_id, id_is)
        VALUES (20, 14, 8);
        
	--Table is_in_State_to_Country: 
        INSERT INTO is_in_State_to_Country (start_id, end_id, id_is)
        VALUES (21, 14, 9);
        
	--Table is_in_State_to_Economichub: 
        INSERT INTO is_in_State_to_Economichub (start_id, end_id, id_is)
        VALUES (21, 14, 9);
        