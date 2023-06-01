# Audio Metadata Translator

This script allows you to translate audio file metadata using the Google Cloud Translation API. It supports translating titles, albums, and artist names of MP3 and FLAC files. The translations are based on the specified input and output languages.

## Prerequisites

- Python 3.6 or above
- Google Cloud Translation API credentials (JSON key file)
- Mutagen
- Google.auth 
- Argparse
Make sure you have these installed beforetrying to use this in the command line 
## Installation

1. Clone or download the repository to your local machine.
2. Install the required Python packages by running the following command:

3. Set up the Google Cloud Translation API:
- Create a project in the Google Cloud Console.
- Enable the Translation API for your project.
- Create a service account and download the JSON key file.
- Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of your JSON key file.

## Usage

1. Go into the command line and type cd "location of the translation.py file" 
2. Run the following command to translate the audio metadata:python translation.py "directory of the music folder you want translated" --input-language "choose the input language" --output-language "choose the output language"
3. remember to use the proper syntax when choosing a folder directory with quotation marks around directories with spaces in it. 
4. https://cloud.google.com/translate/docs/languages check this website to see the short commands for each language and place them in their respective input or output language areas.