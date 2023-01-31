from models.Models import User
class AuthHandler:
    def __init__(self,db):
        self.db = db

    def authenticate(self):
        user = User(name = "Tanvir",email = "tanvir@gmail.com",password = "jpmasudxp")
        db.session.add(user)
        db.serssion.commit()
        pass

    def register(self):
        pass

    def forget_pass(self):
        pass
