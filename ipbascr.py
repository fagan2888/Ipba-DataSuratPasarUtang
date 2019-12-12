import time
import os
import shutil
from selenium import webdriver
import pyautogui
import os
from datetime import datetime
datestring = datetime.strftime(datetime.now(), '(%Y-%m-%d)-(%H.%M.ss)')
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


cwd = os.getcwd()
DRIVER = 'chromedriver'

pathmanual = "C:/Users/BN001166774/Documents/Pasardana.id/IPBA Table/"

chrome_options = webdriver.ChromeOptions()
if os.name == "nt":
    # If current OS is Windows
    chrome_options.add_argument("--start-maximized")
else:
    # Other OS (Mac / Linux)
    chrome_options.add_argument("--kiosk")

#------------------- create folder of the date-------------------

# targetPath = os.path.join(pathmanual, 'FolderPNG');
# while not os.path.exists(targetPath):
#     os.mkdir(targetPath)


#-----------------------------------------------------------------


#------------------------------------------------------------------

tempFolder = os.path.join(os.getcwd(), "Temp")
while not os.path.exists(tempFolder):
	os.mkdir(tempFolder)

driver = webdriver.Chrome(DRIVER, chrome_options = chrome_options)
driver.get('http://www.ibpa.co.id/DataPasarSuratUtang/Indeks/INDOBeX.aspx')
time.sleep(5)
screenshot = driver.save_screenshot('C:/Users/BN001166774/Documents/Pasardana.id/IPBA Table/Temp/atas_'+datestring+'.png')
driver.execute_script("window.scrollTo(0, 500)") 
time.sleep(5)
screenshot = driver.save_screenshot('C:/Users/BN001166774/Documents/Pasardana.id/IPBA Table/Temp/bawah_'+datestring+'.png')
time.sleep(2)

all_html = driver.page_source
soup = BeautifulSoup(all_html,"html.parser")

datasets = []

date = soup.find("span",{"id": "dnn_ctr695_INDOBEX_Data_lblDate"},text = True)
day = soup.find("span",{"id": "dnn_ctr695_INDOBEX_Data_lblDay"},text = True)

all_date = day.get_text()+" "+date.get_text() + " \n"
print(all_date)

for table in soup.findAll("table", {"id": "dnn_ctr695_INDOBEX_Data_gvDailyDate"}):
	for row in table.findAll("tr")[3:]:
		isinya = [td.get_text().replace("  ","") for td in row.findAll("td") if td.get_text()]
		datasets.append(isinya)
		if isinya == []:
			datasets.remove(isinya)
print(*datasets, sep = "\n")

company = "C:/Users/BN001166774/Documents/Pasardana.id/IPBA Table/Temp/ipba_table.csv"
f = open(company, "a")
f.write(all_date)
f.close()

with open(company, 'a') as filehandle:
	filehandle.writelines("%s\n".replace("[","").replace("]","").replace("'","") % table for table in datasets)




targetPath_PNG = os.path.join(pathmanual, datestring)
while not os.path.exists(targetPath_PNG):
	os.mkdir(targetPath_PNG)


cwd = os.getcwd()
source = 'C:/Users/BN001166774/Documents/Pasardana.id/IPBA Table/Temp/'
dest1 = targetPath_PNG


files = os.listdir(source)

for f in files:
        shutil.move(source+f, targetPath_PNG)
