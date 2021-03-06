import sqlite3
import re
import pycountry
import numpy as np
from helper_class.chrome_driver import create_driver, quit_driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from helper_class.country_names import find_iso_of_country
import copy
from lib.database import Database
from lib.config import sqlite_db
from helper_class.flags import Flags
from helper_class.logger import Logger

# Initialize flags, logger & database
FLAGS = Flags()
LEVEL = FLAGS.get_logger_level()
LOGGER = Logger(level=LEVEL) if LEVEL is not None else Logger()
DB = Database(sqlite_db)

#parsing data for canabais laws
def get_countries_canabaislaw():
    LOGGER.info("Retrieving information for canabais")
    try:
        # this is the link to the first page
        url = 'https://en.wikipedia.org/wiki/Legality_of_cannabis'
        driver = create_driver()
        driver.get(url)
        # Selenium hands the page source to Beautiful Soup
        soup=BeautifulSoup(driver.page_source, 'html.parser')
        # patter of the link to the country page that the href should match
        table = soup.find('table', {'class':"wikitable"})
        tbody = table.find('tbody')
        table_rows = tbody.find_all('tr')

        canabais_info= {}
        arrayCanabaisInfo = {}
        for tablerow in table_rows:
            table_columns = tablerow.find_all('td')
            if(len(table_columns)>0):
                country_name= table_columns[0].text
                recreational= table_columns[1].text
                recreational= re.sub(r'\[\d*\]',' ',recreational.rstrip())
                medical= table_columns[2].text
                medical= re.sub(r'\[\d*\]',' ',medical.rstrip())
                country_iso = find_iso_of_country(country_name)
                canabais_info = {
                    "name":country_name,
                    "iso": country_iso,
                    "canabais-recreational": recreational,
                    "canabais-medical": medical
            }
                arrayCanabaisInfo[country_iso] = canabais_info
        return  arrayCanabaisInfo
   
    except Exception as error_msg:
        LOGGER.error(f'An error has occured while retrieving information for cannabis because of the followin error: {error_msg}')

    finally:
        driver.close()
        driver.quit()

#parsing data for cocaine laws
def get_countries_cocainelaw():
    LOGGER.info("Retrieving information for cocaine")
    try:
        # this is the link to the first page
        url = 'https://en.wikipedia.org/wiki/Legal_status_of_cocaine'
        driver = create_driver()
        driver.get(url)
        # Selenium hands the page source to Beautiful Soup
        soup=BeautifulSoup(driver.page_source, 'html.parser')
        # patter of the link to the country page that the href should match
        table = soup.find('table', {'class':"wikitable"})
        tbody = table.find('tbody')
        table_rows = tbody.find_all('tr')

        cocaine_info= {}
        arrayCocaineInfo = {}
        for tablerow in table_rows:
            table_columns = tablerow.find_all('td')
            if(len(table_columns)>0):
                country_name= table_columns[0].text
                cocaine_possession= table_columns[1].text
                cocaine_possession= re.sub(r'\[\d*\]',' ',cocaine_possession.rstrip())
                cocaine_sale= table_columns[2].text
                cocaine_sale= re.sub(r'\[\d*\]',' ',cocaine_sale.rstrip())
                cocaine_transport= table_columns[3].text
                cocaine_transport= re.sub(r'\[\d*\]',' ',cocaine_transport.rstrip())
                cocaine_cultivation= table_columns[4].text
                cocaine_cultivation= re.sub(r'\[\d*\]',' ',cocaine_cultivation.rstrip())
                country_iso = find_iso_of_country(country_name)
                cocaine_info = {
                    "name":country_name,
                    "iso": country_iso,
                    "cocaine-possession": cocaine_possession,
                    "cocaine-sale": cocaine_sale,
                    "cocaine-transport": cocaine_transport,
                    "cocaine-cultivation": cocaine_cultivation
            }
                arrayCocaineInfo[country_iso] = cocaine_info
        return arrayCocaineInfo
    
    except Exception as error_msg:
        LOGGER.error(f'An error has occured while retrieving information for cocaine because of the following error: {error_msg}')
    
    finally:
        driver.close()
        driver.quit()

#parsing data for mathaphetmine laws
def get_countries_methaphetaminelaw():
    LOGGER.info("Retrieving information for methaphetamine")
    try:
        # this is the link to the first page
        url = 'https://en.wikipedia.org/wiki/Legal_status_of_methamphetamine'
        driver = create_driver()
        driver.get(url)
        # Selenium hands the page source to Beautiful Soup
        soup=BeautifulSoup(driver.page_source, 'html.parser')
        # patter of the link to the country page that the href should match
        table = soup.find('table', {'class':"wikitable"})
        tbody = table.find('tbody')
        table_rows = tbody.find_all('tr')

        methaphetamine_info= {}
        arraymethaphetamineInfo = {}
        for tablerow in table_rows:
            table_columns = tablerow.find_all('td')
            if(len(table_columns)>0):
                country_name= table_columns[0].text
                methaphetamine_possession= table_columns[1].text
                methaphetamine_possession= re.sub(r'\[\d*\]',' ',methaphetamine_possession.rstrip())
                methaphetamine_sale= table_columns[2].text
                methaphetamine_sale= re.sub(r'\[\d*\]',' ',methaphetamine_sale.rstrip())
                methaphetamine_transport= table_columns[3].text
                methaphetamine_transport= re.sub(r'\[\d*\]',' ',methaphetamine_transport.rstrip())
                methaphetamine_cultivation= table_columns[4].text
                methaphetamine_cultivation= re.sub(r'\[\d*\]',' ',methaphetamine_cultivation.rstrip())
                country_iso = find_iso_of_country(country_name)
                methaphetamine_info = {
                    "name":country_name,
                    "iso": country_iso,
                    "methaphetamine-possession": methaphetamine_possession,
                    "methaphetamine-sale": methaphetamine_sale,
                    "methaphetamine-transport": methaphetamine_transport,
                    "methaphetamine-cultivation": methaphetamine_cultivation
            }
                arraymethaphetamineInfo[country_iso] = methaphetamine_info
        return arraymethaphetamineInfo

    except Exception as error_msg:
        LOGGER.error(f'An error has occured while retrieving informtion for methaphetamine because of the following error: {error_msg}')
    finally:
        driver.close()
        driver.quit()

