import psycopg2


class SqlDatabase:
    """
        Klasse zur Verwaltung von PostgreSQL-Datenbanken.

        :param user: Benutzername für die Datenbankverbindung
        :param password: Passwort des Benutzers
        :param db_name: Name der zu verwendenden oder zu erstellenden Datenbank
        :param host: Hostname des Datenbankservers (Standard: 'localhost')
        :param port: Portnummer des Datenbankservers (Standard: 5432)
        """
    def __init__(self, user, password,db_name, host ='localhost', port=5432):

        self.user = user
        self.password = password
        self.db_name = db_name
        self.host = host
        self.port = port

    # Funktion die eine Verbindung zur Datenbank herstellt.
    def db_connection(self):
        """
        Stellt eine Verbindung zur angegebenen Datenbank her.
        :return: Tuple aus (Verbindung, Cursor) oder (None, None) bei Fehler
         """
        try:
            conn = psycopg2.connect(
                user=self.user,
                password=self.password,
                dbname=self.db_name,
                host=self.host,
                port=self.port
            )
            conn.set_client_encoding('UTF8')
            cursor = conn.cursor()
            print(f"Erfolgreich verbunden mit der Datenbank '{self.db_name}' auf '{self.host}'.")
            return conn, cursor
        except psycopg2.Error as e:
            print(f"Fehler beim Verbinden zur Datenbank '{self.db_name}': {e}")
            return None, None

    #Funktion um eine Datenbank zu erstellen
    def create_database(self):

        try:
            conn = psycopg2.connect(
                user=self.user,
                password=self.password,
                dbname="postgres",
                host=self.host,
                port=self.port
            )
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f"""CREATE DATABASE {self.db_name}""")

            print(f"Die Datenbank '{self.db_name}' wurde erfolgreich erstellt.")
        except psycopg2.Error as e:
            print(f"Fehler beim Erstellen der Datenbank '{self.db_name}': {e}")

        finally:

            if conn:
                cursor.close()
                conn.close()