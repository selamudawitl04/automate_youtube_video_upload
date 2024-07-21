from scrape_videos import download_instagram_videos
from make_compilation import makeCompilation
from upload_ytvid import uploadYtvid
import schedule
import time
import datetime
import os
import shutil

from google_auth_service import getAuthService
import config


# for instagram login credentials : these variable should stored in config file
IG_USERNAME = config.IG_USERNAME
IG_PASSWORD = config.IG_PASSWORD


# helper variables for video 
num_to_month = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "June",
    7: "July",
    8: "Aug",
    9: "Sept",
    10: "Oct",
    11: "Nov",
    12: "Dec"
} 
title = "TRY NOT TO LAUGH (BEST Dank video memes) V1"
now = datetime.datetime.now()
videoDirectory = "./my_video_" + num_to_month[now.month].upper() + "_" + str(now.year) + "_V" + str(now.day) + "/"
outputFile = "./" + num_to_month[now.month].upper() + "_" + str(now.year) + "_v" + str(now.day) + ".mp4"




# for video compilation
INTRO_VID = '' # SET AS '' IF YOU DONT HAVE ONE
OUTRO_VID = ''
TOTAL_VID_LENGTH = 13*60
MAX_CLIP_LENGTH = 19
MIN_CLIP_LENGTH = 5
DAILY_SCHEDULED_TIME = "20:00"
TOKEN_NAME = "token.json" # Don't change





def routine():

    # Step 1: Scrap video from instagram
    # 1.1: Create Video Directory
    try:
        if not os.path.exists(videoDirectory):
            os.makedirs(videoDirectory)
            print(f"Created directory {videoDirectory}")
    except OSError as e:
        print(f"Error creating directory {videoDirectory}: {e}")

    # 1.2: Scrape Videos
    print("Scraping Videos...")
    download_instagram_videos(username = IG_USERNAME,
                 password = IG_PASSWORD,
                 output_folder = videoDirectory,
                 days=365,
                 max_videos=5
                 )
    print("Scraped Videos!")
    
   

    # Step 2: Compile video
    # print("Making Compilation...")
    makeCompilation(path = videoDirectory,
                    introName = INTRO_VID,
                    outroName = OUTRO_VID,
                    totalVidLength = TOTAL_VID_LENGTH,
                    maxClipLength = MAX_CLIP_LENGTH,
                    minClipLength = MIN_CLIP_LENGTH,
                    outputFile = outputFile)
    print("Made Compilation!")

    # Step 3: Upload to Youtube
    description = "Enjoy the memes! :) \n\n" \
    "like and subscribe to @Chewy for more \n\n" \
    
    description += "\n\nThis is test video description\n\n"
    description += "#test #automate #new #good #funny #no \n\n"

    googleAPI = getAuthService()
    print("Uploading to Youtube...")
    uploadYtvid(VIDEO_FILE_NAME=outputFile,
                title=title,
                description=description,
                googleAPI=googleAPI)
    print("Uploaded To Youtube!")
    
    # Step 4: Cleanup
    print("Removing temp files!")
    # Delete all files made:
    #   Folder videoDirectory
    shutil.rmtree(videoDirectory, ignore_errors=True)
    #   File outputFile
    try:
        os.remove(outputFile)
    except OSError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename, e.strerror))
    print("Removed temp files!")

def attemptRoutine():
    while(1):
        try:
            routine()
            break
        except OSError as err:
            print("Routine Failed on " + "OS error: {0}".format(err))
            time.sleep(60*60)

#attemptRoutine()
schedule.every().day.at(DAILY_SCHEDULED_TIME).do(attemptRoutine)

attemptRoutine()
while True:
    schedule.run_pending()  
    time.sleep(60) # wait one min

