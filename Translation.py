import os
import sys
import argparse
from google.cloud import translate_v3beta1 as translate
from mutagen.easyid3 import EasyID3
from google.auth import default
import concurrent.futures

# Set up Application Default Credentials (ADC)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'place your google_application_json here'
credentials, _ = default()

# Counter for successful translations
successful_translations = 0

def translate_audio_metadata(directory, input_language, output_language):
    # Instantiate the Translation API client
    client = translate.TranslationServiceClient(credentials=credentials)

    # Get the project ID from the credentials
    project_id = credentials.project_id

    # Create a list to store the file paths
    file_paths = []

    # Iterate over all files and subdirectories in the directory
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)

    # Process the audio files using threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Process each audio file concurrently
        results = [executor.submit(process_audio_file, file_path, client, project_id, input_language, output_language) for file_path in file_paths]

        # Wait for all threads to complete
        concurrent.futures.wait(results)

    # Print the number of successful translations
    print(f"Successful Translations: {successful_translations}")

def process_audio_file(file_path, client, project_id, input_language, output_language):
    global successful_translations

    if file_path.endswith('.mp3') or file_path.endswith('.flac'):
        # Load the audio file and extract metadata
        audio = EasyID3(file_path)

        try:
            # Translate and update title metadata if it's in the input language
            title = audio.get('title', [''])[0]
            if is_text_in_language(title, input_language):
                translated_title = translate_text(title, client, project_id, input_language, output_language)
                audio['title'] = translated_title
                successful_translations += 1
            else:
                translated_title = title

            # Translate and update album metadata if it's in the input language
            album = audio.get('album', [''])[0]
            if is_text_in_language(album, input_language):
                translated_album = translate_text(album, client, project_id, input_language, output_language)
                audio['album'] = translated_album
                successful_translations += 1
            else:
                translated_album = album

            # Translate and update artist metadata if it's in the input language
            artists = audio.get('artist', [])
            translated_artists = []
            for artist in artists:
                if is_text_in_language(artist, input_language):
                    translated_artist = translate_text(artist, client, project_id, input_language, output_language)
                    translated_artists.append(translated_artist)
                    successful_translations += 1
                else:
                    translated_artists.append(artist)
            audio['artist'] = translated_artists

            # Save the changes
            audio.save()

            # Print the original and translated metadata
            print(f"File Name: {file_path}")
            print(f"Original Title: {title}")
            print(f"Translated Title: {translated_title}")
            print(f"Original Album: {album}")
            print(f"Translated Album: {translated_album}")
            print(f"Original Artists: {', '.join(artists)}")
            print(f"Translated Artists: {', '.join(translated_artists)}")
            print("\n")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

def translate_text(text, client, project_id, input_language, output_language):
    # Set the target language
    target_language_code = output_language
    location = 'global'
    parent = f"projects/{project_id}/locations/{location}"

    # Translate the text
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": input_language,
            "target_language_code": target_language_code,
        }
    )

    # Retrieve the translated text
    translation = response.translations[0].translated_text

    return translation

def is_text_in_language(text, language):
    # Check if the text matches the specified language code
    return text.lower().startswith(language.lower())

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Translate audio metadata.')
    parser.add_argument('directory', type=str, help='Path to the directory containing the audio files')
    parser.add_argument('--input-language', type=str, default='ja', help='Input language code (default: ja)')
    parser.add_argument('--output-language', type=str, default='en', help='Output language code (default: en)')
    args = parser.parse_args()

    # Call the function to translate and write audio metadata
    translate_audio_metadata(args.directory, args.input_language, args.output_language)

if __name__ == "__main__":
    main()
