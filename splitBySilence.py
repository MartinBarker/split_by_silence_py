import sys
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from datetime import timedelta  # Added import for timedelta

print("Split By Silence Python - Martin Barker")

def clear_output_folder():
    if os.path.exists('output'):
        for file in os.listdir('output'):
            file_path = os.path.join('output', file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

def format_time(milliseconds):
    # Convert milliseconds to HH:MM:SS format
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def split_mp3_into_tracks(input_file, num_tracks):
    print(f"Loading audio from {input_file}...")
    audio = AudioSegment.from_mp3(input_file)
    print(f"Audio loaded successfully!")

    print("Splitting audio into tracks...")
    silence_chunks = split_on_silence(audio, silence_thresh=-40, min_silence_len=1000)

    if len(silence_chunks) < num_tracks:
        print("Error: Not enough split points found to create the specified number of tracks.")
        return

    print(f"Found {len(silence_chunks)} split points.")

    clear_output_folder()  # Clear the 'output' folder

    # Create the specified number of tracks
    for i in range(num_tracks):
        if i < len(silence_chunks):
            track = silence_chunks[i]
            output_file = os.path.join('output', f"track_{i + 1}.mp3")  # Save in 'output' folder
            track.export(output_file, format="mp3")
            track_length = len(track)
            formatted_length = format_time(track_length)
            print(f"Track {i + 1} saved as {output_file} ({formatted_length})")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python split_mp3.py <input_mp3_file> <num_tracks>")
    else:
        input_file = sys.argv[1]
        num_tracks = int(sys.argv[2])
        split_mp3_into_tracks(input_file, num_tracks)
