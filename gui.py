import os
import xml.etree.ElementTree as ET
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog , Button
from PIL import Image, ImageTk
from mutagen import File
from mutagen.id3 import TALB, TIT2, TPE1, TRCK, TCON, TDRC
from mutagen.mp3 import MP3
from mutagen.flac import FLAC

# Créer la fenêtre principale
root = Tk()
root.title("Générateur de Playlist BOURASSI_AMEGA ")

default_image = Image.open("C:/Users/jameg/PycharmProjects/pythonProject/DU_II-Projet_POO-JEREMIE_ACHRAF/DU_II-Projet_POO-JEREMIE_ACHRAF___src_/no_cover_image.png")
default_image = default_image.resize((150, 150), Image.Resampling.LANCZOS)
default_image = ImageTk.PhotoImage(default_image)

# Définir les variables globales
file_paths = []  # variable globale pour stocker les chemins de fichier

# Définir les fonctions
def add_files():
    global file_paths
    file_types = (
        ("Fichiers MP3", "*.mp3"),
        ("Fichiers FLAC", "*.flac")
    )
    files = filedialog.askopenfilenames(filetypes=file_types)
    if files:
        file_paths += files
        files_list.delete(0, END)
        for file_path in file_paths:
            files_list.insert(END, os.path.basename(file_path))

        # Afficher les métadonnées et la couverture du premier fichier ajouté
        display_metadata_and_cover()

def remove_files():
    global file_paths
    file_paths = []
    files_list.delete(0, END)

def create_playlist(custom=False, playlist_file=None, playlist_name=None, file_paths=None):
    # Vérifier si le nom de la playlist a été fourni
    if not playlist_name:
        messagebox.showerror("Erreur", "Veuillez fournir un nom pour la playlist")
        return

    # Vérifier si le fichier de la playlist existe déjà
    if os.path.isfile(playlist_file):
        overwrite = messagebox.askyesno("Fichier existant", f"Le fichier {playlist_file} existe déjà. Voulez-vous le remplacer ?")
        if not overwrite:
            return

    # Créer l'élément racine de la playlist
    playlist = ET.Element("playlist", version="1", xmlns="http://xspf.org/ns/0/")

    # Créer l'élément title pour le nom de la playlist
    title = ET.Element("title")
    title.text = playlist_name
    playlist.append(title)

    # Ajouter les fichiers à la playlist
    for file_path in file_paths:
        track = ET.Element("track")

        # Ajouter le nom du fichier comme titre de la piste
        title = ET.Element("title")
        title.text = os.path.basename(file_path)
        track.append(title)

        # Ajouter l'emplacement du fichier comme emplacement de la piste
        location = ET.Element("location")
        location.text = file_path
        track.append(location)

        # Ajouter la piste à la playlist
        playlist.append(track)

    # Enregistrer la playlist dans un fichier
    tree = ET.ElementTree(playlist)
    tree.write(playlist_file)

    # Afficher un message de confirmation
    if custom:
        messagebox.showinfo("Playlist créée", f"La playlist {playlist_name} a été créée avec succès !")

def generate_custom_playlist():
    global file_paths

    # Vérifier si des fichiers ont été ajoutés
    if not file_paths:
        messagebox.showerror("Erreur", "Veuillez ajouter des fichiers à la playlist")
        return

    # Demander le nom de la playlist à l'utilisateur
    playlist_name = simpledialog.askstring("Nom de la playlist", "Entrez un nom pour la playlist")

    # Vérifier si l'utilisateur a annulé la boîte de dialogue
    if playlist_name is None:
        return

    # Vérifier si l'utilisateur a entré un nom pour la playlist
    if not playlist_name.strip():
        messagebox.showerror("Erreur", "Veuillez entrer un nom pour la playlist")
        return

    # Créer la playlist
    playlist_file = f"{playlist_name}.xspf"
    create_playlist(custom=True, playlist_file=playlist_file, playlist_name=playlist_name, file_paths=file_paths)

def generate_default_playlist():
    # Demander le nom de la playlist à l'utilisateur
    playlist_name = simpledialog.askstring("Nom de la playlist", "Entrez un nom pour la playlist", initialvalue="Playlist par défaut")

    # Vérifier si l'utilisateur a annulé la boîte de dialogue
    if playlist_name is None:
        return

    # Trouver tous les fichiers musicaux sur l'ordinateur
    file_paths = []
    for root, dirs, files in os.walk("/"):
        for file in files:
            if file.endswith(".mp3") or file.endswith(".flac"):
                file_paths.append(os.path.join(root, file))

    # Créer la playlist
    playlist_file = "Playlist_par_défaut.xspf"
    create_playlist(custom=False, playlist_file=playlist_file, playlist_name=playlist_name, file_paths=file_paths)

    # Afficher un message de confirmation
    messagebox.showinfo("Playlist créée", f"La playlist {playlist_name} a été créée avec succès !")

