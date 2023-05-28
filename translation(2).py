import os
from google.cloud import translate_v3beta1 as translate
from mutagen.easyid3 import EasyID3
from google.auth import default
import concurrent.futures

# Set up Application Default Credentials (ADC)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'put your translation project json here'
credentials, _ = default()

# Counter for successful translations
successful_translations = 0

def translate_audio_metadata(directory):
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
        results = [executor.submit(process_audio_file, file_path, client, project_id) for file_path in file_paths]

        # Wait for all threads to complete
        concurrent.futures.wait(results)

    # Print the number of successful translations
    print(f"Successful Translations: {successful_translations}")

def process_audio_file(file_path, client, project_id):
    global successful_translations

    if file_path.endswith('.mp3') or file_path.endswith('.flac'):
        # Load the audio file and extract metadata
        audio = EasyID3(file_path)

        try:
            # Translate and update title metadata if it's in Japanese
            title_ja = audio.get('title', [''])[0]
            if is_japanese_text(title_ja):
                title_en = translate_text(title_ja, client, project_id)
                audio['title'] = title_en
                successful_translations += 1
            else:
                title_en = title_ja

            # Translate and update album metadata if it's in Japanese
            album_ja = audio.get('album', [''])[0]
            if is_japanese_text(album_ja):
                album_en = translate_text(album_ja, client, project_id)
                audio['album'] = album_en
                successful_translations += 1
            else:
                album_en = album_ja

            # Translate and update artist metadata if it's in Japanese
            artists_ja = audio.get('artist', [])
            artists_en = []
            for artist_ja in artists_ja:
                if is_japanese_text(artist_ja):
                    artist_en = translate_text(artist_ja, client, project_id)
                    artists_en.append(artist_en)
                    successful_translations += 1
                else:
                    artists_en.append(artist_ja)
            audio['artist'] = artists_en

            # Save the changes
            audio.save()

            # Print the original and translated metadata
            print(f"File Name: {file_path}")
            print(f"Original Title: {title_ja}")
            print(f"Translated Title: {title_en}")
            print(f"Original Album: {album_ja}")
            print(f"Translated Album: {album_en}")
            print(f"Original Artists: {', '.join(artists_ja)}")
            print(f"Translated Artists: {', '.join(artists_en)}")
            print("\n")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

def is_japanese_text(text):
    # Check if the text contains any Japanese characters
    return any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' for char in text)

def translate_text(text, client, project_id, target_language='en'):
    # Set the target language
    target_language_code = 'en'
    location = 'global'
    parent = f"projects/{project_id}/locations/{location}"

    # Translate the text
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "ja",
            "target_language_code": target_language_code,
        }
    )

    # Retrieve the translated text
    translation = response.translations[0].translated_text

    return translation

# Provide the directory path containing the audio files
directory_path = 'Put your Music Directory Here'

# Call the function to translate and write audio metadata
translate_audio_metadata(directory_path)