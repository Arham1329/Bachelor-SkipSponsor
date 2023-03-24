import cv2
import pytesseract
import argparse
from pytube import YouTube

# Parsing arguments from command line
parser = argparse.ArgumentParser(description='Remove ads from video')
parser.add_argument('source', help='Enter YouTube video id')
parser.add_argument('dest_file', help='Enter destination output file')
args = parser.parse_args()

source_id = args.source
dest_file = args.dest_file

def is_sponsored(frame):
    """Detects if frame has a sponsored segment in it

    Parameters:
    frame : The frame to be analyzed

    Returns:
    bool  : True if frame contains sponsor keyword otherwise False 

   """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray)

    keywords = ["sponsored", "promoted", "free trial"]
    for keyword in keywords:
        if keyword in text.lower():
            print(keyword)
            return True

    return False

def cap_from_youtube(yt_id):
    """Get video stream from YouTube video id

    Parameters:
    yt_id : The YouTube video id

    Returns:
    cap   : The video stream
    """

    url = f'https://www.youtube.com/watch?v={yt_id}'

    yt = YouTube(url)

    # get the resolution video stream
    stream = yt.streams.get_by_resolution("720p")

    # convert stream to opencv compatible video
    cap = cv2.VideoCapture(stream.url)

    return cap

def skip_sponsored(yt_id, output_path):
    """Detects if frame has a sponsored segment in it

    Parameters:
    yt_id       : The YouTube video id.
    output_path : Path to the output video.

    Returns:
    video       : Returns a video in mp4 format without sponsored segments
   """
    cap = cap_from_youtube(yt_id)

    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frameRate = cap.get(cv2.CAP_PROP_FPS)
    allFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), frameRate, (frameWidth, frameHeight))

    sponsorStart = None
    sponsorEnd = None

    for i in range(0, allFrames, 20):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            break
        if is_sponsored(frame):
            if sponsorStart is None:
                sponsorStart = i
            sponsorEnd = i
            print(f"Sponsored segment from {sponsorStart/frameRate:.2f}s to {sponsorEnd/frameRate:.2f}s")
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    for i in range(allFrames):
        ret, frame = cap.read()
        if not ret:
            break
        if i < sponsorStart or i > sponsorEnd:
            out.write(frame)
    cap.release()
    out.release()

skip_sponsored(source_id, dest_file)