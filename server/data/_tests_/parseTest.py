import sys
from unittest.mock import MagicMock, Mock
import unittest
import sqlite3
from bs4 import BeautifulSoup

sys.path.append('../')
from advisory_ca import MyBeautifulSoup, get_all_countries, advisory_canada
from advisory_aus import get_url_of_countries, parse_a_country, create_driver, quit_driver
from languages import get_concatinated_values
from advisory_nz import get_url_of_countries_nz, parse_a_country_advisory
from advisory_us import get_name_and_advisory_of_countries
from advisory_uk import get_url_of_countries as get_url_of_countries_uk, parse_one_country_advisory
from advisory_ie import find_all_url, get_one_info
from unsafe_areas_ca import get_all_links, get_all_regional_advisories
from advisory_sg import parse_one_country_advisory as parse_one_country_advisory_sg
from advisory_central_america import mexico_all_links
from vaccines import get_url_of_countries, parse_one_country_vaccine
from weather import save_to_weather
from unsafe_areas_ca import get_regional_advisories, get_all_links
from wiki_weather_parser import  wiki_weather_parser

from helper_class.chrome_driver import create_driver, quit_driver

sys.path.append('../helper_class/')
from wiki_visa_parser import wiki_visa_parser

class parseTest(unittest.TestCase):

    # Tests for canada's parser

    def test_canada_soup(self):
        # tests MyBeautifulSoup() method
        # with Lebanon as a test country
        visa = MyBeautifulSoup("https://data.international.gc.ca/travel-voyage/cta-cap-lb.json", "Visas")
        # tests if it is not empty
        self.assertFalse("", visa)

    def test_canada_getCountry(self):
        # tests get_all_countries() method
        allCountries = get_all_countries()
        # tests to make sure the returned dictionary is not empty
        self.assertFalse("", allCountries)

    def test_canada_adviosry(self):
        # tests advisory_canada() method
        lb = {"AF":"a test"}
        all_data = advisory_canada(lb)
        self.assertFalse({}, all_data)

    # Tests for australia's parser

    def test_australia_getCountry(self):
        # tests getting the correct url of the countries
        urls = get_url_of_countries()
        self.assertFalse("", urls)

    def test_australia_parse(self):
        # tests parsing a single country
        driver = create_driver()
        data = parse_a_country("https://smartraveller.gov.au/Countries/europe/western/Pages/austria.aspx", driver, "Visas")
        quit_driver(driver)
        self.assertFalse("", data)

    # Tests for Language parser

    def test_get_concatinated_values(self):
        # tests comma seperating function
        test_value = ["English", "French", "Spanish"]
        value = get_concatinated_values(test_value)
        self.assertTrue("English, French, Spanish", value)

    # Tests for new zealand's parser

    def test_nz_getCountry(self):
        # tests get url
        driver = create_driver()
        urls = get_url_of_countries_nz(driver)
        quit_driver(driver)
        self.assertFalse("", urls)

    def test_parse_advisory(self):
        # tests getting advisory
        driver = create_driver()
        urls = parse_a_country_advisory("https://safetravel.govt.nz/canada", driver)
        quit_driver(driver)
        self.assertFalse("", urls)

    def tests_nz_parse_visa(self):
        # tests parsing visa
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_New_Zealand_citizens'
        wiki_visa_ob = wiki_visa_parser(wiki_visa_url, driver)
        wiki_visa = wiki_visa_ob.visa_parser_table()
        quit_driver(driver)
        self.assertFalse("", wiki_visa)

    # Tests for USA's parser

    def test_parse_advisory_us(self):
        # tests getting advisory
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_United_States_citizens'
        wiki_visa_ob = wiki_visa_parser(wiki_visa_url, driver)
        wiki_visa = wiki_visa_ob.visa_parser_table()
        quit_driver(driver)
        self.assertFalse("", wiki_visa)

    def tests_us_parse(self):
        # tests parsing visa
        urls = get_name_and_advisory_of_countries()
        self.assertFalse("", urls)

    # Tests for United Kingdom's parser

    def tests_get_url_of_countries_uk(self):
        # tests get url
        urls = get_url_of_countries_uk()
        self.assertFalse("", urls)

    def test_parse_one_country_uk(self):
        # tests parsing of 1 country, Afghanistan
        urls = parse_one_country_advisory("https://www.gov.uk/foreign-travel-advice/afghanistan", "foreign-travel-advice/afghanistan")
        self.assertFalse("", urls)

    def tests_uk_parse_visa(self):
        # tests parsing visa
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_British_citizens'
        wiki_visa_ob = wiki_visa_parser(wiki_visa_url, driver)
        wiki_visa = wiki_visa_ob.visa_parser_table()
        quit_driver(driver)
        self.assertFalse("", wiki_visa)

    # Tests for Ireland's parser

    def test_get_urls_ie(self):
        # tests getting the urls fromt the gov't site
        driver = create_driver()
        urls = find_all_url(driver)
        quit_driver(driver)
        self.assertFalse("", urls)

    def test_get_info_ie(self):
        # tests getting visa info
        my_driver = create_driver()
        soup = BeautifulSoup(my_driver.page_source, 'lxml')
        info = get_one_info('https://www.dfa.ie/travel/travel-advice/a-z-list-of-countries/canada/', 'visa/passport', my_driver, soup)
        quit_driver(my_driver)
        self.assertFalse("", info)

    def test_ie_parse_visa_wiki(self):
        # tests parsing visa from wiki for ie
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_Irish_citizens'
        wiki_visa_ob = wiki_visa_parser(wiki_visa_url, driver)
        wiki_visa = wiki_visa_ob.visa_parser_table()
        quit_driver(driver)
        self.assertFalse("", wiki_visa)

    # Tests for central america's parser

    def test_mx_parse_visa_wiki(self):
        # tests parsing visa from wiki for ie
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_Dominica_citizens'
        wiki_visa_ob = wiki_visa_parser(wiki_visa_url, driver)
        wiki_visa = wiki_visa_ob.visa_parser_table()
        quit_driver(driver)
        self.assertFalse("", wiki_visa)

    def test_do_parse_visa_wiki(self):
        # tests parsing visa from wiki for ie
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_Dominican_Republic_citizens'
        wiki_visa_ob = wiki_visa_parser(wiki_visa_url, driver)
        wiki_visa = wiki_visa_ob.visa_parser_table()
        quit_driver(driver)
        self.assertFalse("", wiki_visa)

    def test_dm_parse_visa_wiki(self):
        # tests parsing visa from wiki for ie
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_Dominica_citizens'
        wiki_visa_ob = wiki_visa_parser(wiki_visa_url, driver)
        wiki_visa = wiki_visa_ob.visa_parser_table()
        quit_driver(driver)
        self.assertFalse("", wiki_visa)

    def test_pa_parse_visa_wiki(self):
        # tests parsing visa from wiki for ie
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_Panamanian_citizens'
        wiki_visa_ob = wiki_visa_parser(wiki_visa_url, driver)
        wiki_visa = wiki_visa_ob.visa_parser_table()
        quit_driver(driver)
        self.assertFalse("", wiki_visa)

    def test_bz_parse_visa_wiki(self):
        # tests parsing visa from wiki for ie
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_Belizean_citizens'
        wiki_visa_ob = wiki_visa_parser(wiki_visa_url, driver)
        wiki_visa = wiki_visa_ob.visa_parser_table()
        quit_driver(driver)
        self.assertFalse("", wiki_visa)

    def test_mx_get_all_urls(self):
        # tests getting all the urls for advisories
        driver = create_driver()
        urls = mexico_all_links(driver)
        quit_driver(driver)
        self.assertFalse("", urls);

    # Test for Caribbean wiki parser

    def test_AG_parse_visa_wiki(self):
        # tests parsing visa from wiki for Antigua and Barbuda
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_Antigua_and_Barbuda_citizens'
        wiki_visa_ob = wiki_visa_parser(wiki_visa_url, driver)
        wiki_visa = wiki_visa_ob.visa_parser_table()
        quit_driver(driver)
        self.assertFalse("", wiki_visa)

    def test_BB_parse_visa_wiki(self):
        # tests parsing visa from wiki for Barbados
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_Barbadian_citizens'
        wiki_visa_ob = wiki_visa_parser(wiki_visa_url, driver)
        wiki_visa = wiki_visa_ob.visa_parser_table()
        quit_driver(driver)
        self.assertFalse("", wiki_visa)

    def test_BS_parse_visa_wiki(self):
        # tests parsing visa from wiki for Bahamas
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_Bahamian_citizens'
        wiki_visa_ob = wiki_visa_parser(wiki_visa_url, driver)
        wiki_visa = wiki_visa_ob.visa_parser_table()
        quit_driver(driver)
        self.assertFalse("", wiki_visa)

    def test_GD_parse_visa_wiki(self):
        # tests parsing visa from wiki for Grenada
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_Grenadian_citizens'


    def test_JM_parse_visa_wiki(self):
        # tests parsing visa from wiki for Jamaica
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_Jamaican_citizens'
        wiki_visa_ob = wiki_visa_parser(wiki_visa_url, driver)
        wiki_visa = wiki_visa_ob.visa_parser_table()
        quit_driver(driver)
        self.assertFalse("", wiki_visa)

    def test_TT_parse_visa_wiki(self):
        # tests parsing visa from wiki for Trinidad and Tobago
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_Trinidad_and_Tobago_citizens'
        wiki_visa_ob = wiki_visa_parser(wiki_visa_url, driver)
        wiki_visa = wiki_visa_ob.visa_parser_table()
        quit_driver(driver)
        self.assertFalse("", wiki_visa)

    def test_sg_parse_advisory(self):
        data = parse_one_country_advisory_sg("https://www.mfa.gov.sg/countries-regions/c/canada/travel-page")
        self.assertFalse("", data)

    #Unsafe areas tests
    #get all links
    def parse_unsafe_areas_all_links(self):
        data = get_all_links()
        self.assertFalse("",data)

    #Parse an unsafe area data
    def parse_one_unsafe_area(self):
        driver = create_driver()
        url = "https://travel.gc.ca/destinations/united-states"
        data = get_regional_advisories(url,driver)
        quit_driver(driver)
        self.assertFalse("",data)
    # Test for Asian countries

    def test_sg_parse_visa_wiki(self):
        # tests parsing visa from wiki for ie
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_Singaporean_citizens'
        wiki_visa_ob = wiki_visa_parser(wiki_visa_url, driver)
        wiki_visa = wiki_visa_ob.visa_parser_table()
        quit_driver(driver)
        self.assertFalse("", wiki_visa)

    def test_mu_parse_visa_wiki(self):
        # tests parsing visa from wiki for mu
        driver = create_driver()
        wiki_visa_url = 'https://en.wikipedia.org/wiki/Visa_requirements_for_Mauritian_citizens'
        wiki_visa_ob = wiki_visa_parser(wiki_visa_url, driver)
        wiki_visa = wiki_visa_ob.visa_parser_table()
        quit_driver(driver)
        self.assertFalse("", wiki_visa)


    # Test for vacines
    def tests_get_url_of_countries_vaccines(self):
        # tests get url
        driver = create_driver()
        urls = get_url_of_countries(driver)
        quit_driver(driver)
        self.assertFalse("", urls)


        #Test for weather
    def test_save_to_weather(self):
        # tests saving weather
        self.assertFalse("",  " ")

    #Test for weather
    def test_wiki_weather_parser(self):
        # tests saving weather
        weather = wiki_weather_parser()
        self.assertFalse("",  weather)



if __name__ == '__main__':
    unittest.main()