def open_playlist():
    # Demander à l'utilisateur de sélectionner une playlist existante
    playlist_file = filedialog.askopenfilename(title="Sélectionnez une playlist", filetypes=[("Fichiers de playlist XSPF", "*.xspf")])

    # Vérifier si l'utilisateur a annulé la boîte de dialogue
    if not playlist_file:
        return

    # Analyser le fichier de la playlist
    try:
        tree = ET.parse(playlist_file)
        root = tree.getroot()
    except ET.ParseError:
        messagebox.showerror("Erreur", "Le fichier de la playlist est invalide ou corrompu.")
        return

    # Extraire le nom de la playlist
    playlist_name = os.path.basename(playlist_file)

    # Afficher le nom de la playlist dans la fenêtre principale
    playlist_label.config(text="Nom de la playlist: " + playlist_name)

    # Extraire les informations des pistes
    tracks = []
    for track_elem in root.findall(".//{http://xspf.org/ns/0/}track"):
        title = track_elem.findtext("{http://xspf.org/ns/0/}title")
        location = track_elem.findtext("{http://xspf.org/ns/0/}location")
        if title and location:
            tracks.append((title, location))

    # Afficher les informations de la playlist dans la fenêtre principale
    files_list.delete(0, END)
    file_paths.clear()
    for title, location in tracks:
        files_list.insert(END, title)
        file_paths.append(location)

def display_metadata_and_cover(event=None):
    # Effacer les métadonnées précédentes
    metadata_text.delete(1.0, END)
    cover_image.config(image=None)

    # Récupérer l'index du fichier sélectionné dans la liste
    selection = files_list.curselection()
    if not selection:
        return
    index = selection[0]
    file_path = file_paths[index]

    # Extraire les métadonnées
    file = File(file_path)
    if file is None:
        messagebox.showerror("Erreur", "Le fichier audio n'a pas de tag !")
        return
    metadata = {}
    if isinstance(file, MP3):
        if 'TIT2' in file:
            metadata['Titre'] = file['TIT2'].text[0]
        if 'TALB' in file:
            metadata['Album'] = file['TALB'].text[0]
        if 'TPE1' in file:
            metadata['Artiste'] = file['TPE1'].text[0]
        if 'TRCK' in file:
            metadata['Numéro de piste'] = file['TRCK'].text[0]
        if 'TCON' in file:
            metadata['Genre'] = file['TCON'].text[0]
        if 'TDRC' in file:
            metadata['Année'] = file['TDRC'].text[0]
        if 'APIC:' in file:
            apic = file['APIC:'].data
            with open("temp.jpg", "wb") as f:
                f.write(apic)
            image = Image.open("temp.jpg")
            image = image.resize((200, 200), Image.ANTIALIAS)
            cover_image.image = ImageTk.PhotoImage(image)
            cover_image.config(image=cover_image.image)
        else:
            # Aucune image de couverture trouvée
            cover_image.config(image=default_image)
    elif isinstance(file, FLAC):
        if 'title' in file.tags:
            metadata['Titre'] = file.tags['title'][0]
        if 'album' in file.tags:
            metadata['Album'] = file.tags['album'][0]
        if 'artist' in file.tags:
            metadata['Artiste'] = file.tags['artist'][0]
        if 'tracknumber' in file.tags:
            metadata['Numéro de piste'] = file.tags['tracknumber'][0]
        if 'genre' in file.tags:
            metadata['Genre'] = file.tags['genre'][0]
        if 'date' in file.tags:
            metadata['Année'] = file.tags['date'][0]
        if 'pictures' in file.tags:
            picture = file.tags['pictures'][0]
            with open("temp.jpg", "wb") as f:
                f.write(picture.data)
            image = Image.open("temp.jpg")
            image = image.resize((200, 200), Image.ANTIALIAS)
            cover_image.image = ImageTk.PhotoImage(image)
            cover_image.config(image=cover_image.image)
        else:
            # Aucune image de couverture trouvée
            cover_image.config(image=default_image)

    # Afficher les métadonnées dans la zone de texte
    metadata_text.delete(1.0, END)
    if not metadata:
        metadata_text.insert(END, "Impossible de récupérer les métadonnées demandées.")
    else:
        for key, value in metadata.items():
            metadata_text.insert(END, f"{key}: {value}\n")

