from youtube_transcript_api import YouTubeTranscriptApi

video_id = "vuuD2mKyiPs"

data = YouTubeTranscriptApi.get_transcript(video_id)

# print(data)

for i in data:
    print(i["text"])