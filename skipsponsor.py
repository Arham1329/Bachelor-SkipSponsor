import cv2
import pytesseract
import argparse
from pytube import YouTube

# Parsing arguments from command line
parser = argparse.ArgumentParser(description='Remove ads from video')
parser.add_argument('source', help='Enter YouTube video id')
# parser.add_argument('dest_file', help='Enter destination output file')
args = parser.parse_args()

source_id = args.source
# dest_file = args.dest_file

def is_sponsored(frame):
    """Detects if frame has a sponsored segment in it

    Parameters:
    frame : The frame to be analyzed

    Returns:
    bool  : True if frame contains sponsor keyword otherwise False 

   """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray)

    keywords = ["sponsored", "promoted", "free trial", "revolut", "sponsor", "with code", "code:", "discovery+"]
    for keyword in keywords:
        if keyword in text.lower():
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

def skip_sponsored(yt_id):
    """Detects if frame has a sponsored segment in it

    Parameters:
    yt_id       : The YouTube video id.
    output_path : Path to the output video.

    Returns:
    video       : Returns a video in mp4 format without sponsored segments
   """
    cap = cap_from_youtube(yt_id)

    frameRate = cap.get(cv2.CAP_PROP_FPS)
    allFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    sponsorStart = None
    sponsorEnd = None

    for i in range(0, allFrames, 10):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            break
        if is_sponsored(frame):
            if sponsorStart is None:
                sponsorStart = i
            sponsorEnd = i
    
    sponsorStartMin, sponsorStartSec = divmod(sponsorStart/frameRate, 60)
    sponsorEndMin, sponsorEndSec = divmod(sponsorEnd/frameRate, 60)       
    print(f"Sponsored segment from {sponsorStartMin:.0f}m {sponsorStartSec:.0f}s to {sponsorEndMin:.0f}m {sponsorEndSec:.0f}s")
    
    # Functionality to remove the sponsored segments 
    # for i in range(allFrames):
    #     ret, frame = cap.read()
    #     if not ret:
    #         break
    #     if i < sponsorStart or i > sponsorEnd:
    #         out.write(frame)
    # cap.release()
    # out.release()

skip_sponsored(source_id)