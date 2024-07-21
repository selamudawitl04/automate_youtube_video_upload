from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
from os.path import isfile, join
import random
from collections import defaultdict




def extractAcc(filepath):
    try:
        s = filepath.split("/")[-1].split("-")
        acc = "-".join(s[1:(2+(len(s) - 4))])
        return acc
    except:
        return ""

def generateTimeRange(duration, clipDuration):
    preHour = int(duration / 60)
    preMin = int(duration % 60)
    preTime = str(preHour // 10) + str(preHour % 10) + ":" + str(preMin // 10) + str(preMin % 10)

    duration += clipDuration
    postHour = int(duration / 60)
    postMin = int(duration % 60)
    postTime = str(postHour // 10) + str(postHour % 10) + ":" + str(postMin // 10) + str(postMin % 10)

    return "@" + preTime

def makeCompilation(path = "./",
                    introName = '',
                    outroName = '',
                    totalVidLength = 10*60,
                    maxClipLength = 20,
                    minClipLength = 5,
                    outputFile = "output.mp4"):

    print("Making Compilation")
    allVideos = []
    seenLengths = defaultdict(list)
    totalLength = 0
    for fileName in os.listdir(path):
        filePath = join(path, fileName)
        if isfile(filePath) and fileName.endswith(".mp4"):
            print(fileName)
            if os.stat(filePath).st_size < 5000:
                continue

            clip = VideoFileClip(filePath)
            duration = clip.duration
            print(duration)
            if duration <= maxClipLength and duration >= minClipLength:
                allVideos.append(clip)
                seenLengths[duration].append(fileName)
                totalLength += duration

    print("Total Length: " + str(totalLength))

    if totalLength == 0:
        print("No video to compile")
        return

    random.shuffle(allVideos)
    duration = 0
    videos = []
    if introName != '':
        introVid = VideoFileClip(join(path, introName))
        videos.append(introVid)
        duration += introVid.duration

    description = ""
    for clip in allVideos:
        timeRange = generateTimeRange(duration, clip.duration)
        acc = extractAcc(clip.filename)
        description += timeRange + " : @" + acc + "\n"
        duration += clip.duration 
        videos.append(clip)
        print(duration)
        if duration >= totalVidLength:
            break

    if outroName != '':
        outroVid = VideoFileClip(join(path, outroName))
        videos.append(outroVid)

    finalClip = concatenate_videoclips(videos, method="compose")
    finalClip.write_videofile(outputFile, threads=12, remove_temp=True, codec="libx264", audio_codec="aac")

    return description

if __name__ == "__main__":
    makeCompilation(path = "/home/minab/Documents/upwork/automated_youtube_channel/test-video1",
                    introName = "",
                    outroName = '',
                    totalVidLength = 1*60,
                    maxClipLength = 20,
                    outputFile = "compiled_video.mp4")
