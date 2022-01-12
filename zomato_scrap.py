import time         #for using sleep in order to load website
from selenium import webdriver    #webdriver for loading webpages
from selenium.webdriver.common.by import By   # for locating elements in the webpage
from selenium.common.exceptions import NoSuchElementException # For handling exceptions
import pandas as pd # Pandas data manipulation library for storing data as CSV file
from datetime import datetime
from pytz import timezone    


class zomato_scrap:
    def __init__(self, city) -> None:
        self.city = city
        

    def open_browser(self):
        self.driver = webdriver.Firefox()  #instance of Firefox WebDriver is created
        
    def load_url(self):
        self.open_browser()
        self.driver.get(f"https://www.zomato.com/{self.city}")    #The driver.get method will navigate to a page given by the URL
        time.sleep(2)  # Allow 2 seconds for the web page to open

    def infinite_scroll(self):
        self.load_url()
        scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
        screen_height = self.driver.execute_script("return window.screen.height;")   # get the screen height of the web
        i = 1
        ##### Web scrapper for infinite scrolling page #####
        while True:
            # scroll one screen height each time
            self.driver.execute_script(f"window.scrollTo(0, {screen_height}*{i});")  
            i += 1
            time.sleep(scroll_pause_time)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = self.driver.execute_script("return document.body.scrollHeight;")  
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            if (screen_height) * i > scroll_height:
                break

    def extract_data(self):
        self.infinite_scroll()
        ### Extract restaurant details once we reach the end of dynamic Zomato webpage ####
        rest_list = []  ## Restaurant list variable to which dictionary of each restaurant details will be appended

        row = 10 # row variable for iterating Restaurant elements XPATH (***This has to checked manually in the webpage manually before running this script since it will also change dynamically sometimes***)
        column = 1 # column variable for iterating Restaurant elements XPATH

        while True:  #infinite loop initiation
            # Restaurants are diplayed in the website similar to (n-rows x 3-columns) matrix. So basically we are indexing the XPATH link using row and column cariable.
            if column > 3:   #Since 3 restaurants are displayed in 1 row, this condition is necessary to restrict the column within 3.
                row += 1     # Row is also incremented to 1 to move on to the next row when column variable completed 3.
                column = 1   # we also need the reset the column back to 1 

            try:
                rest_name = self.driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[{row}]/div/div[{column}]/div/div/a[2]/div[1]/h4").text  #Returns retaurant name from corresponding XPATH element 
            except NoSuchElementException:  #If the XPATH isn't found this exception is raised and handled
                rest_name = None

            try:
                rating = self.driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[{row}]/div/div[{column}]/div/div/a[2]/div[1]/div/div/div/div/div/div[1]").text #Returns retaurant rating from corresponding XPATH element
            except NoSuchElementException: #If the XPATH isn't found this exception is raised and handled
                rating = None

            try:
                offer_ = self.driver.find_elements(By.XPATH, f"/html/body/div[1]/div/div[{row}]/div/div[{column}]/div/div/a[1]/div[3]/p") ##Returns list of Offers from corresponding XPATH elements
                if len(offer_) > 1:  #checking the length if there are any multiple offers
                    pro_offer = offer_[0].text #Zomato offer for only pro users
                    offer = offer_[1].text # Zomato offer for all users
                else:                      
                    pro_offer = None
                    offer = self.driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[{row}]/div/div[{column}]/div/div/a[1]/div[3]/p").text #Returns offer from corresponding XPATH element
            except NoSuchElementException: #If the XPATH isn't found this exception is raised and handled
                pro_offer = None
                offer = None

            try:
                del_time = self.driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[{row}]/div/div[{column}]/div/div/a[1]/p").text #Returns delivery time from corresponding XPATH element
            except NoSuchElementException: #If the XPATH isn't found this exception is raised and handled
                del_time = None

            try:
                category = self.driver.find_element(By.XPATH,f"/html/body/div[1]/div/div[{row}]/div/div[{column}]/div/div/a[2]/div[2]/p[1]").text #Returns restaurant category from corresponding XPATH element
            except NoSuchElementException:  #If the XPATH isn't found this exception is raised and handled
                category = None

            try:
                cfo = self.driver.find_element(By.XPATH,f"/html/body/div[1]/div/div[{row}]/div/div[{column}]/div/div/a[2]/div[2]/p[2]").text #Returns *cost for one* from corresponding XPATH element
            except NoSuchElementException: #If the XPATH isn't found this exception is raised and handled
                cfo = None

            try:
                roc = self.driver.find_element(By.XPATH,f"/html/body/div[1]/div/div[{row}]/div/div[{column}]/div/div/a[2]/div[4]/div/div/div/p").text #Returns *recent orders count* from corresponding XPATH element
            except NoSuchElementException:  #If the XPATH isn't found this exception is raised and handled
                roc = None

            if (rest_name or rating or offer or del_time or category or cfo or roc) == None:     #This is the infinite loop breaker. When all the variables is none, loop breaks
                break


            rest_item = {                         #dictionary for storing the restaurant feature variables
                'rest_name' : rest_name,
                'rating' : rating,
                'pro_offer': pro_offer,
                'offer' : offer,
                'del_time' : del_time,
                'category' : category,
                'cost_for_one' : cfo,
                'recent_orders_count': roc
            }

            rest_list.append(rest_item)     #dictionsry will be appended to this rest_list

            column += 1 # column is incremented

        return rest_list    


    def convert_csv(self):
        india = timezone('Asia/Kolkata')
        india_time = datetime.now(india).strftime('%Y_%m_%d-%H_%M_%S')
        df = pd.DataFrame(self.extract_data())    #dataframe creation from the list
        df.to_csv(f"Zomato_rest_{self.city}_{india_time}.csv", index = False) #Saving as CSV file


covai = zomato_scrap("coimbatore")
covai.convert_csv()   
