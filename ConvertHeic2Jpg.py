import pyheif
from PIL import Image
import io
import os
import subprocess


def convert_heic_to_jpeg(heic_path, jpeg_path, width=1024):
    # Read the HEIC file
    heif_file = pyheif.read(heic_path)

    # Convert HEIC file to an Image object
    img = Image.open(io.BytesIO(heif_file.data))

    # Calculate the height to maintain the aspect ratio
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio)

    # Resize and save as JPEG
    img.resize((width, height), Image.ANTIALIAS).save(jpeg_path, format="JPEG")


def convert_all_heic_to_jpg(folder_path):
    for file in os.listdir(folder_path):
        if file.lower().endswith('.heic'):
            heic_path = os.path.join(folder_path, file)
            jpeg_path = os.path.join(folder_path, os.path.splitext(file)[0] + '.jpg')
            convert_heic_to_jpeg(heic_path, jpeg_path)
            print(f"Converted {file} to JPEG.")


def convert_heic_to_jpg_with_imagemagick(input_folder, width=1024):
    """
    Convert HEIC files to JPG format using ImageMagick.

    :param input_folder: The path to the folder containing HEIC files.
    :param width: The desired width of the output JPG files. Defaults to 1024.
    :return: None
    """
    files = [f for f in os.listdir(input_folder) if f.lower().endswith('.heic')]
    for file in files:
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(input_folder, os.path.splitext(file)[0] + '.jpg')
        subprocess.run(['magick', 'convert', input_path, '-resize', str(width), output_path])
        print(f"Converted {file} to JPG.")


# Example usage
convert_heic_to_jpg_with_imagemagick('/Users/gzonelee/PycharmProjects/pythonProject1')