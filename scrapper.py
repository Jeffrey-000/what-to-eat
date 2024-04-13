from datetime import date
import requests
from time import sleep

class Today:
    def __init__(self):
        self.TODAY = date.today().strftime("%Y-%m-%d")
        self.YEAR = date.today().strftime("%Y")
        self.MONTH = date.today().strftime("%m")
        self.DAY = date.today().strftime("%d")


#useful urls?
#https://uga.api.nutrislice.com/menu/api/schools/

#------------------------------------------^^^^ugli code--------------------------------------------------
WHITE_LIST_CATAGORIES = ['Classic Cuisine', 
                       'Fruit', 
                       'Hickory & Oak Specials', 
                       'Lemon Grass Kitchen Specials', 
                       'Special Selections Specials', 
                       "Chef's Choice", 
                       'Deliciously Southern', 
                       'Dessert Specials',
                       "O'hacienda",
                       'Snelling Selects',
                       'The Bowl Specials',
                       "Headliners"]

WHITE_LIST_FOODS = []


DINNING_HALLS = {"BOLTON" : "dining-hall-1",
                "OHOUSE" : "dining-hall-2",
                "SNELLING" : "dining-hall-3",
                "NICHE" : "dining-hall-4",
                "JOEFRANK" : "dining-hall-5"}

MEALTYPE = ["breakfast", "lunch", "dinner"]

class Bot:
    def __init__(self):
        self.today = Today()

    #prob useless function but making just in case for now
    def updateToday(self):
        self.today = Today()

    #return whole weeks of data
    #returns json data in python dict/list form
    #no error checking, assumes input is always valid    
    def get_api(self, diningHall: str, breakfastLunchOrDinner: str):
        url = f"https://uga.api.nutrislice.com/menu/api/weeks/school/{diningHall}/menu-type/{breakfastLunchOrDinner}/{self.today.YEAR}/{self.today.MONTH}/{self.today.DAY}/"
        #print(url)
        return requests.get(url).json()
    

    #parses raw api data to only include catagories and a list of food that they contain
    def parseMenu(self, data):
        days = {}
        for day in data["days"]: #day is a dictionary object
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


                        #dictionary keys (catagory_id) are strings. to be evaluated all other values must be casted to string
                        #menu_id and caragory_id refer to the same data
                        if str(menu_item["menu_id"]) == catagory_id: 
                            foodUnderThisCatagoryList.append(menu_item["food"]["name"])
                    catagoryDic[catagoryName] = foodUnderThisCatagoryList
            days[day['date']] = catagoryDic

        return days
    
    #takes in the return data of parseMenu()
    #would be more algorithmicly efficient if integrate with parseMenu function but dont care rn
    def filterMenu(self, data: dict):
        filteredDic = {}
        for key, value in data.items(): #key = date, value = {catagory : foodList}
            tempValueDic = {}
            for catagory, foodlist in value.items():
                if catagory in WHITE_LIST_CATAGORIES:
                    tempValueDic[catagory] = foodlist

            filteredDic[key] = tempValueDic

        return filteredDic
    
    #TODO: since intergrating with discord, make function to bold foods in WHITE_LIST_FOODS



        
def testing():
    bot = Bot()
    data = bot.get_api(DINNING_HALLS["BOLTON"], 'lunch')
    data = bot.parseMenu(data)
    print(data[bot.today.TODAY])
    print("\n\n\n\n\n\n\n\n\n")
    print(bot.filterMenu(data))




if __name__ == "__main__":
    testing()