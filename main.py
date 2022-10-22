from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize


def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path):
    # Make folder for archive
    target_folder.mkdir(exist_ok=True, parents=True)
    # Create a folder where we unpack the archive
    # Take the suffix in the file and replace(filename.suffix, '')
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))

    # Create an archive folder with a file name
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'This is not an archive {filename}!')
        folder_for_file.rmdir()
        return None
    


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'Error deleting the folder {folder}')


def main(folder: Path):
    parser.scan(folder)
    for file in parser.JPEG_IMAGES:
        handle_media(file, folder / 'images')
    for file in parser.JPG_IMAGES:
        handle_media(file, folder / 'images')
    for file in parser.PNG_IMAGES:
        handle_media(file, folder / 'images')
    for file in parser.SVG_IMAGES:
        handle_media(file, folder / 'images')

    for file in parser.MP3_AUDIO:
        handle_media(file, folder / 'audio')
    for file in parser.OGG_AUDIO:
        handle_media(file, folder / 'audio')
    for file in parser.WAV_AUDIO:
        handle_media(file, folder / 'audio')
    for file in parser.AMR_AUDIO:
        handle_media(file, folder / 'audio')

    for file in parser.AVI_VIDEO:
        handle_media(file, folder / 'video')
    for file in parser.MP4_VIDEO:
        handle_media(file, folder / 'video')
    for file in parser.MOV_VIDEO:
        handle_media(file, folder / 'video')
    for file in parser.MKV_VIDEO:
        handle_media(file, folder / 'video')

    for file in parser.DOC_DOCUMENTS:
        handle_media(file, folder / 'documents')
    for file in parser.DOCX_DOCUMENTS:
        handle_media(file, folder / 'documents')
    for file in parser.PDF_DOCUMENTS:
        handle_media(file, folder / 'documents')
    for file in parser.TXT_DOCUMENTS:
        handle_media(file, folder / 'documents')
    for file in parser.XLSX_DOCUMENTS:
        handle_media(file, folder / 'documents')
    for file in parser.PPTX_DOCUMENTS:
        handle_media(file, folder / 'documents')        


    for file in parser.MY_OTHER:
        handle_other(file, folder)
    for file in parser.ARCHIVES:
        handle_archive(file, folder / 'archives')

    # Perform a list reverse in order to delete all folders
    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)

def run_sort():

    try:
        folder_for_scan = Path(sys.argv[1])
        
    except IndexError:
        print('Enter path to folder')

    else:    

        print(f'Start in folder {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())


if __name__ == '__main__':

    try:        
        run_sort()
    except FileNotFoundError:
        print(f"Directory not found, try again")



# TODO: run:  python main.py `name_folder`