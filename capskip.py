# Import the required packages
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Define the API key and other constants
VIDEO_ID = "OPoMww9x378"


KEYWORDS = ["sponsored by", "in collaboration with", "brought to you by", "paid promotion"]

# Retrieve the transcript for the video using youtube-transcript-api
transcript_list = YouTubeTranscriptApi.get_transcript(VIDEO_ID)
transcript = "\n".join([line["text"] for line in transcript_list])

# Analyze the transcript to detect sponsored segments
sponsored_segments = []
for keyword in KEYWORDS:
    pattern = re.compile(keyword, re.IGNORECASE)
    for match in pattern.finditer(transcript):
        start_time = match.start() / 1000
        end_time = match.end() / 1000
        sponsored_segments.append((match.group(), start_time, end_time))

# Output the results
print("Sponsored segments found:")
for segment in sponsored_segments:
    print(f"Timestamp: {segment[1]:.2f} - {segment[2]:.2f}  Segment: {segment[0]}")
