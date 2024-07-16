from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from db_actions import createDB, insert_data , get_first_n_rows
createDB()
# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open the website
driver.get('https://www.redbus.in/bus-tickets/chennai-to-bangalore?fromCityName=Chennai&fromCityId=123&srcCountry=IND&toCityName=Bangalore&toCityId=122&destCountry=IND&opId=0&busType=Any')

# Wait for the results to load
WebDriverWait(driver, 100000).until(EC.presence_of_element_located((By.CLASS_NAME, 'bus-items')))
print(dir(driver))
driver.maximize_window()
# Scrape the data
import time
import re
start_time = time.time()  # remember when we started
while (time.time() - start_time) < 5:  # should run for 15 seconds
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
bus_items = driver.find_elements(By.CSS_SELECTOR, "ul.bus-items div")
rows=[]
print(len(bus_items))
c=0
for item in bus_items:

    item = item.text.split("\n")
    
    if len(item) < 14:
        continue
    if item[6] != '19-Jul':
        item.insert(6,'19-Jul')
    if 'redDeal applied' in item:
        item.remove('redDeal applied')
    if 'redDeal available' in item:
        item.remove('redDeal available')
    if item[9] != 'Starts from':
        if item[10] == 'Starts from':
            item.remove(item[9])
        else:
            item.insert(9,'Starts from')
        
    if len(item) < 14:
        continue
    c+=1
    #route_name, route_link, busname, bustype, 
            #departing_time, duration, reaching_time, 
            #star_rating, price, seats_available
    mapp = [[3,7],[3,7],0,1,2,4,5,8,10,11]

    # Regular expressions for each item in the list
    regexes = [
        r'(\w+)-(\w+)',  # route_name
        r'(\w+)-(\w+)',  # route_link
        r'(.*)',  # busname
        r'(.*)',  # bustype
        r'(\d{2}:\d{2})',  # departing_time
        r'(\d{2}h \d{2}m)',  # duration
        r'(\d{2}:\d{2})',  # reaching_time
        r'(\d+\.\d+)',  # star_rating
        r'INR (\d+)',  # price
        r'(\d+) Seats available'  # seats_available
    ]

    # Your code here...

    row = []
    for key in mapp:
        if isinstance(key,int):
            row.append(item[key])
        else:
            row.append(f'{item[key[0]]}-{item[key[1]]}')


    # Only append the row to rows if all items match their corresponding regex
    if all(re.match(regex, item) for regex, item in zip(regexes, row)):
        rows.append(row)

    
insert_data(rows)
print(f'inserted {c} rows')
# Close the driver
driver.quit()
# get_first_n_rows()
