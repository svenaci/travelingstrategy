from bs4 import BeautifulSoup
import regex
from helper_class.chrome_driver import create_driver
from helper_class.chrome_driver import quit_driver
from helper_class.sqlite_advisories import sqlite_advisories
from helper_class.country_names import find_iso_of_country
from helper_class.country_names import find_all_iso
from helper_class.sqlite_advisories import sqlite_advisories


# Used to translate using the googletrans library
import json


def get_url_of_countries():
    info = {}
    try:
        #this is the link to the first page
        url = 'https://www.gov.uk/foreign-travel-advice'

        driver = create_driver()
        driver.get(url)

        #Selenium hands the page source to Beautiful Soup
        soup=BeautifulSoup(driver.page_source, 'lxml')

        #patter of the link to the country page that the href should match
        countries_div = soup.findAll("div", {"class": "govuk-grid-column-two-thirds"})[0]
        countries = countries_div.findAll('a')

        #retrieving links for all countries
        for country in countries:
            country_name = country.text
            href = country['href']
            info[country_name] = {"href":href}
    finally:
        driver.close()
        driver.quit()

    return info


def parse_one_country_advisory(url,href):
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
    for country in urls:
        href = urls[country].get("href")
        link = "https://www.gov.uk{}".format(href,sep='')
        advisory = parse_one_country_advisory(link,href)
        data[country]= {"advisory": advisory}
    return data

def parse_a_country_visa(url, driver):
    info ={}
    driver.get(url)
    #Selenium hands the page source to Beautiful Soup
    soup = BeautifulSoup(driver.page_source, 'lxml')
    visa = " "
    table = soup.find('table')
    table_body = table.find('tbody')
    table_rows = table_body.find_all('tr')
    x = 0
    for tr in table_rows:
         x = x+1
         cols = tr.find_all('td')
         cols = [ele.text.strip() for ele in cols]
         name = cols[0]
         if(x < 5):
           visaLength = len(cols[1])-3
           visa = cols[1][0:visaLength]
         elif( x < 80):
           visaLength = len(cols[1])-4
           visa = cols[1][0:visaLength]
         else:
           visaLength = len(cols[1])-5
           visa = cols[1][0:visaLength]
         if(visa[len(visa)-1: len(visa)] == ']'):
              if(x < 5):
                visaLength = len(visa)-3
                visa = visa[0:visaLength]
              elif( x < 80):
                visaLength = len(visa)-4
                visa = visa[0:visaLength]
              else:
                visaLength = len(visa)-5
                visa = visa[0:visaLength]
         if(name == "Angola"):
           visaLength = len(visa)-2
           visa = visa[0:visaLength]

         info[name] = {"visa":visa}

    return info


def save_to_UK():
    url = get_url_of_countries() #this function create its own driver -- to change
    data = {}
    driver = create_driver()
    visas = parse_a_country_visa("https://en.wikipedia.org/wiki/Visa_requirements_for_British_citizens",driver)
    counter_country = 0

    for country in url:
        driver.implicitly_wait(5)
        name = country
        href = url[country].get("href")

        link = "https://safetravel.govt.nz/{}".format(href,sep='')
        advisory_text = parse_a_country_advisory(link)

        visa_text= ""
        for countryVisa in visas:
            if(countryVisa ==  country):
               visa_text = visas[countryVisa].get('visa')
               break;

        country_iso = "na"
        data[name] = {'country-iso':country_iso,'name':name,'advisory-text':advisory_text,'visa-info':visa_text}
        data = find_all_iso(data)

        if ((counter_country%50) == 0):
            quit_driver(driver)
            driver = create_driver()
        counter_country += 1

    with open('./advisory-uk.json', 'w') as outfile:
        json.dump(data, outfile)

    save_into_db(data)


def save_to_db():
    data = parse_all_countries_advisory()
    # create an an sqlite_advisory object
    sqlite = sqlite_advisories('GB')
    sqlite.delete_table()
    sqlite.create_table()
    for country in data:
        iso = find_iso_of_country(country)
        if(iso != ""):
            name = country
            advisory = data[country].get('advisory')
            visa_info = " "
            sqlite.new_row(iso,name,advisory,visa_info)

    sqlite.commit()
    sqlite.close()

if __name__ == '__main__':
    save_into_db()