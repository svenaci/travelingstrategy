from bs4 import BeautifulSoup
import regex
from helper_class.chrome_driver import create_driver, quit_driver
from helper_class.country_names import find_iso_of_country, find_all_iso
from helper_class.wiki_visa_parser import wiki_visa_parser
from selenium.webdriver.common.by import By
from lib.database import Database
from helper_class.flags import Flags
from helper_class.logger import Logger
import time

import json

# Initialize flags, logger & database
FLAGS = Flags()
LEVEL = FLAGS.get_logger_level()
LOGGER = Logger(level=LEVEL) if LEVEL is not None else Logger()

def get_url_of_countries():
    info = {}
    LOGGER.info('Retrieving URL of all countries for United Kingdom advisory')
    try:
        #this is the link to the first page
        url = 'https://www.gov.uk/foreign-travel-advice'

        driver = create_driver()
        driver.get(url)

        #Selenium hands the page source to Beautiful Soup
        soup=BeautifulSoup(driver.page_source, 'lxml')

        #patter of the link to the country page that the href should match
        countries_div = soup.findAll("div", {"class": "govuk-grid-column-two-thirds"})[1]
        countries = countries_div.findAll('a')

        #retrieving links for all countries
        for country in countries:
            country_name = country.text
            country_iso = find_iso_of_country(country_name)
            if(country_iso != ""): #Countries that don't have iso are not official counntries
                href = country['href']
                info[country_iso] = {"href":href}
                LOGGER.success(f'URL of {country_name} was successfully retrieved')
    except Exception as error_msg:
      LOGGER.error(f'An error has occured while retrieving URL of countries for United Kingdom advisory because of the following error: {error_msg}')
    finally:
        driver.close()
        driver.quit()

    return info


def parse_one_country_advisory(url, href):
    driver = create_driver()
    driver.get(url)
    advisory=""
    #Selenium hands the page source to Beautiful Soup
    soup=BeautifulSoup(driver.page_source, 'lxml')
    advisory_div = soup.find("div", {"class": "gem-c-govspeak govuk-govspeak direction-ltr"})
    advisory_paragraph1 = advisory_div.findAll("p")[0]
    advisory_paragraph2 = advisory_div.findAll("p")[1]
    advisory = advisory_paragraph1.text +" "+advisory_paragraph2.text
    quit_driver(driver)

    return advisory


def parse_all_countries_advisory():
    data = {}
    urls = get_url_of_countries()
    driver = create_driver()

    
    for country in urls:
       
        href = urls[country].get("href")
        link = "https://www.gov.uk{}".format(href,sep='')
        advisory = parse_one_country_advisory(link,href)
        link =  "https://www.gov.uk{}/safety-and-security".format(href,sep='')
        additional_advisory_info = parse_additional_advisory_info(link, driver)
        data[country]= {"advisory": advisory + additional_advisory_info}
    return data

       
#Acquires additional advisory information
def parse_additional_advisory_info(link, driver):
      # time.sleep(1) #prevents error
       #Selenium hands the page source to Beautiful Soup
       driver.get(link)
       soup=BeautifulSoup(driver.page_source, 'lxml')
       warning = " "

       advisories = soup.find('div', {'class': 'gem-c-govspeak govuk-govspeak direction-ltr'})
    
       count = 0
       tag_type ="<ul>"

       try:       
          for tag in advisories: 
             #Finds and selects only these sections of advisory info
             if(tag.name == 'h3'):
               if(tag.text.strip().lower() == "crime"):
                 count  = 2
                 tag_type = '<li><b>Crime:</b> '
               elif(tag.text.strip().lower() == "road travel"):
                 count  = 2
                 tag_type = '<li><b>Road Travel:</b>'
               elif(tag.text.strip().lower() == "local travel"):
                 count  = 2
                 tag_type = '<li><b>Local Travel:</b>'
               elif(tag.text.strip().lower() == "landmines"):
                 count  = 2
                 tag_type = '<li><b>Landmines</b>'
             elif(count == 2):
               count = 1
             elif(count == 1):
               warning +=  tag_type +" "+ tag.text.strip()
               count = 0

       except : 
           print('No additional information') 
       return warning +'</ul>'


def save_to_UK():

    LOGGER.info("Begin parsing and saving for United Kingdom table...")
    driver = create_driver()
    LOGGER.info('Parsing the visa requirements of all countries for United Kingdom advisory')
    try:
      wiki_visa_url ="https://en.wikipedia.org/wiki/Visa_requirements_for_British_citizens"
      wiki_visa_ob = wiki_visa_parser(wiki_visa_url,driver)
      visas = wiki_visa_ob.visa_parser_table()
      data = parse_all_countries_advisory()
      LOGGER.success('Successfully parsed the visa requirements of all countries for United Kingdom advisory')
    except Exception as error_msg:
      LOGGER.error(f'An error has occured while retrieving the visa reuirements of all countries for United Kingdom advisory because of the following error: {error_msg}')
    
    info = {}
    array_info = []
    # create an an sqlite_advisory object]
    db = Database("countries.sqlite")
    db.drop_table("GB")
    db.add_table("GB", country_iso="text", name="text", advisory_text="text", visa_info="text")
    LOGGER.info('Saving countries informations into the UK table')

    try:
      for country in visas:
          iso = find_iso_of_country(country)
          if(iso != ""):
              try:
                  name = country
                  advisory = data[iso].get('advisory') #dictionary for the travel advisory is iso{advisory:text}
                  visa_info = visas[country].get('visa') #dictionary for visa info is country{visa:text}
                  info = {
                      "country_iso" : iso,
                      "name": name,
                      "advisory": advisory,
                      "visa_info": visa_info
                  }
                  array_info.append(info)
                  LOGGER.success(f"Saving {name} into the UK table with the following information: {visa_info}. {advisory}")
                  db.insert("GB",iso,name,advisory,visa_info)
                  LOGGER.success(f'{name} sucesfully saved to the database.')
              except KeyError:
                  LOGGER.warning(f'This country doesn\'t have advisory info: {country}')
                  print("This country doesn't have advisory info: ",country)
                  LOGGER.info(f'Its ISO is {iso}')
                  print("Its ISO is: ",iso)
      LOGGER.success('All countries have been succesfully saved into the UK table')
   
    except Exception as error_msg:
      LOGGER.error(f'An error has occured while saving countries into the UK table because of the following: {error_msg}')
    db.close_connection()

    with open('./advisory-uk.json', 'w') as outfile:
        json.dump(array_info, outfile)

#save_to_UK()
