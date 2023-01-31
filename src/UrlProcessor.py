class UrlProcessor:
    def __init__(self,url):
        self.url = url
    def get_processed_data(self):
        data = []
        if (self.url.__contains__("facebook") or self.url.__contains__("fb")):
            url_arr = self.url.split("/")
            print(url_arr)
            data.append("facebook")
            data.append(self.url)

        elif (self.url.__contains__("tiktok")):
            arr = self.url.split("/")
            video_id = arr[len(arr)-1]
            
            data.append("tiktok")
            data.append(video_id)

        elif (self.url.__contains__("instagram")):
            data.append("instagram")
            data.append(self.url)

        elif (self.url.__contains__("youtube")):
            # arr = self.url.split("/")
            # # v=343433
            # v_data = arr[len(arr)-1].split("?")[1]
            # video_id = v_data.split("=")[1]

            data.append("youtube")
            # data.append(video_id)
            data.append(self.url)

        return data
# test code
if __name__ == "__main__":
    url_processor = UrlProcessor("https://www.tiktok.com/@sevki8mine/video/7194058613235649797")
    print(url_processor.get_processed_data())