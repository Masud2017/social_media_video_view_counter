import logging

from . import handler
from . import UrlProcessor

class UrlHandlerFactory:
    def __init__(self):
        pass
    @classmethod
    def get_instance(self,url):
        url_processor = UrlProcessor.UrlProcessor(url)
        processed_data = url_processor.get_processed_data()
        
        if (url.__contains__("facebook")):
            facebook_handler = handler.FacebookUrlHandler(url)

            return facebook_handler
            
        elif (url.__contains__("instagram")):
            instagram_handler = handler.InstagramUrlHandler(processed_data)
            instagram_handler.set_access_token("d34345206emshadd9b00e3b03f6fp1f97a4jsn83cf7dddaef2")
            
            return instagram_handler

        elif (url.__contains__("tiktok")):
            tiktok_handler = handler.TikTokUrlHandler(processed_data)

            return tiktok_handler
        elif (url.__contains__("youtube")):
            youtube_handler = handler.YoutubeUrlHandler(processed_data)

            return youtube_handler
        else:
            raise TypeError("Sorry the type of the platform is not supported")
# Test code
if __name__ == "__main__":
    try:
       UrlHandlerFactory.get_instance("tiki.com")
    except TypeError:
        logging.error("Sorry the type of platform is not supported") 