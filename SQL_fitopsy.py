import sqlite3 
with sqlite3.connect("DATA_fitopsy.db") as db:
    cursor = db.cursor()

def makeTableSongs(): 
    cursor.execute("CREATE TABLE IF NOT EXISTS songs"
                       "(song_id INTEGER PRIMARY KEY AUTOINCREMENT, song_name TEXT NOT NULL, artist_id INTEGER NOT NULL, Genre TEXT NO NULL, file_location TEXT NOT NULL, Streams INTEGER NOT NULL, FOREIGN KEY(artist_id) REFERENCES artists(artist_id));"  
                    )
    print("Tabel songs is aangemaakt")

def makeTableArtists():
    cursor.execute("CREATE TABLE IF NOT EXISTS artists"
                        "(artist_id INTEGER PRIMARY KEY AUTOINCREMENT, artist_name TEXT NOT NULL);"
                    )
    print("Tabel artists is aangemaakt")

def makeTablePlaylists():
    cursor.execute("CREATE TABLE IF NOT EXISTS playlists"
                        "(playlist_id INTEGER PRIMARY KEY AUTOINCREMENT, playlist_name TEXT NOT NULL);"
                    )
    print("Tabel playlists is aangemaakt")

def makeTableSongOnPlaylist():
    cursor.execute("CREATE TABLE IF NOT EXISTS songs_on_playlists"
                        "(matching_id INTEGER PRIMARY KEY AUTOINCREMENT, song_id INTEGER NOT NULL, playlist_id INTEGER NOT NULL, FOREIGN KEY(song_id) REFERENCES songs(song_id), FOREIGN KEY(playlist_id) REFERENCES playlists(playlist_id));"
                    )
    print("Tabel songs_on_playlists is aangemaakt")

# def makeTableUsers():
#     cursor.execute("CREATE TABLE IF NOT EXISTS users"
#                             "(user_id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT NOT NULL)"
#                     )
#     print("Tabel users is aangemaakt")

#Vul de tabellen met gegevens
def addSong(name, artist, genre, file_location, streams):
    artist_id = getArtistFromTable("artists",artist)

    if artist_id == None: #voegt automatisch artisten toe die niet in de tabel staan
        addArtist(artist)

    artist_id = int(getArtistFromTable("artists", artist)[0])

    cursor.execute("INSERT INTO songs VALUES (NULL, ?, ?, ?, ?, ?) ", (name, artist_id, genre, file_location, streams))
    cursor.execute("COMMIT")
    print("nummer toegevoegd")

def addArtist(artist):
    cursor.execute("INSERT INTO artists VALUES (NULL, ? ) ", (artist, ))
    cursor.execute("COMMIT") 
    print("Artiest toegevoegd")

def addPlaylist(name):
    cursor.execute("INSERT INTO playlists VALUES (NULL, ?) ", (name, ))
    cursor.execute("COMMIT")
    print("Playlist aangemaakt") 

def addSongOnPlaylist(song, playlist):
    song_id = int(getSongFromTable("songs", song)[0])
    playlist_id = int(getPlaylistFromTable("playlists", playlist)[0])
    cursor.execute("INSERT INTO songs_on_playlists VALUES(NULL,?,?)",(song_id, playlist_id))
    cursor.execute("COMMIT")
    print("nummer toegevoegd aan playlist")

# def addUser(name):
#     cursor.execute("INSERT INTO users VALUES (NULL, ?)",(name, ))
#     cursor.execute("COMMIT")
#     print("gebruiker toegevoegd")

# Gegevens in tabel afdrukken
def gegevensUitTabelPrinten(tabelnaam):
    cursor.execute("SELECT * FROM "+ tabelnaam)
    result = cursor.fetchall() #gegevens opslaan onder result
    print("Gegevens in tabel: " + tabelnaam)
    print(result)

# Hele tabel verwijderen uit de database
def verwijderTabel(tabelNaam):
    cursor.execute("DROP TABLE IF EXISTS " + tabelNaam)
    # cursor.execute("COMMIT")
    print("Tabel "+ tabelNaam + " verwijderd")