#combining all the tabls for different type of drugs
def combine_dictionaries(dict1, dict2, dict3):


    all_drugs = {}
    temp =  copy.deepcopy(dict1)
    temp.update(dict2)
    temp.update(dict3)

    for iso in temp:
         iso = iso
         country_name = temp[iso].get('name')
         canabais_recreational = ""
         canabais_medical = ""
         cocaine_possession = "no information"
         cocaine_sale = "no information"
         cocaine_transport = "no information"
         cocaine_cultivation ="no information"
         methaphetamine_possession = "no information"
         methaphetamine_sale = "no information"
         methaphetamine_transport = "no information"
         methaphetamine_cultivation = "no information"
         if(iso in dict1):
            canabais_recreational = dict1[iso].get('canabais-recreational')
            canabais_medical  = dict1[iso].get('canabais-medical')
         if(iso in dict2):
            cocaine_possession = dict2[iso].get('cocaine-possession')
            cocaine_sale = dict2[iso].get('cocaine-sale')
            cocaine_transport = dict2[iso].get('cocaine-transport')
            cocaine_cultivation = dict2[iso].get('cocaine-cultivation')
         if(iso in dict3):
            methaphetamine_possession = dict3[iso].get('methaphetamine-possession')
            methaphetamine_sale = dict3[iso].get('methaphetamine-sale')
            methaphetamine_transport = dict3[iso].get('methaphetamine-transport')
            methaphetamine_cultivation = dict3[iso].get('methaphetamine-cultivation')
         all_drugs[iso] = {"name":country_name,
                          "iso": iso,
                          "methaphetamine_possession": methaphetamine_possession,
                          "methaphetamine_sale": methaphetamine_sale,
                          "methaphetamine_transport": methaphetamine_transport,
                          "methaphetamine_cultivation": methaphetamine_cultivation,
                          "cocaine_possession": cocaine_possession,
                          "cocaine_sale": cocaine_sale,
                          "cocaine_transport": cocaine_transport,
                          "cocaine_cultivation": cocaine_cultivation,
                          "canabais_recreational": canabais_recreational,
                          "canabais_medical": canabais_medical
                          }
    return all_drugs

#saving all the infos to the final dictionary
def save_drug_law():

    marijuana = get_countries_canabaislaw()
    cocaine = get_countries_cocainelaw()
    methaphetamine = get_countries_methaphetaminelaw()
    DB = Database(sqlite_db)
    DB.drop_table('drugs')
    DB.add_table('drugs', country_iso='text', name="text", methaphetamine_possession='text', methaphetamine_sale='text', methaphetamine_transport='text', methaphetamine_cultivation='text', cocaine_possession='text', cocaine_sale='text', cocaine_transport='text', cocaine_cultivation='text', canabais_recreational='text', canabais_medical='text')
    drug_info = combine_dictionaries(marijuana,cocaine, methaphetamine)

    for iso in drug_info:
        country_iso = drug_info[iso].get("iso")
        country_name =  drug_info[iso].get("name")
        methaphetamine_possession =  drug_info[iso].get("methaphetamine_possession")
        methaphetamine_sale =  drug_info[iso].get("methaphetamine_sale")
        methaphetamine_transport =  drug_info[iso].get("methaphetamine_transport")
        methaphetamine_cultivation =  drug_info[iso].get("methaphetamine_cultivation")
        cocaine_possession =  drug_info[iso].get("cocaine_possession")
        cocaine_sale =  drug_info[iso].get("cocaine_sale")
        cocaine_transport =  drug_info[iso].get("cocaine_transport")
        cocaine_cultivation =  drug_info[iso].get("cocaine_cultivation")
        canabais_recreational =  drug_info[iso].get("canabais_recreational")
        canabais_medical =  drug_info[iso].get("canabais_medical")

        LOGGER.info(f"Parsing {country_name} to insert into drug table with the following information: {canabais_recreational}. {canabais_medical}.{cocaine_possession}.{methaphetamine_possession}")
        DB.insert('drugs', country_iso, country_name, methaphetamine_possession, methaphetamine_sale, methaphetamine_transport, methaphetamine_cultivation, cocaine_possession, cocaine_sale, cocaine_transport, cocaine_cultivation, canabais_recreational, canabais_medical)

save_drug_law()