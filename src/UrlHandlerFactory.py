import logging

class UrlHandlerFactory:
    def __init__(self):
        pass
    @classmethod
    def get_instance(self,url):
        res =url.__contains__("facebook")
        print(res)
        if (url.__contains__("facebook")):
            print("facebook")
        elif (url.__contains__("instagram")):
            print("instagram")
        elif (url.__contains__("tiktok")):
            print("tiktok")
        elif (url.__contains__("youtube")):
            print("youtube")
        else:
            raise TypeError("Sorry the type of the platform is not supported")
# Test code
if __name__ == "__main__":
    try:
       UrlHandlerFactory.get_instance("tiki.com")
    except TypeError:
        logging.error("Sorry the type of platform is not supported") 