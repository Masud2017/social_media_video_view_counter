from .models.Models import User,Url,db
from .UrlProcessor import UrlProcessor

class VideoViewsStat:
    def __init__(self):
        self.user_list = User.query.all()
        self.url_list = Url.query.all()
    
    def get_total_views_count_by_url_type(self):
        youtube = 0
        instagram = 0 
        tiktok = 0

        for url_item in self.url_list:
            url_processor = UrlProcessor(url_item.url)
            processed_info = url_processor.get_processed_data()
            print("Url: ",processed_info[1])
            print("Platform type ",processed_info[0])
            if (processed_info[0] == "youtube"):
                youtube = youtube + url_item.view_count
            elif (processed_info[0] == "tiktok"):
                tiktok = tiktok + url_item.view_count
            elif (processed_info[0] == "instagram"):
                instagram = instagram + url_item.view_count
        
        return {"youtube":youtube, "instagram":instagram,"tiktok":tiktok}
    
    def get_total_views_value(self):
        views_count = 0

        for url_item in self.url_list:
            views_count = views_count + url_item.view_count
            
        return views_count

    '''
        This method is used by get_total_views_by_user to get total count of views
        from each user account
    '''
    def get_total_view(self,url_list):
        count = 0

        for url_item in url_list:
            count = count + url_item.view_count

        return count

    def get_total_views_by_user(self):
        user_view_count_mapper = {}
        print("Using user specific total view counter ; ",len (self.user_list))


        for user_item in self.user_list:
            if (user_item.is_admin):
                continue
            user_view_count_mapper[user_item.name] = self.get_total_view(user_item.urls)

        return user_view_count_mapper