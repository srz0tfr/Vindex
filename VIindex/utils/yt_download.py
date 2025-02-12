from pytube import YouTube
import argparse 

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", required=True,
	help="URL of youtube video")
args = vars(ap.parse_args())

#ask for the link from user
link = args['url']
yt = YouTube(link)

#Showing details
print("Title: ",yt.title)
print("Number of views: ",yt.views)
print("Length of video: ",yt.length)
print("Rating of video: ",yt.rating)
#Getting the highest resolution possible
ys = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

#Starting download
print("Downloading...")
ys.download()
print("Download completed!!")