# Bepaal welke ID (primary key) bij een gegeven hoort
def getArtistFromTable(table, name):
    cursor.execute("SELECT artist_id FROM "+table+" WHERE artist_name = ?;", (name,))
    result = cursor.fetchone() # je wilt maar 1 rij met gegevens
    return( result)

def getSongFromTable(table, name):
    cursor.execute("SELECT song_id FROM "+table+" WHERE song_name = ?;", (name,))
    result = cursor.fetchone() # je wilt maar 1 rij met gegevens
    return( result)

def getPlaylistFromTable(table, name):
    cursor.execute("SELECT playlist_id FROM "+table+" WHERE playlist_name = ?;", (name,))
    result = cursor.fetchone() # je wilt maar 1 rij met gegevens
    return( result)


# Verdwijderd een gegegeven uit een tabel, door eerst ID (primary key) op te zoeken en dan alle gegevens van die primary key te verwijderen
def verwijderUitTabel(tabelnaam, titel):
    id_om_te_verwijderen = getSongFromTable(tabelnaam, titel)[0] # eerst de ID opzoeken dat bij titel hoort
    cursor.execute("DELETE FROM " + tabelnaam + " WHERE song_id = ?", ( str(id_om_te_verwijderen),) )
    print("Nummer met titel " + titel +" verwijderd uit tabel: "+ tabelnaam)

# # #Pas een bepaalde gegeven aan in een tabel
# def pasAanInTabel(tabelnaam, titeloud, titelnieuw):
#     id_om_aantepassen = getBoekIDUitTabel(tabelnaam, titeloud) #eerst ID opzoeken dat bij titel hoort
#     cursor.execute("UPDATE " + tabelnaam + " SET Titel = ' "+ titelnieuw + "' WHERE BoekID = ?", (id_om_aantepassen,) )
#     print("Boektitel aangepast van " +titeloud + " naar: "+ titelnieuw)

# # HOOFDPROGRAMMA
# keuze = ""
# while not keuze == "STOP" :
#     print("1. Maak tabellen aan")
#     print("2. Vul tabbellen")
#     print("3. Toon alle tabellen")
#     print("4. Verwijder alle tabellen")
#     print("5. Nummer verwijderen")
#     print("STOP")
#     print("Geef je keuze: ")
#     keuze = input()
#     if keuze == "1":
#         makeTableSongs()
#         makeTableArtists()
#         makeTablePlaylists()
#         makeTableSongOnPlaylist()

      
#     elif keuze == "2":
#         addSong("guccigang", "lil pump", "hiphop", "aewq.mp3")
#         addSong("runaway", "kanye", "hiphop", "a452afsaq.mp3")
#         addSong("i wonder", "kanye", "hiphop", "aewq.mp3")
#         addSong("watermelonman", "Herbie Hancock", "jazz", "opq.mp3")
#         addPlaylist("vibes")
#         addPlaylist("sporten")
#         addPlaylist("slapen")
#         addSongOnPlaylist("runaway", "vibes")
#         addSongOnPlaylist("i wonder", "sporten")
#         addSongOnPlaylist("guccigang", "slapen")
#         addSongOnPlaylist("watermelonman", "sporten")
      
#     elif keuze == "3":
#         gegevensUitTabelPrinten("songs")
#         gegevensUitTabelPrinten("artists")
#         gegevensUitTabelPrinten("playlists")
#         gegevensUitTabelPrinten("songs_on_playlists")
      
#     elif keuze == "4":
#         verwijderTabel("songs")
#         verwijderTabel("artists")
#         verwijderTabel("playlists")
#         verwijderTabel("songs_on_playlists")
#         verwijderTabel("users")
#     elif keuze == "5":
#         print("welk nummer wil je verwijderen:")
#         name = str(input())
#         verwijderUitTabel("songs", name)

# print("Doei")