# README - Bachelorarbeit Timo Hanöffner
## 🔎 Projektbeschreibung
Dieses Projekt einer Bachelorarbeit beinhaltet ein Verfahren zur Transformation von Neo4j-Graphdatenbanken in relationale Datenbanksysteme (PostgreSQL), 
das auf die Integration mit dem Provenance-System ProSA ausgelegt ist. Es ermöglicht die strukturierte Abbildung komplexer Entitäten,
einschließlich Multilabel-Knoten, in relationale Modelle und unterstützt zudem Schema-Evolution und eine Rücktransformation von relationaler Datenbank
nach Neo4j.

---

## 📁 Projektstruktur

```plaintext
.
├── Antrittsvortrag/               # Präsentationsfolien zum Projektstart
│   └── Schema_Evolution_Timo_Hanöffner.pptx
├── Back_extraction/              # Rücktransformation: Relation → Graph (Neo4j)
│   ├── back_extraction_after_evolution.py
│   └── imported_data.cypher
├── Database/                     # Dokumentation und SQL-/Cypher-Abfragen zu den Beispieldatenbanken
│   ├── Documentation_Graphdatabase.cypher
│   ├── DocumentationSQL.sql
│   └── Queries_from_mapping.sql
├── Database_Classes/             # Python-Klassen zur Kommunikation mit Neo4j und PostgreSQL
│   ├── Neo4jDatabase.py
│   └── SqlDatabase.py
├── Evaluation/                   # Benchmarks, Auswertungsskripte, Notebooks
│   ├── Plots/
│   ├── Benchmark/
│   ├── evaluation.py
│   ├── Evolution_main.ipynb
│   └── Queries_for_testing_mapping.py
├── Evolution/                    # Umsetzung der Schema-Evolution
│   ├── ProSA/                    # XML-Definitionen der Evolutionsoperationen
│   │   ├── BA-Timo-Add.xml
│   │   ├── BA-Timo-Copy.xml
│   │   └── BA-Timo-Rename.xml
│   └── schema_evolution.py
├── jsonfiles/                    # JSON-Dateien mit extrahierten/umgewandelten Daten
│   ├── back_extracted.json
│   ├── graph_data.json
│   ├── grouped_nodes.json
│   └── test.json
├── Literatur/                    # Literatur- und Quellenverzeichnis
│   ├── ProSA/
│   ├── Schema Extraction/
│   ├── SchemaEvolution/
│   ├── SchemaMapping/
├── schema_extraktion/           # Extraktion des Schemas aus Neo4j
│   ├── grouping_multilabels.py
│   └── main.py

```
---
## ⚙️  Voraussetzungen

- Python 3.10+
- PostgreSQL
- Neo4j 5.x
- Abhängigkeiten (via `requirements.txt`)
  - `neo4j`
  - `psycopg2`
  - `pandas` (für Performance-Testing)
  - `matplotlib` (für Performance-Testing)

Installation via:

```bash
pip install -r requirements.txt
```

## 💾 Beispieldatenbanken aufsetzen
Zum initialen Setup der Beispiel-Datenbanken stehen zwei Dateien im Verzeichnis `Database/` zur Verfügung:
- `Documentation_Graphdatabase.cypher`: Cypher-Statements für Neo4j
- `DocumentationSQL.sql`: SQL-Anweisungen für PostgreSQL
### Ausführen in Shell
🟦 Neo4j
```bash
cypher-shell -u <USERNAME> -p <PASSWORD> -d <DATABASE_NAME> < Database/Documentation_Grapphdatabase.cypher
```
🐘 PostgreSQL
```bash
psql -U <USERNAME> -d <DATABASE_NAME> -f Database/DocumentationSQL.sql
```
Hinweis: Stellen Sie sicher, dass die Zieldatenbank bereits erstellt wurde und die Zugangsdaten korrekt sind.
Zudem müssen alle Informationen wie USERNAME und DATABASE_NAME in `config.py` gespeichert werden.
___

## 🚀 Verwendung

### 1. Graphdaten-Export
Mithilfe von `schema_extraktion/main.py`werden alle Knoten und Kanten aus der Neo4j Datenbank extrahiert und in `jsonfiles/graph_data.json`
gespeichert.
### 2. Schema-Extraktion
Mit `schema_extraktion/grouping_multilabels.py` wird aus allen Knoten und Kanten ein einheitliches Schema transformiert und in `jsonfiles/grouped_nodes.json`
gespeichert.
### 3. Schema-Mapping
Mit `schema_mapping\mapping.py` wird das extrahierte Schema auf eine relationale Datenbank gemappt. Alle SQL-Befehle werden
`Database/DocumentationsSQL.sql` gespeichert.
### 4. Schema-Evolution
In `Evolution/schema_evolution.py` wurde ein Parser implementiert, der aus Evolutionsoperatoren, die als Cypher-Befehl vorliegen
in SQL-Befehle geparst und beide Befehle auf der jeweiligen Datenbank ausgeführt.
### 5. Rücktransformation
In `Back_extraktion/back_extraction_after_evolution.py` erfolgt die Rücktransformation von einer Relationalen Datenbank in eine
Graphdatenbank. Alle Cypher-Befehle werden in `Back_extraktion/import_data.cypher` gespeichert.

---
## 🧑‍💻 Autor
**Timo Hanöffner**  

Kontakt: timo.hanoeffner@stud.uni-regensburg.de
---

## 🌐 Quellen
Die verwendeten Quellen befinden sich jeweils:
- ProSA: `Literatur/ProSA`
- Schema-Extraktion: `Literatur/SchemaExtraktion`
- Schema-Mapping: `Literatur/SchemaMapping`
- Datenbanken: `Literatur/Database`