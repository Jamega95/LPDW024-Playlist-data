import mutagen
import io
from PIL import Image


class Thumbnail:
    def __init__(self, filepath):
        self.filepath = filepath

    def display(self):
        """
        Displays the thumbnail of the given song if available as a block ASCII art.
        """
        try:
            audio = mutagen.File(self.filepath)
            if 'APIC:' in audio.tags:
                image_data = audio.tags['APIC:'].data
                thumbnail = Image.open(io.BytesIO(image_data)).convert('L')
                thumbnail = thumbnail.resize((60, 30))
                ascii_art = self.convert_image_to_ascii(thumbnail)
                print(ascii_art)
        except Exception as e:
            print(f"Error displaying thumbnail: {e}")
    @staticmethod
    def convert_image_to_ascii(image):
        """
        Converts the given image to block ASCII art.

        Args:
            image (PIL.Image.Image): The image to convert.

        Returns:
            str: The ASCII representation of the image.
        """
        ascii_chars = [' ', '░', '▒', '▓', '█']
        ascii_art = ''
        width, height = image.size
        for y in range(height):
            for x in range(width):
                pixel = image.getpixel((x, y))
                char = ascii_chars[pixel // 51]  # Map pixel value to ASCII character
                ascii_art += char * 2  # Repeat the character to match aspect ratio
            ascii_art += '\n'
        return ascii_art
