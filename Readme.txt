# Audio Metadata Translation

This project provides a script for translating audio metadata using the Google Cloud Translation API. It allows you to translate the title, album, and artist metadata of audio files from Japanese to English.

## Prerequisites

Before using this script, make sure you have the following:

- Python 3.x installed on your system.
- Access to the Google Cloud Translation API. You can obtain the API credentials and enable the Translation API in the Google Cloud Console. [Link to the Google Cloud Translation API documentation](https://cloud.google.com/translate/docs/getting-started)
- Audio files in either MP3 or FLAC format with Japanese metadata.

## Installation

1. Clone or download this repository to your local machine.

2. Install the required Python dependencies by running the following command:


3. Set up the Google Cloud credentials by exporting the path to your service account key JSON file:


## Usage

1. Provide the directory path containing the audio files you want to translate by modifying the `directory_path` variable in the `translation.py` file.

2. Open a terminal or command prompt and navigate to the project directory.

3. Run the script by executing the following command:


The script will start processing the audio files, translating the Japanese metadata to English using the Google Cloud Translation API. It will update the metadata of the audio files if the translation is successful.

4. After the script finishes, check the terminal output for the number of successful translations and any errors encountered during the process.

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.


The google-cloud-translation api does require billing to be setup on your account and while there are other free open source api's due to certain issues this was the most efficient way i could think of to make this work. Im open to suggestions and be sure to reach out with any questions and i will do my best to answer them if i see the question.

There are going to be a good amount of errors but i found that it managed to translate most of my 4000+ files correctly 
