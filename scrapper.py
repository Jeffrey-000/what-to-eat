from datetime import date
import requests

class Today:
    def __init__(self):
        self.TODAY = date.today().strftime("%Y-%m-%d")
        self.YEAR = date.today().strftime("%Y")
        self.MONTH = date.today().strftime("%m")
        self.DAY = date.today().strftime("%d")


#------------------------------------------^^^^ugli code--------------------------------------------------

class Bot:
    def __init__(self):
        self.today = Today()
        self.diningHalls = {"BOLTON" : "dining-hall-1",
                            "OHOUSE" : "dining-hall-2",
                            "SNELLING" : "dining-hall-3",
                            "NICHE" : "dining-hall-4",
                            "JOEFRANK" : "dining-hall-5"}
        
    def get_api(self, diningHall): #returns json data in python dict/list form
        url = f"https://uga.api.nutrislice.com/menu/api/weeks/school/{diningHall}/menu-type/dinner/{self.today.YEAR}/{self.today.MONTH}/{self.today.DAY}/"
        #print(url)
        return requests.get(url).json()




if __name__ == "__main__":
    bot = Bot()
    print(bot.today.TODAY)