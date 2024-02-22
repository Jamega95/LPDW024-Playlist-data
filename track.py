import mutagen
import os
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from xml.etree.ElementTree import Element, SubElement


class Track:
    def __init__(self, filepath):
        """
        Initializes a Track object.

        Args:
            filepath (str): The path to the music file.
        """
        self.filepath = filepath
        if filepath.endswith(".mp3"):
            self.metadata = EasyID3(filepath)
        else:
            self.metadata = FLAC(filepath)
    
    def to_element(self):
        """
        Converts the track to an XML element for inclusion in the playlist.

        Returns:
            xml.etree.ElementTree.Element: The XML element representing the track.
        """
        track = Element("track")
        location = SubElement(track, "location")
        location.text = "file://" + self.filepath.replace(" ", "%20")
        title = SubElement(track, "title")
        title.text = self.metadata.get("title", [os.path.basename(self.filepath)])[0]
        creator = SubElement(track, "creator")
        creator.text = self.metadata.get("artist", [""])[0]
        album = SubElement(track, "album")
        album.text = self.metadata.get("album", [""])[0]
        duration = SubElement(track, "duration")
        duration.text = str(int(self.metadata.get("length", [0])[0]) * 1000)
        return track

    def get_metadata(self):
        """
        Gets the metadata of the track.

        Returns:
            dict: A dictionary containing the metadata of the track.
        """
        if self.filepath.endswith(".mp3"):
            metadata = EasyID3(self.filepath)
        elif self.filepath.endswith(".flac"):
            metadata = FLAC(self.filepath)
        else:
            metadata = {}
        return metadata
