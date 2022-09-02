import os
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class Parser_in_car(object):
    def __init__(self):
        path_driver = os.path.abspath("config/chromedriver")
        options = Options()
        options.headless = True
        self.__driver = webdriver.Chrome(executable_path=path_driver,options=options)
        self.__driver.maximize_window()
        self.__driver.implicitly_wait(3)


    def _get_url(self,count):
        return f'https://losangeles.craigslist.org/search/lac/cta?s={count}&lang=ru'


    def __start_url__(self,url):
        self.__driver.get(url)

    def _parser_page(self,url):
        self.__start_url__(url=url)

        links = [i.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
                 for i in self.__driver.find_elements(by=By.CLASS_NAME, value='result-row')]

        self._get_number_in_page(links)


    def _save_phone_number(self,number_final):
        if os.path.isfile('number.csv'):
            len_file = len(open('number.csv', 'r+', encoding='utf-8').readlines())
        else:
            with open('number.csv', 'a+', encoding='utf-8') as file:
                file.write('Name;Phone\n')
            len_file = 0

        with open('number.csv', 'a+', encoding='utf-8') as file:
            number_final = list(set(number_final))
            for number in number_final:
                if len(number) < 10:
                    continue
                if "+1" in number:
                    number = f"{number}"
                else:
                    try:
                        if number.index('1') == 0:
                            number = f"+{number}"
                        else:
                            number = f"+1{number}"
                    except:
                        number = f"+1{number}"

                save_string = f"name{len_file};{number}\n"
                if len(number) == 12:
                    print(number, self.__driver.current_url)
                    file.write(save_string)


    def _parser_html_in_number(self):
        html = self.__driver.page_source

        parent_n = r"\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}"

        mass_number = list(set(re.findall(parent_n, html)))
        number_final = [i.replace(' ','').replace('(','').replace(')','').replace('.','').replace('-','')
                        for i in mass_number if not i.isdigit()]

        self._save_phone_number(number_final=number_final)



    def _get_number_in_page(self,links):
        for url in links:
            self.__start_url__(url=url)
            self._parser_html_in_number()

    def close_driver(self):
        self.__driver.close()


def len_file_get():
    return str(len(open('number.csv', 'r+', encoding='utf-8').readlines()))


def delete_dubli():
    with open('number.csv','r+',encoding='utf-8') as file:
        file_dd_get = file.readlines()

        array_save = list(set([i.split(';')[1] for i in file_dd_get]))

    with open('number.csv','w+',encoding='utf-8') as file:
        file.write('Name;Phone\n')
        for count, number in enumerate(array_save):
            save_string = f"name{count};{number}"
            file.write(save_string)


def main():
    parser_turbo = Parser_in_car()

    for number_page in range(1,3000,120):

        url = parser_turbo._get_url(number_page)
        parser_turbo._parser_page(url)

    parser_turbo.close_driver()

if '__main__' == __name__:
    try:
        delete_dubli()
    except:
        pass

    start_time = time.time()
    end_time = 0
    while True:
        try:
            main()
        except:
            pass
        try:
            delete_dubli()
        except:
            pass
        end_time = time.time()
        print_string = f"Время работы - {end_time - start_time} Спарсило - {len_file_get()}"
        print(print_string)






