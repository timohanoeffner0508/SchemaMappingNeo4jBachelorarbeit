CREATE TABLE cities (
    id_c SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE states (
    id_s SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE countries (
    id_co SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE economichub(
    id_eh SERIAL PRIMARY KEY,
    gdp  BIGINT
)

CREATE TABLE multilabel(
    id_c INT REFERENCES city(id_c),
    id_s INT REFERENCES state(id_s),
    id_co INT REFERENCES country(id_co),
    id_eh INT REFERENCES economichub(id_eh)

)
CREATE TABLE data (
    id_d SERIAL PRIMARY KEY,
    id_c INT REFERENCES cities(id_c),
    month VARCHAR NOT NULL,
    temp DECIMAL NOT NULL
);

CREATE TABLE has (
    id_h SERIAL PRIMARY KEY,
    id_s INT REFERENCES states(id_s),
    id_c INT REFERENCES cities(id_c),
    start INT, 
    capital BOOLEAN
)

CREATE TABLE is_in (
    id_is SERIAL PRIMARY KEY,
    id_s INT REFERENCES states(id_s),
    id_co INT REFERENCES countries(id_co),
    start INT
)

INSERT INTO cities (name) VALUES
('Munich'),
('New York City'),
('Vienna'),
('Delsberg'),
('Roma'),
('Paris'),
('London'),
('London'),
('Landshut'),
('Regensburg'),
('Passau'),

INSERT INTO countries (name) VALUES
    ('Germany'),
    ('USA'),
    ('Austria'),
    ('Swiss'),
    ('Italia'),
    ('France'),
    ('Great Britain');

INSERT INTO states (name) VALUES
    ('Bavaria'),
    ('New York'),
    ('Tyrol'),
    ('Jura'),
    ('Toskana'),
    ('Bretagne'),
    ('England'),
    ('Sachsen');

INSERT INTO has (id_s, id_c,start,capital) VALUES
(1,1,1,true)
(2,2,2, tue),
(3,3,3,false),
(4,4,4,true),
(5,5,5,false),
(6,6,6,false),
(7,7,7,true),
(9,9,9,false),
(10,10,10,false),
(11,11,11,false)

INSERT INTO is_in (id_s,id_co,start) VALUES
(1,1,1),
(2,2,2),
(3,3,3),
(4,4,4),
(5,5,5),
(6,6,6),
(7,7,7),
(8,1,8)

INSERT INTO economichub (id_eh, gdp) VALUES
(1,2600555550000),  --Frankfurt
(2,1500000000000), --New York City
(3,4200000000000), -- Germany




SELECT h.id_h, h.start_id, h.end_id, h.capital,
       COALESCE(c1.name, co1.name, s1.name, eh1.gdp) AS start_name,
       COALESCE(c2.name, co2.name, s2.name, eh2.gdp) AS end_name
FROM has h
LEFT JOIN city c1 ON h.start_id = c1.id
LEFT JOIN country co1 ON h.start_id = co1.id
LEFT JOIN state s1 ON h.start_id = s1.id
LEFT JOIN economichub eh1 ON h.start_id = eh1.id
LEFT JOIN city c2 ON h.end_id = c2.id
LEFT JOIN country co2 ON h.end_id = co2.id
LEFT JOIN state s2 ON h.end_id = s2.id
LEFT JOIN economichub eh2 ON h.end_id = eh2.id;




SELECT *
FROM economichub eh
JOIN city c on eh.id = c.id,



Union

SELECT *
FROM economichub eh
Join country co on eh.id = co.id





SELECT id_h, state.name, city.name, capital
FROM has_state_to_city has
JOIN state ON state.id = has.start_id
JOIN city ON city.id = has.end_id