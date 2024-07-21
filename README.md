# Scarp videos from instagram and upload them to youtube

# This software do three main things

    1. Scrap video from instagram
    2. Compile videos
    3. Upload videos

Steps to run the program

1. Configure username and password of the instagram user in config.py like below
   IG_USERNAME = ""
   IG_PASSWORD = ""
2. Configure google cloud provider and download client_secret.json

3. Setup the google api
   python setup_google.py
4. Run the program
   python main.py

# Configuration Options

1. Video Length: You can adjust the length of the compiled video.
2. Days: Specify the number of days for which to scrape videos.
3. Thread Count (Compilation Time): Configure the thread count for compiling videos.
