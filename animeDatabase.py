import sqlite3

# get connection to a database
def getConnection(dbName):
    try:
        return sqlite3.connect(dbName)
    except Exception as e:
        print(f"Error: {e}")
        raise

# create the desired table
def createTable(connection):
    query = """
    CREATE TABLE IF NOT EXISTS anime (
        title TEXT,
        captionPath TEXT,
        episodePath TEXT,
        numEpisodes INTEGER
    )
    """
    try:
        with connection:
            connection.execute(query)
    except Exception as e:
        print(f"Error: {e}")

# insert an anime into this table
def insertAnime(connection, title:str, capPath:str, epPath: str, numEp:int):
    query = "INSERT INTO anime (title, captionPath, episodePath, numEpisodes) VALUES (?, ?, ?, ?)"
    try:
        with connection:
            connection.execute(query, (title, capPath, epPath, numEp))
            print(f"Anime: {title} was added to the anime database")
    except Exception as e:
        print(f"Error: {e}")

# fetch a desired anime from the table
def fetchAnime(connection, animeName):
    query = "SELECT * FROM anime WHERE TRIM(LOWER(title)) = TRIM(LOWER(?))"
    try:
        with connection:
            row = connection.execute(query, [animeName]).fetchone()
        return row
    except Exception as e:
        print(f"Error: {e}")

# fetching data necessary for the ascii table
def fetchAnime4Tbl(connection) -> list[tuple]:
    query = "SELECT title, numEpisodes FROM anime ORDER BY title DESC"

    try:
        with connection:
            rows = connection.execute(query).fetchall()
        return rows
    except Exception as e:
        print(f"Error: {e}")  

# delete an anime from the table
def deleteAnime(connection, animeName):
    query = "DELETE FROM anime WHERE title = ?"
    try:
        with connection:
            connection.execute(query, [animeName])
        print(f"Anime: {animeName} was deleted from the database")
    except Exception as e:
        print(f"Error: {e}")
