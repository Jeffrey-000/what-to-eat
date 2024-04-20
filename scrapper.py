from datetime import date
import requests
import time
import json
from pathlib import Path

class Today:
    def __init__(self):
        self.TODAY = date.today().strftime("%Y-%m-%d")
        self.YEAR = date.today().strftime("%Y")
        self.MONTH = date.today().strftime("%m")
        self.DAY = date.today().strftime("%d")

def timeFunc(function_ref):
    def caller(*args, **kwargs):
        begin = time.time()
        ret_value =function_ref(*args, **kwargs)
        end = time.time()
        print(function_ref.__name__, "--- time elapsed : ", str(end - begin))
        return ret_value
    return caller


#useful urls?
#https://uga.api.nutrislice.com/menu/api/schools/

#------------------------------------------^^^^ugli code--------------------------------------------------
WHITE_LIST_CATAGORIES = [] #placeholder objects
WHITE_LIST_FOODS = []
DINNING_HALLS = {}
MEALTYPE = []
#populates globals from data.json
path = Path(__file__).parent / 'data.json' #absolute path to current directory
#allows this file to be executed from directory other than this one, assumeing / here is operator overloading
with open(path) as f:
    temp = json.load(f)
    WHITE_LIST_CATAGORIES = temp["WHITE_LIST_CATAGORIES"]
    WHITE_LIST_FOODS = temp["WHITE_LIST_FOODS"]
    DINNING_HALLS = temp["DINNING_HALLS"]
    MEALTYPE = temp["MEALTYPE"]

class Bot:
    def __init__(self):
        self.today = Today()

    #calls the correct squence of methods then returns dictionary 
    def lazyGet(self, dinningHall):
        data = self.filterParsedMenu(self.parseMenuWholeWeek(self.get_api(dinningHall, 'lunch')))
        return data[self.today.TODAY]


    #prob useless function but making just in case for now
    def updateToday(self):
        self.today = Today()

    #return whole weeks of data
    #returns json data in python dict/list form
    #no error checking, assumes input is always valid    
    #@timeFunc
    def get_api(self, diningHall: str, breakfastLunchOrDinner: str):
        url = f"https://uga.api.nutrislice.com/menu/api/weeks/school/{diningHall}/menu-type/{breakfastLunchOrDinner}/{self.today.YEAR}/{self.today.MONTH}/{self.today.DAY}/"
        #print(url)
        return requests.get(url).json()
    

    #parses raw api data to only include catagories and a list of food that they contain
    #@timeFunc
    def parseMenuWholeWeek(self, data):
        days = {}
        for day in data["days"]: #day is a dictionary object
            catagoryDic = {}

            if len(day["menu_info"]) != 0:

                #groups all foods under the appropriate section name
                #i.e rice undre lemongrass
                for catagory_id in day["menu_info"]:
                    foodUnderThisCatagoryList = []
                    catagoryName = day["menu_info"][catagory_id]["section_options"]["display_name"]
                    #print(menuName)
                    for menu_item in day["menu_items"]: #menu_item is dictionary object
                        #dictionary keys (catagory_id) are strings. to be evaluated all other values must be casted to string
                        #menu_id and caragory_id refer to the same data
                        #each food item is linked under a catagory_id
                        if str(menu_item["menu_id"]) == catagory_id: 
                            foodUnderThisCatagoryList.append(menu_item["food"]["name"])
                    catagoryDic[catagoryName] = foodUnderThisCatagoryList
            days[day['date']] = catagoryDic

        return days
        #return value
        """
        {
        DATE1 : {
                CATAGORY1 : [],
                CATAGORY2 : [],
                ...
                },
        DATE2 : {
                CATAGORY1 : [],
                CATAGORY2 : [],
                ...
                },
        ...
        }
        
        """
    
    #takes in the return data of parseMenu()
    #would be more algorithmicly efficient if integrate with parseMenu function but dont care rn. <--- current 2 methods actually better in case the api data changes in future. less code to change
    #4 nests for loops is very ugly BUT it works
    #@timeFunc
    def filterParsedMenu(self, data: dict):
        filteredDic = {}
        for key, value in data.items(): #key = date, value = {catagory : foodList}
            tempValueDic = {}
            for catagory, foodlist in value.items():
                if catagory in WHITE_LIST_CATAGORIES:
                    tempList = []
                    for foodItem in foodlist:
                        for whiteItem in WHITE_LIST_FOODS: #using two for loops allows for partial string matching using 'in' keyword. i.e allows for 'catfish' to match both 'blackened catfish' and 'miso glaze catfish'
                            if str(whiteItem).lower() in str(foodItem).lower():
                                foodItem = '__***' + foodItem + '***__'  #discord bold underline and italics
                        tempList.append(foodItem)
                    tempValueDic[catagory] = tempList

            filteredDic[key] = tempValueDic

        return filteredDic
    
#TODO: list all the days in which whitelisted food will be on the menu




        
def testing():
    bot = Bot()
    data = bot.get_api(DINNING_HALLS["OHOUSE"], 'lunch')
    data = bot.parseMenuWholeWeek(data)
    print(data[bot.today.TODAY])
    print("\n\n\n\n\n\n\n\n\n")
    print(bot.filterParsedMenu(data))




if __name__ == "__main__":
    testing()