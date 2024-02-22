from xml.etree.ElementTree import Element, SubElement, tostring
import os
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from track import Track
import glob

class Playlist:
    def __init__(self, directory, title="My Playlist", creator="Me"):
        """
        Initializes a Playlist object.

        Args:
            directory (str): The directory containing the music files for the playlist.
            title (str): The title of the playlist. Default is "My Playlist".
            creator (str): The creator of the playlist. Default is "Me".
        """
        self.directory = directory
        self.playlist = Element("playlist")
        self.playlist.set("version", "1")
        self.playlist.set("xmlns", "http://xspf.org/ns/0/")
        self.title = SubElement(self.playlist, "title")
        self.title.text = title
        self.creator = SubElement(self.playlist, "creator")
        self.creator.text = creator
        self.tracklist = SubElement(self.playlist, "trackList")
    
    def build(self):
        """
        Builds the playlist by iterating through the music files in the directory.
        Adds each track to the playlist's tracklist.
        """
        for filepath in glob.glob(os.path.join(self.directory, "**/*"), recursive=True):
            if os.path.isfile(filepath) and (filepath.endswith(".mp3") or filepath.endswith(".flac")):
                track = Track(filepath)
                self.tracklist.append(track.to_element())
    
    def save(self, filename):
        """
        Saves the playlist to a file in XSPF format.

        Args:
            filename (str): The name of the output file.
        """
        with open(filename, "w") as f:
            f.write(tostring(self.playlist).decode())
