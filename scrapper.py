from datetime import date
import requests
from time import sleep

class Today:
    def __init__(self):
        self.TODAY = date.today().strftime("%Y-%m-%d")
        self.YEAR = date.today().strftime("%Y")
        self.MONTH = date.today().strftime("%m")
        self.DAY = date.today().strftime("%d")

#making this a class is probably unessecary but will keep for now
class Menu:
    def __init__(self, data):
        self.data = data
    
    def parseMenu(self):
        days = {}
        for day in self.data["days"]: #day is a dictionary object
            if len(day["menu_info"]) != 0:
                catagoryDic = {}

                #groups all foods under the appropriate section name
                #i.e rice undre lemongrass
                for catagory_id in day["menu_info"]:
                    foodUnderThisCatagoryList = []
                    catagoryName = day["menu_info"][catagory_id]["section_options"]["display_name"]
                    #print(menuName)
                    for menu_item in day["menu_items"]: #menu_item is dictionary object
                        #print(menu_item)
                        #print('\n\n\n\n\n\n')
                        #sleep(20)
                        if str(menu_item["menu_id"]) == catagory_id: #dictionary keys (catagory_id) are strings. to be evaluated all other values must be casted to string
                            foodUnderThisCatagoryList.append(menu_item["food"]["name"])
                    catagoryDic[catagoryName] = foodUnderThisCatagoryList
            days[day['date']] = catagoryDic

        return days
                    


        




#useful urls?
#https://uga.api.nutrislice.com/menu/api/schools/

#------------------------------------------^^^^ugli code--------------------------------------------------

class Bot:
    def __init__(self):
        self.today = Today()
        self.diningHalls = {"BOLTON" : "dining-hall-1",
                            "OHOUSE" : "dining-hall-2",
                            "SNELLING" : "dining-hall-3",
                            "NICHE" : "dining-hall-4",
                            "JOEFRANK" : "dining-hall-5"}
        self.breakfastLunchOrDiner = ["breakfast", "lunch", "dinner"]
        

    #returns json data in python dict/list form
    #no error checking, assumes input is always valid    
    def get_api(self, diningHall: str, breakfastLunchOrDinner: str):
        url = f"https://uga.api.nutrislice.com/menu/api/weeks/school/{diningHall}/menu-type/{breakfastLunchOrDinner}/{self.today.YEAR}/{self.today.MONTH}/{self.today.DAY}/"
        #print(url)
        return requests.get(url).json()


        
def testing():
    bot = Bot()
    menu = Menu(bot.get_api(bot.diningHalls["BOLTON"], bot.breakfastLunchOrDiner[0]))
    print(menu.parseMenu())




if __name__ == "__main__":
    testing()