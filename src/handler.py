from bs4 import BeautifulSoup
import requests
import json
from TikTokApi import TikTokApi
from TikTokApi.api.video import Video


class YoutubeUrlHandler:
    def __init__(self,url_info_list):
        self.youtube_url = "https://www.youtube.com/watch?v="
        self.url_info_list = url_info_list
        
    def scrape_data(self):
        req = requests.get(self.youtube_url+self.url_info_list[1])
        self.youtube_html_doc = req.text
        
        soup = BeautifulSoup(self.youtube_html_doc,"html.parser")
        
#         for div in soup.find_all("div"):
#             print(div)
        print()
        self.view_count_str = soup.select_one('meta[itemprop="interactionCount"][content]')['content']
        return self
        
    def get_video_view_count(self):
        return int(self.view_count_str)


class FacebookUrlHandler:
    def __init__(self,url):
        self.req = requests.get("https://www.facebook.com/watch/?v=5828619303890975")

    def scrap_data(self):
        self.soup = BeautifulSoup(self.req.text,"html.parser")
        return self

    def get_video_view_count(self):
        # soup.body.findAll(text=re.compile('views'))
        # print(soup.find_all("meta"))
        views_string = self.soup.find_all("meta")[1]["content"]
        views_string = views_string.split(" ")[0]
        print(views_string)
        views_string = views_string.replace(views_string[len(views_string) - 1],"")
        views_count = float(views_string)

        return views_count*1000

class TikTokUrlHandler:
    def __init__(self,url_info):
        # ["platform","id"]
        self.url_info = url_info
    
    def scrape_data(self):
        api = TikTokApi()
        video = Video(id = self.url_info[1])
        self.play_count_str = video.info()["stats"]["playCount"]

        return self
    
    def get_video_view_count(self):
        return int(self.play_count_str)

class InstagramUrlHandler:
    def __init__(self,url_info):
        # ["platform_name","full video_url"]
        self.url_info = url_info

    def set_access_token(self,access_token):
        self.access_token = access_token

        return self

    def scrape_data(self):
        querystring = {"query":self.url_info[1],"related_posts":"false"}
        headers = {
            "X-RapidAPI-Key": self.access_token,
            "X-RapidAPI-Host": "instagram110.p.rapidapi.com"
        }

        url = "https://instagram110.p.rapidapi.com/v2/instagram/post"

        self.response = requests.request("GET", url, headers=headers, params=querystring)



        return self
    
    def get_video_view_count(self):
        json_data = json.loads(self.response.text)
        
        return int(json_data["video_views_count"])
#test code
if __name__ == "__main__":
    # youtube_handler = YoutubeUrlHandler(["youtube","YTv7FVaLp68&t=303s"])
    # print(youtube_handler.scrape_data().get_video_view_count())
    # facebook_handler = FacebookUrlHandler("dsfsdf")
    # print(facebook_handler.scrap_data().get_video_view_count())

    # tiktok_handler = TikTokUrlHandler(["tiktok","7194308423406619946"])
    # print(tiktok_handler.scrape_data().get_video_view_count())

    # access_token = ""
    # instagram_handler = InstagramUrlHandler(["instagram","https://www.instagram.com/p/Cn9_atvDau_/"])
    # print(instagram_handler.set_access_token("e36f1e6155mshff1726076963dcbp1c7f3djsne9d31088f5e0").scrape_data().get_video_view_count())
    pass