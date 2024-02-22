import time
import os
import mutagen
from pygame import mixer
from thumbnail import Thumbnail

def play_song(filepath):
    """
    Plays the given song file in the console.

    Args:
        filepath (str): Path to the song file.
    """
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()
    print(f"Now playing: {os.path.basename(filepath)}")
    duration = get_song_duration(filepath)
    start_time = time.time()

    thumbnail = Thumbnail(filepath)
    thumbnail.display()  # Display the thumbnail before playback

    while mixer.music.get_busy():
        current_time = time.time() - start_time
        display_progress(current_time, duration)
        time.sleep(1)

    # Display the final progress after the song finishes
    display_progress(duration, duration)

def get_song_duration(filepath):
    """
    Retrieves the duration of the given song.

    Args:
        filepath (str): Path to the song file.

    Returns:
        float: Duration of the song in seconds.
    """
    audio = mutagen.File(filepath)
    return audio.info.length

def display_progress(current_time, duration):
    """
    Displays the progress of the song playback.

    Args:
        current_time (float): Current playback time in seconds.
        duration (float): Duration of the song in seconds.
    """
    minutes, seconds = divmod(int(current_time), 60)
    progress = current_time / duration
    bar_length = 30
    filled_length = int(bar_length * progress)
    remaining_length = bar_length - filled_length

    print(f"\r[{filled_length * '='}>{remaining_length * ' '}] "
          f"{minutes:02d}:{seconds:02d}/{int(duration // 60):02d}:{int(duration % 60):02d}", end="")