def edit_metadata(event=None):
    # Récupérer le fichier audio sélectionné
    selection = files_list.curselection()
    if not selection:
        return
    index = selection[0]
    file_path = file_paths[index]
    

    # Vérifier que le fichier est un MP3 ou un FLAC
    file_type = os.path.splitext(file_path)[1].lower()
    if file_type not in ['.mp3', '.flac']:
        messagebox.showerror("Erreur", "Le fichier sélectionné n'est pas un fichier audio MP3 ou FLAC.")
        return

    # Ouvrir la boîte de dialogue pour l'édition des métadonnées
    metadata = {}
    if file_type == '.mp3':
        file = MP3(file_path)
        if 'TIT2' in file:
            metadata['Titre'] = file['TIT2'].text[0]
        if 'TALB' in file:
            metadata['Album'] = file['TALB'].text[0]
        if 'TPE1' in file:
            metadata['Artiste'] = file['TPE1'].text[0]
        if 'TRCK' in file:
            metadata['Numéro de piste'] = file['TRCK'].text[0]
        if 'TCON' in file:
            metadata['Genre'] = file['TCON'].text[0]
        if 'TDRC' in file:
            metadata['Année'] = file['TDRC'].text[0]
        initial_metadata = metadata.copy()
        edited_metadata = simpledialog.askstring("Édition des métadonnées", "Modifier les métadonnées (au format 'nom: valeur') :", initialvalue=f"{metadata}")
        if edited_metadata is None:
            # L'utilisateur a cliqué sur Annuler
            return
        for item in edited_metadata.split(','):
            item = item.strip()
            if not item:
                continue
            name, value = item.split(':', maxsplit=1)
            name = name.strip()
            value = value.strip()
            if name.lower() in ['titre', 'album', 'artiste', 'numéro de piste', 'genre', 'année']:
                metadata[name.title()] = value
        if metadata == initial_metadata:
            # Pas de modification
            return
        file['TIT2'] = TIT2(encoding=3, text=[metadata.get('Titre', '')])
        file['TALB'] = TALB(encoding=3, text=[metadata.get('Album', '')])
        file['TPE1'] = TPE1(encoding=3, text=[metadata.get('Artiste', '')])
        file['TRCK'] = TRCK(encoding=3, text=[metadata.get('Numéro de piste', '')])
        file['TCON'] = TCON(encoding=3, text=[metadata.get('Genre', '')])
        file['TDRC'] = TDRC(encoding=3, text=[metadata.get('Année', '')])
        file.save()
    else:
        file = FLAC(file_path)
        if 'title' in file.tags:
            metadata['Titre'] = file.tags['title'][0]
        if 'album' in file.tags:
            metadata['Album'] = file.tags['album'][0]
        if 'artist' in file.tags:
            metadata['Artiste'] = file.tags['artist'][0]
        if 'tracknumber' in file.tags:
            metadata['Numérode piste'] = str(file.tags['tracknumber'][0])
        if 'genre' in file.tags:
            metadata['Genre'] = file.tags['genre'][0]
        if 'date' in file.tags:
            metadata['Année'] = str(file.tags['date'][0])
        initial_metadata = metadata.copy()
        edited_metadata = simpledialog.askstring("Édition des métadonnées", "Modifier les métadonnées (au format 'nom: valeur') :", initialvalue=f"{metadata}")
        if edited_metadata is None:
            # L'utilisateur a cliqué sur Annuler
            return
        for item in edited_metadata.split(','):
            item = item.strip()
            if not item:
                continue
            name, value = item.split(':', maxsplit=1)
            name = name.strip()
            value = value.strip()
            if name.lower() in ['titre', 'album', 'artiste', 'numéro de piste', 'genre', 'année']:
                metadata[name.title()] = value
        if metadata == initial_metadata:
            # Pas de modification
            return
        file.tags['title'] = metadata.get('Titre', '')
        file.tags['album'] = metadata.get('Album', '')
        file.tags['artist'] = metadata.get('Artiste', '')
        file.tags['tracknumber'] = metadata.get('Numéro de piste', '')
        file.tags['genre'] = metadata.get('Genre', '')
        file.tags['date'] = metadata.get('Année', '')
        try:
            file.save()
            messagebox.showinfo("Succès", "Les métadonnées ont été modifiées avec succès !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer les métadonnées : {str(e)}")


# Créer les widgets
playlist_label = Label(root, text="Playlist : ")
add_button = Button(root, text="Ajouter musique(s)", command=add_files, width=25)
remove_button = Button(root, text="Reset liste de musique(s)", command=remove_files, width=25)
custom_button = Button(root, text="Générer playlist personnalisée", command=generate_custom_playlist, width=25)
default_button = Button(root, text="Générer playlist par défaut", command=generate_default_playlist, width=25)
open_button = Button(root, text="Réouvrir une playlist", command=open_playlist, width=25)
files_list = Listbox(root, selectmode=MULTIPLE, height=10, width=106)
metadata_label = Label(root, text="Métadonnées du fichier audio sélectionné :")
metadata_text = Text(root, height=10)
cover_label = Label(root, text="Couverture :")
cover_image = Label(root)
button_edit_metadata = Button(root, text="Éditer les métadonnées", command=edit_metadata, width=25)

# Positionner les widgets
playlist_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
add_button.grid(row=1, column=1, padx=5, pady=5, sticky="e")
remove_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")
custom_button.grid(row=3, column=1, padx=5, pady=5, sticky="e")
default_button.grid(row=4, column=1, padx=5, pady=5, sticky="e")
open_button.grid(row=5, column=1, padx=5, pady=5, sticky="e")
files_list.grid(row=1, column=0, rowspan=5, padx=5, pady=5)
metadata_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
metadata_text.grid(row=7, column=0, padx=5, pady=5)
cover_label.grid(row=6, column=1, padx=5, pady=5, sticky="w")
cover_image.grid(row=7, column=1, padx=5, pady=5)
button_edit_metadata.grid(row=8, column=0, padx=5, pady=5)

files_list.bind("<<ListboxSelect>>", display_metadata_and_cover)

# Lancer la fenêtre principale
root.mainloop()
