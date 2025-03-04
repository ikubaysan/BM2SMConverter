import os
import subprocess
import sys
from bm2sm.BM_parser import BMChartParser

# Define input and output group directories
INPUT_GROUPS_DIR = r"C:\Users\PC\Desktop\misc\coding\repos\public\BM2SMConverter\working\input_groups"
OUTPUT_GROUPS_DIR = r"C:\Users\PC\Desktop\misc\coding\repos\public\BM2SMConverter\working\output_groups"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BMX2OGG_PATH = os.path.join(SCRIPT_DIR, "bmx2ogg", "bmx2ogg.exe")


def process_song(input_song_dir, output_song_dir):
    """ Processes a song folder: converts SPA.bme to SM and OGG if no errors occur. """

    spa_bme_path = os.path.join(input_song_dir, "SPA.bme")

    if not os.path.exists(spa_bme_path):
        print(f"Skipping {input_song_dir} - SPA.bme not found.")
        return

    # Ensure output directory exists
    os.makedirs(output_song_dir, exist_ok=True)

    # Convert BME to SM format
    print(f"Converting {spa_bme_path} to StepMania format...")
    try:
        parser = BMChartParser(spa_bme_path, output_song_dir, "S1234567", False)
        parser.SM_converter.compose_chart()
        parser.copy_files()
    except Exception as e:
        print(f"Error converting {spa_bme_path} to SM: {e}")
        return

    # Define the output OGG file path
    output_ogg_path = os.path.join(output_song_dir, "SPA.ogg")

    # Convert BME to OGG
    print(f"Converting {spa_bme_path} to OGG...")
    try:
        command = [BMX2OGG_PATH, spa_bme_path, "-o", output_ogg_path, "-noautofn"]
        subprocess.run(command, cwd=os.path.dirname(BMX2OGG_PATH), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {spa_bme_path} to OGG: {e}")


def main():
    """ Main function to iterate over input groups and process songs. """

    if not os.path.exists(INPUT_GROUPS_DIR):
        print(f"Input directory does not exist: {INPUT_GROUPS_DIR}")
        return

    for group in os.listdir(INPUT_GROUPS_DIR):
        input_group_dir = os.path.join(INPUT_GROUPS_DIR, group)
        if not os.path.isdir(input_group_dir):
            continue  # Skip non-directory files

        output_group_dir = os.path.join(OUTPUT_GROUPS_DIR, group)
        os.makedirs(output_group_dir, exist_ok=True)

        for song_folder in os.listdir(input_group_dir):
            input_song_dir = os.path.join(input_group_dir, song_folder)
            if not os.path.isdir(input_song_dir):
                continue  # Skip non-directory files

            output_song_dir = os.path.join(output_group_dir, song_folder)
            process_song(input_song_dir, output_song_dir)


if __name__ == "__main__":
    main()
