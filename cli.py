import argparse
import os
from playlist import Playlist
from track import Track
from thumbnail import Thumbnail
from directory_tree import DirectoryTree
from audio_player import play_song


def main():
    """
    Main function for the command-line interface.
    Parses the command-line arguments and performs the required actions.
    """
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Generate a playlist from a music file or directory.")

    # Add arguments for the input file/directory and type
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--file", help="Input music file to generate a playlist from.")
    group.add_argument("-d", "--directory", help="Input directory to generate a playlist from.")

    # Add an argument for the output file
    parser.add_argument("-o", "--output", help="Output playlist file in XSPF format.")

    # Add an argument for playing the song
    parser.add_argument("-p", "--play", metavar="SONG", help="Play the specified song.")

    # Parse the arguments
    args = parser.parse_args()

    # Check if the play option is provided
    if args.play:
        play_song(args.play)
        
    else:
        if args.file:
            # Get the metadata of the file using the Track object
            track = Track(args.file)
            print(track.get_metadata())
        else:
            if args.output:
                # Generate a playlist from the directory
                playlist = Playlist(args.directory)
                playlist.build()
                playlist.save(args.output)
            else:
                # Print directory tree for the current directory
                print(f"Directory tree for {os.getcwd()}:")
                directory_tree = DirectoryTree(os.getcwd())
                directory_tree.print()


if __name__ == "__main__":
    import sys

    # Check if any arguments were passed
    if len(sys.argv) == 1:
        print("Error: You have to provide parameters. Use 'cli.py -h' to see available parameters.")
    else:
        main()
