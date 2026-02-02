import sqlite3

def getConnection(dbName):
    try:
        return sqlite3.connect(dbName)
    except Exception as e:
        print(f"Error: {e}")
        raise


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

def insertAnime(connection, title:str, capPath:str, epPath: str, numEp:int):
    query = "INSERT INTO anime (title, captionPath, episodePath, numEpisodes) VALUES (?, ?, ?, ?)"
    try:
        with connection:
            connection.execute(query, (title, capPath, epPath, numEp))
            print(f"Anime: {title} was added to the anime database")
    except Exception as e:
        print(f"Error: {e}")

def fetchAnime(connection, animeName):
    query = "SELECT * FROM anime WHERE LOWER(title) = LOWER(?)"
    try:
        with connection:
            row = connection.execute(query, [animeName]).fetchone()
        return row
    except Exception as e:
        print(f"Error: {e}")


def fetchAnime4Tbl(connection) -> list[tuple]:
    query = "SELECT title, numEpisodes FROM anime ORDER BY title DESC"

    try:
        with connection:
            rows = connection.execute(query).fetchall()
        return rows
    except Exception as e:
        print(f"Error: {e}")  

def deleteAnime(connection, animeName):
    query = "DELETE FROM anime WHERE title = ?"
    try:
        with connection:
            connection.execute(query, [animeName])
        print(f"Anime: {animeName} was deleted from the database")
    except Exception as e:
        print(f"Error: {e}")
