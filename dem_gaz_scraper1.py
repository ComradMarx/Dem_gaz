import requests
from bs4 import BeautifulSoup
from googletrans import Translator, constants
from pprint import pprint
import pyttsx3
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pandas as pd
import pyttsx3
import time 
from bs4 import BeautifulSoup
from time import gmtime, strftime
import csv 
from requests_html import HTMLSession
import pandas as pd
import requests
from time import gmtime, strftime
from datetime import datetime
from threading import Thread
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import threading
import codecs
import webbrowser
from datetime import date
import calendar

###################################################################################################################
###################################################################################################################

def get_all_links(Z): 

    all_links = Z * ['']

    def get_links(Y):

        url ="https://www.arkansasonline.com/news/news/arkansas/?page="+str(Y+1)

        #grabe the page source for the page
        normal_header = {'Mozilla/5.0': '(Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)', 'From':  'Chrome/96.0.4664.93 Safari/537.36'} #Other option if you get blocked
        normal_header2 = {'User-Agent': 'My User Agent 5.11', 'From': 'ericmarks1@gmail.com'}  #Other Option if you get blocked
        r = requests.get(url, headers = normal_header2).text
        soup    = BeautifulSoup(r,'html.parser') 

        #get the links from the page
        links = []
        for link in soup.findAll('a'):
            links.append(link.get('href'))

        #filter the links from the page... There are advertiser links and what not
        html_links = [ x for x in links if "news-arkansas" in x ]
        html_links_filtered = [i for n, i in enumerate(html_links) if i not in html_links[:n]]

        #append the new links to the master_list:
        html_links_filtered_all = []
        for x in html_links_filtered:
            html_links_filtered_all.append("https://www.arkansasonline.com"+x)

        all_links[Y] = html_links_filtered_all

    if __name__ == '__main__':
        for th in range(0,Z):
            globals()[f"s{th}"] = Thread(target = get_links,  args=(th,))

    #multi fx activation  
    for th in range(0,Z):
        globals()[f"s{th}"].start() 

    #multi thread         
    for th in range(0,Z):
        globals()[f"s{th}"].join() 


    all_links2 = []
    for x in all_links:
        for y in x:
            all_links2.append(y)
            
            
    return all_links2
###################################################################################################################
###################################################################################################################



def scrape_links(all_links):
    #multi-thread function ends
    ##########################################################################################################################################################
    #Global Variables compiled through execution of multithread fx. 
    image_list = len(all_links)*['']
    title_list = len(all_links)*['']
    story_list = len(all_links)*['']

    def dem_gaz_scraper(V): 
        url = all_links[V]
        normal_header = {'Mozilla/5.0': '(Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)', 'From':  'Chrome/96.0.4664.93 Safari/537.36'} #Other option if you get blocked
        normal_header2 = {'User-Agent': 'My User Agent 5.11', 'From': 'ericmarks1@gmail.com'}  #Other Option if you get blocked
        r = requests.get(url, headers = normal_header2).text
        soup = BeautifulSoup(r,'html.parser') 

        #finds the variables inside the HTML
        image = soup.findAll('img')[1]['src']
        if image =='https://media.arkansasonline.com/static/ao_redesign/dist/img/adg-logo.svg':
            image = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'


        title = (soup).find_all('h1')[0].text.replace("’",'')

        #parcing HTML to find Story:
        #######################################
        soup_object = soup.find_all('p')
        list_of_paragraphs = []
        for x in soup_object:
            list_of_paragraphs.append(x.text)

        story =  ' '.join(list_of_paragraphs).replace('\n',"").replace('Send any friend a story As a subscriber, you have 10 gift articles to give each month. Anyone can read what you share.','').replace('Advertisement Supported by','').replace('All rights reserved.', '').replace('  This document may not be reprinted without the express written permission of Arkansas Democrat-Gazette, Inc. Material from the Associated Press is Copyright © 2022, Associated Press and may not be published, broadcast, rewritten, or redistributed. Associated Press text, photo, graphic, audio and/or video material shall not be published, broadcast, rewritten for broadcast or publication or redistributed directly or indirectly in any medium. Neither these AP materials nor any portion thereof may be stored in a computer except for personal and noncommercial use. The AP will not be held liable for any delays, inaccuracies, errors or omissions therefrom or in the transmission or delivery of all or any part thereof or for any damages arising from any of the foregoing.', '').replace('Copyright © 2022, Arkansas Democrat-Gazette, Inc.', '').replace("’",'').replace(' •', '')    #combines list  
        #######################################

        #appends variables to global list
        image_list[V] = (image)
        title_list[V] = (title)
        story_list[V] = (story)

    if __name__ == '__main__':
        for th in range(0,len(all_links)):
            globals()[f"s{th}"] = Thread(target = dem_gaz_scraper,  args=(th,))

    #multi fx activation  
    for th in range(0,len(all_links)):
        globals()[f"s{th}"].start() 

    #multi thread         
    for th in range(0,len(all_links)):
        globals()[f"s{th}"].join() 

        return image_list, title_list, story_list

##########################################################################################################################################################    
##########################################################################################################################################################   
#multi-thread fx ends    



