Audio Metadata Translation
This code is designed to translate the metadata (e.g., title, album, artist) of audio files in a specified directory from Japanese to English using the Google Cloud Translation API. It supports MP3 and FLAC audio file formats.

Prerequisites
Before running the code, make sure you have the following prerequisites:

Python 3 installed on your system.
Access to the Google Cloud Translation API. You will need to set up a project in the Google Cloud Console and enable the Translation API. Obtain the JSON key file for your service account, which will be used for authentication.
Setup
Clone the repository or download the code files to your local machine.

Install the required Python dependencies using the following command:

Copy code
pip install google-cloud-translate mutagen
Open the code file and update the following variables:

GOOGLE_APPLICATION_CREDENTIALS: Set the path to your JSON key file obtained from the Google Cloud Console.

directory_path: Specify the path to the directory containing the audio files you want to translate.

Usage
To run the code and translate the audio metadata, follow these steps:

Open a terminal or command prompt and navigate to the directory where the code files are located.

Run the following command:

Copy code
python translation.py
The code will process the audio files in the specified directory and translate the metadata from Japanese to English using the Google Cloud Translation API.

The original and translated metadata will be printed for each audio file processed.

Once all the files are processed, the total number of successful translations will be displayed.

Note: It's recommended to test the code on a small subset of audio files before running it on a large collection to ensure it works as expected.


The google-cloud-translation api does require billing to be setup on your account and while there are other free open source api's due to certain issues this was the most efficient way i could think of to make this work. Im open to suggestions and be sure to reach out with any questions and i will do my best to answer them if i see the question.

There are going to be a good amount of errors but i found that it managed to translate most of my 4000+ files correctly 
