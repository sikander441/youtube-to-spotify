import os
import argparse
import googleapiclient.discovery
import youtube_dl


class DownloadLogger(object):
        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            print(msg)


def ydl_progress_hook(d):
    global hook_call_counter
    if d['status'] == 'downloading':
     if hook_call_counter == 0:
        print('\n'+'--'*65)
        print('\nCurrently downloading: '+d['filename'].upper())
        hook_call_counter+=1
    if d['status'] == 'finished':
        hook_call_counter=0
        print(f'Finished Downloading { d["filename"].upper() } , now converting ...')
        print('\n'+'--'*65)

class SaveYoutubePlaylist:
    # class variables
    api_key = os.environ.get("YOUTUBE_API_KEY")
    fi=0
    li=0
    url=""
    outDir=""

    # class methods, also accesible by objects
    def __init__(self,fi,li,url,outDir):
        self.youtube = self.get_youtube_client()
        self.firstIndex=fi
        self.lastIndex=li
        self.playlistUrl=url
        self.output_dir = outDir

    # returns the youtube client
    def get_youtube_client(self):
        print("picked up API_KEY:"+self.api_key)
        return googleapiclient.discovery.build('youtube', 'v3', developerKey=self.api_key)

    def download_videos(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        'outtmpl': self.output_dir+'/%(title)s.%(ext)s',
        'logger': DownloadLogger(),
        'playlistend':self.lastIndex,
        'playliststart':self.firstIndex,
        'progress_hooks': [ydl_progress_hook],

        }
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        print(self.playlistUrl)
        ydl.download([self.playlistUrl])

if __name__ == "__main__":
    # parse arguments
    arg_parser = argparse.ArgumentParser(description="Download music from any playlist on youtube,You can select range of video to download by giving the starting and ending video number")
    arg_parser.add_argument("-u", "--playlist-url", type=str, help="url of playlist to download",required=True)
    arg_parser.add_argument("-o", "--output-dir", type=str, help="output directory to download songs in (Default if not given is folder named out in current directory )")
    arg_parser.add_argument("-fi", "--first-index", type=str, help="Starting index of the video to download from playlist, Default value if not given is 50")
    arg_parser.add_argument("-li", "--last-index", type=str, help="Last index of video to download from playlist, Default value if not given is 50")
    args = arg_parser.parse_args()

    playlistUrl = args.playlist_url
    output_dir = args.output_dir
    firstIndex = args.first_index
    lastIndex = args.last_index

    if(firstIndex == None):
        firstIndex=1
    if(lastIndex == None):
        lastIndex=50
    if(output_dir == None):
        output_dir='out'


    print('Downloading Playlist from index: ',firstIndex,' to ',lastIndex)
    print('Downloading files in directory: '+output_dir )
    save_youtube = SaveYoutubePlaylist(int(firstIndex),int(lastIndex),playlistUrl,output_dir)
    hook_call_counter=0
    save_youtube.download_videos()




"""

    ***change download path to use the argument given instead of downloading in current dir.
    if unable to find option in youtube-dl, just change the current directory before calling download.
"""
