# Vul hier de naam van je programma in:
#fitopsy
#
# Vul hier jullie namen in:
# Willem Paternotte en Robin KUijpers
#
#
###------------------bibliotheek en globale variabelen--------------

from os import name
from tkinter import *
from tkinter.font import Font
from tkinter import filedialog
from pygame import mixer
from tinytag import TinyTag #VOOR META DATA MP3 BESTANDEN
import tkinter as tk # voor popup scherm check

import SQL_fitopsy

#globale variabele voor het handmatig invoeren

ingevoerde_name = ""
ingevoerde_artist = ""
ingevoerde_genre = ""
ingevoerde_file_path = ""

#globale variabele voor het tonen van nummerGegevens
name = ""
artist = ""
genre = ""
file_path = ""
album = ""
bitrate = 0
year = 0


venster = Tk()



#--------opstarten---------------------#
venster.geometry("600x600") #bepaalt grootte window
mainFont = Font(
    family="Comic Sans MS",
    size= 40,
    )
venster.wm_title("fitopsy" )
venster["bg"] = "white"
venster.iconbitmap("fitopsy.ico")


# tag = TinyTag.get("C:/Users/robin/Sync/leerjaar 5/informatica/SQL/music/Future, Drake - Life Is Good.mp3") 
# tag = TinyTag.get('C:/Users/robin/Sync/leerjaar 5/informatica/SQL/music/Future, Drake - Life Is Good.mp3',) 

###------------------Functie defenities-----------------------------


def zoekNummer():
    gevonden_nummer=SQL_fitopsy.getSongFromTable("songs", ingevoerde_nummer.get())
    print(gevonden_nummer)

def BestandKiezen(): #zorgt ervoor dat windows verkenner opent, zodat filepath niet handmatigf moet worden ingevuld
    global file_path
    file_path = StringVar()
    file_path = filedialog.askopenfilenames(filetypes=(("mp3 files","*.mp3"),("FLAC files","*.flac"),("wav files","*.wav"),("All files","*.*"))) #bepaalt welke bestandtypes gezein kunnen worden
    print(file_path)
    return(file_path)

def metadata(file_path):
    global name
    global artist
    global genre
    global album
    global bitrate
    global year
    tag = TinyTag.get(file_path)

    name = tag.title
    artist = tag.artist
    genre = tag.genre
    album = tag.album
    bitrate = tag.bitrate
    year = tag.year
    streams = 0

    nieuw_nummer=SQL_fitopsy.addSong(name,artist,genre,file_path,0)

    nummerGegevens()
    print("hola",name)

def nummerGegevens():

    popup = Tk()
    popup.wm_title("fitopsy" )
    popup["bg"] = "white"
    popup.iconbitmap("fitopsy.ico")
    popup.geometry("300x120")

    labelNummer = Label(popup,bg ="White", text="Titel:     "+ name)
    labelNummer.grid(row=2, column=0, sticky="W")

    labelArtist = Label(popup,bg ="White", text="Artiest: "+ artist)
    labelArtist.grid(row=1, column=0, sticky="W")

    labelGenre = Label(popup,bg ="White", text="Genre:  "+ genre)
    labelGenre.grid(row=3, column=0, sticky="W")

    labelInfo = Label(popup,bg ="White", text="Info")
    labelInfo.grid(row=0, column=0, sticky="W")

    labelExtraInfo = Label(popup,bg ="White", text="extra info")
    labelExtraInfo.grid(row=0, column=2, sticky="W")

    labelAlbum = Label(popup,bg ="White", text="Album:  "+album)
    labelAlbum.grid(row=1, column=2, sticky="W")

    labelBitrate = Label(popup,bg ="White", text="Bitrate:   "+str(round(bitrate))+"kBits/s")
    labelBitrate.grid(row=2, column=2, sticky="W")
    
    labelYear = Label(popup,bg ="White", text="Jaar:        "+str(year))
    labelYear.grid(row=3, column=2, sticky="W")

    LabelSluiten = Button(popup,bg="white", text=" ok ", command= popup.destroy)
    LabelSluiten.place(relx= 0.5, rely= 0.8)
    

def NummerToevoegen():
    name = ingevoerde_name.get()
    artist = ingevoerde_artist.get()
    genre = ingevoerde_genre.get()
    file_path = ingevoerde_file_path.get()
    print("name::",name)
    nieuw_nummer=SQL_fitopsy.addSong(name,artist,genre,file_path,0)
    print(f"{name =}")

#------------------Popup-scherm voor handmatig toevoegen---------------------------------

