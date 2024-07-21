# Scarp videos from instagram and upload them to youtube

# This software do three main things

    1. Scrap video from instagram
    2. Compile videos
    3. Upload videos

Steps to run the program

1. Scrapping Videos from Instagram

   The program scrapes videos from Instagram by logging into a specified Instagram account, retrieving a list of followees, and then iterating through their recent posts to identify and download videos. The number of days to look back and the maximum number of videos to download per followee can be configured. The program handles session management to maintain an authenticated state, ensuring uninterrupted access to the Instagram API.

2. Configure google cloud provider and download client_secret.json
   python setup_google.py
   To enable the application to upload videos to YouTube, you need to set up Google API authentication. This process involves downloading the client_secret.json file from the Google Cloud Console, setting up OAuth 2.0 credentials, and using the provided Python function to authenticate and store the credentials in a pickle file for future use.
3. Run the program
   python main.py

# Configuration Options

1. Video Length: You can adjust the length of the compiled video.
2. Days: Specify the number of days for which to scrape videos.
3. Thread Count (Compilation Time): Configure the thread count for compiling videos.
