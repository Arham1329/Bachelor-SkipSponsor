import cv2
import pytesseract
import argparse

# Parsing arguments from command line
parser = argparse.ArgumentParser(description='Remove ads from video')
parser.add_argument('source_file', help='Enter input video file')
parser.add_argument('dest_file', help='Enter destination output file')
args = parser.parse_args()

source_file = args.source_file
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

    keywords = ["sponsored", "ad", "promoted", "free trial"]
    for keyword in keywords:
        if keyword in text.lower():
            return True

    return False

def skip_sponsored(video_path, output_path):
    """Detects if frame has a sponsored segment in it

    Parameters:
    video_path  : Path to the video to be analyzed.
    output_path : Path to the output video.

    Returns:
    video       : Retruns a video in mp4 format without sponosred
                    segements

   """
    cap = cv2.VideoCapture(video_path)

    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frameRate = cap.get(cv2.CAP_PROP_FPS)
    allFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), frameRate, (frameWidth, frameHeight))

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
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    for i in range(allFrames):
        ret, frame = cap.read()
        if not ret:
            break
        if i < sponsorStart or i > sponsorEnd:
            out.write(frame)
    cap.release()
    out.release()

skip_sponsored(source_file, dest_file)