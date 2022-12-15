from pprint import pprint
def create_user(conn, cur, user):

    sql = '''INSERT INTO Users (Username,Fullname,Password,IsAdmin) VALUES (?,?,?,?)'''

    cur.execute(sql, user)
    
    conn.commit()

    return cur.lastrowid

def logIn(conn, cur, username, password):
    sql = f'''SELECT Username FROM Users WHERE Username = "{username}" AND Password = "{password}"'''

    cur.execute(sql)
    
    response = cur.fetchone()

    return response

def albumAndArtist(conn, cur):
    sql = f'''SELECT Album.ArtistId, Album.title, Artist.name ,  Track.name
                FROM Album 
                INNER JOIN Artist
                ON Album.ArtistId = Artist.ArtistId
                INNER JOIN Track ON Album.AlbumId=Track.AlbumId;
                '''

    cur.execute(sql)
    
    response = cur.fetchall()
    return response

def artista(conn, cur):
    sql = f'''SELECT Name 
                FROM Artist;
                '''

    cur.execute(sql)
    
    response = cur.fetchall()
    return response

def create_artist(conn, cur, artist):

    sql = '''INSERT INTO Artist (Name) VALUES (?)'''

    cur.execute(sql, (artist,))
    
    conn.commit()

    return cur.lastrowid

def delete_artist(conn, cur, artistdelete):

    sql = '''DELETE FROM Artist WHERE Name = (?)'''

    cur.execute(sql,(artistdelete,))
    
    conn.commit()

    return cur.lastrowid