def HandmatigToevoegen():
    global ingevoerde_name
    global ingevoerde_artist
    global ingevoerde_genre
    global ingevoerde_file_path

    popup = Toplevel(venster)
    # popup = Tk()
    popup.wm_title("fitopsy" )
    popup["bg"] = "white"
    popup.iconbitmap("fitopsy.ico")
    popup.geometry("300x150")

    ingevoerde_genre = StringVar()
    ingevoerde_genre.set("Hiphop") #keuzemenu voor genres
    entryGenre = OptionMenu(popup, ingevoerde_genre, "Hiphop","Rock","Pop","Klassiek","K-pop","Jazz","Disoc", "Electro","Alternatief" )
    entryGenre.grid(row=2, column=1, sticky="W")

    labelName = Label(popup,bg ="White", text="Titel:" )
    labelName.grid(row=0, column=0, sticky="W")
    
    ingevoerde_name = StringVar()
    entryName = Entry(popup, textvariable=ingevoerde_name)
    entryName.grid(row=0, column=1, sticky="W")

    labelArtist = Label(popup,bg ="White", text="Artiest:" )
    labelArtist.grid(row=1, column=0, sticky="W")
    
    ingevoerde_artist = StringVar()
    entryArtist = Entry(popup, textvariable=ingevoerde_artist)
    entryArtist.grid(row=1, column=1, sticky="W")

    LabelSluiten = Button(popup,bg="white", text=" opslaan", command=NummerToevoegen)
    LabelSluiten.place(relx=0.5,rely=0.8)

    labelGenre = Label(popup,bg ="White", text="Genre:" )
    labelGenre.grid(row=2, column=0, sticky="W")

    # ingevoerde_genre = StringVar()
    # entryGenre = Entry(popup, textvariable=ingevoerde_genre)
    # entryGenre.grid(row=2, column=1, sticky="W")

    labelFilepath = Label(popup,bg ="White", text="Filepath:" )
    labelFilepath.grid(row=3, column=0, sticky="W")

    ingevoerde_file_path = StringVar()
    entryFilepath = Entry(popup, textvariable=ingevoerde_file_path)
    entryFilepath.grid(row=3, column=1, sticky="W")


#------------------Hoofdprogramma---------------------------------

labelIntro = Label(venster,bg = "white", text="F I T O P S Y", font = mainFont )
labelIntro.grid(row=0,column=0, sticky="w")

labelNummer = Label(venster,bg ="White", text="nummer:" )
labelNummer.grid(row=1, column=0, sticky="W")

ingevoerde_nummer = StringVar()
entryNummer = Entry(venster, textvariable=ingevoerde_nummer)
entryNummer.grid(row=1, column=2, sticky="W")

knopNummer = Button(venster, text="zoek nummer", width= 15, command=zoekNummer)
knopNummer.grid(row=1, column=3, sticky="W")

# NieuwNummer = StringVar()
# entryNummerToevoegen = Entry(venster, textvariable=NieuwNummer)
# entryNummerToevoegen.grid(row=2, column=2, sticky="W")

def on_enter(e):
    knopNummerToevoegen['background'] = 'white'

def on_leave(e):
    knopNummerToevoegen['background'] = 'SystemButtonFace'

knopNummerToevoegen = Button(venster,bg="#fffffb",fg="#191414",border=0 ,text="nummer toevoegen \n met metadata", width=20, command=lambda:[BestandKiezen(), metadata(file_path[0])]) 
knopNummerToevoegen.grid(row=2, column=3, sticky="W")
knopNummerToevoegen.bind("<Enter>", on_enter)   #voor het effect van activebackground
knopNummerToevoegen.bind("<Leave>", on_leave)

knopNummerHandmatigToevoegen = Button(venster,text="Nummer toevoegen \n zonder metadata", width=20,height=2, command=lambda: HandmatigToevoegen()) 
knopNummerHandmatigToevoegen.grid(row=3, column=3, sticky="W")

# knopBestand = Button(venster, text="zoek bestand", width= 14, command=BestandKiezen) #bestand
# knopBestand.grid(row=3, column=3, sticky="W")

# knopBestand = Button(venster, text="zoek bestand", width= 14, command=lambda:[BestandKiezen(), metadata(file_path[0])]) #bestand
# knopBestand.grid(row=3, column=3, sticky="W")

# place(relx=0.5, rely=0.5, anchor=CENTER)

# knopSluit = Button(venster, text="Sluiten", width=12, command=venster.destroy)
# knopSluit.place(relx=0.01, rely=0.0, anchor=NE)

# knopNummer = Button(venster, text="zoek nummer", width= 12, command=VoegnummerToe)
# knopNummer.grid(row=2,column=4,sticky="W")

# filePath = BestandKiezen()
# tag.album         # album as string
# tag.albumartist   # album artist as string
# tag.artist        # artist name as string
# tag.audio_offset  # number of bytes before audio data begins
# tag.bitrate       # bitrate in kBits/s
# tag.comment       # file comment as string
# tag.composer      # composer as string 
# tag.disc          # disc number
# tag.disc_total    # the total number of discs
# tag.duration      # duration of the song in seconds
# tag.filesize      # file size in bytes
# tag.genre         # genre as string
# tag.samplerate    # samples per second
# tag.title         # title of the song
# tag.track         # track number as string
# tag.track_total   # total number of tracks as string
# tag.year          # year or data as string

# def NummerToevoegen():
#     nieuw_nummer=SQL_fitopsy.addSong()

##191414 spotify zwart
##1DB954 spotify groen
##fffffb wit
##ebe6e1 donker wit
venster.mainloop()
