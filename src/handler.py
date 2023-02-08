from bs4 import BeautifulSoup
import requests
import json
from TikTokApi import TikTokApi
from TikTokApi.api.video import Video
from instagram_private_api import Client, ClientCompatPatch


import asyncio


class YoutubeUrlHandler:
    def __init__(self,url_info_list):
        # self.youtube_url = "https://www.youtube.com/watch?v="
        self.youtube_url = url_info_list[1]
        self.url_info_list = url_info_list
        
    def scrap_data(self):
        # req = requests.get(self.youtube_url+self.url_info_list[1])
        req = requests.get(self.youtube_url)

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
        self.req = requests.get(url)
        self.converion_digit_and_symbol_mapper = {"K":1000,"M":1000000,"B":1000000000,"T":1000000000000,"Q":1000000000000000}

    def scrap_data(self):
        self.soup = BeautifulSoup(self.req.text,"html.parser")
        return self

    def get_video_view_count(self):
        # soup.body.findAll(text=re.compile('views'))
        # print(soup.find_all("meta"))
        views_string = self.soup.find_all("meta")[1]["content"]
        views_string = views_string.split(" ")[0]
        print(views_string)
        symbol = views_string[len(views_string) - 1]
        views_string = views_string.replace(views_string[len(views_string) - 1],"")
        views_count = float(views_string)

        return views_count*self.converion_digit_and_symbol_mapper[symbol]

class TikTokUrlHandler:
    def __init__(self,url_info):
        # ["platform","id"]
        self.url_info = url_info
    
    
    def set_access_token(self,access_token):
        self.access_token = access_token

    def scrap_data(self):
        url = "https://tiktok-scraper2.p.rapidapi.com/video/info"

        querystring = {"video_url": self.url_info[1]}

        headers = {
            "X-RapidAPI-Key": self.access_token,
            "X-RapidAPI-Host": "tiktok-scraper2.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        self.res = json.loads(response.text)
        


        return self
    
    def get_video_view_count(self):
        return int(self.res["itemStruct"]["stats"]["playCount"])

# class InstagramUrlHandler:
#     def __init__(self,url_info):
#         # ["platform_name","full video_url"]
#         self.url_info = url_info

#     def set_access_token(self,access_token):
#         self.access_token = access_token

#         return self

#     def scrap_data(self):
#         querystring = {"query":self.url_info[1],"related_posts":"false"}
#         headers = {
#             "X-RapidAPI-Key": self.access_token,
#             "X-RapidAPI-Host": "instagram110.p.rapidapi.com"
#         }

#         url = "https://instagram110.p.rapidapi.com/v2/instagram/post"

#         self.response = requests.request("GET", url, headers=headers, params=querystring)



#         return self
    
#     def get_video_view_count(self):
#         json_data = json.loads(self.response.text)
        
#         # return int(json_data["video_views_count"])
#         return int(json_data["video_plays_count"])



class InstagramUrlHandler:
    def __init__(self,url_info):
        # ["platform_name","full video_url"]
        self.url_info = url_info
        self.api = Client("jibon123420", "@amiakjajabor0433")
        self.media_id = self.api.oembed(url_info[1])["media_id"]

        print("initiating test")
    def set_access_token(self,access_token):
        self.access_token = access_token

        return self

    def scrap_data(self):
        # querystring = {"query":self.url_info[1],"related_posts":"false"}
        # headers = {
        #     "X-RapidAPI-Key": self.access_token,
        #     "X-RapidAPI-Host": "instagram110.p.rapidapi.com"
        # }

        # url = "https://instagram110.p.rapidapi.com/v2/instagram/post"

        # self.response = requests.request("GET", url, headers=headers, params=querystring)
        # print(self.api.medias_info(self.media_id))
        self.json_data = self.api.medias_info(self.media_id.split("_")[0])


        return self
    
    def get_video_view_count(self):
        # json_data = json.loads(self.response.text)
        
        # # return int(json_data["video_views_count"])
        return int(self.json_data["items"][0]["play_count"]
)



#test code
if __name__ == "__main__":
    # youtube_handler = YoutubeUrlHandler(["youtube","YTv7FVaLp68&t=303s"])
    # print(youtube_handler.scrape_data().get_video_view_count())
    # facebook_handler = FacebookUrlHandler("https://www.facebook.com/watch/?v=714212663453200")
    # print(facebook_handler.scrap_data().get_video_view_count())

    # tiktok_handler = TikTokUrlHandler(["tiktok","7194308423406619946"])
    # print(tiktok_handler.scrap_data().get_video_view_count())

    # access_token = ""
    # instagram_handler = InstagramUrlHandler(["instagram","https://www.instagram.com/p/Cn9_atvDau_/"])
    # print(instagram_handler.set_access_token("e36f1e6155mshff1726076963dcbp1c7f3djsne9d31088f5e0").scrape_data().get_video_view_count())
    pass