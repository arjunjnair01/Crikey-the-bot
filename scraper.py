
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import csv
from datetime import datetime

load_dotenv()

# ESPN Cricket URL
ESPN_CRICKET_URL = "https://www.espncricinfo.com"


def finder2(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    div1=soup.find('div',class_="ds-flex ds-flex-col ds-mb-4")
    if div1:
        text = div1.find('h3').text.strip()
        return text
    else:return("Not available")
         
def scrape_live_scores():
    response = requests.get(ESPN_CRICKET_URL,verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        live_score_div = soup.find('div', class_='ds-relative ds-w-[288px] card scorecard')

        if live_score_div:
            team1 = live_score_div.find('div', class_='ci-team-score ds-flex ds-justify-between ds-items-center ds-text-typo')
            if team1:
                print(1)
                name1=team1.find('div')['title']
                scorediv=team1.find('div',class_='ds-text-compact-s ds-text-typo ds-text-right ds-whitespace-nowrap')
                if scorediv:
                    score1=scorediv.find('strong').text.strip()
                else:score1="0/0"
            else:return "No live scores available! Try again later."
            team2 = team1.find_next_sibling('div')
            if team2:
                print(2)
                name2=team2.find('div')['title']
                scorediv=team2.find('div',class_='ds-text-compact-s ds-text-typo ds-text-right ds-whitespace-nowrap')
                if scorediv:
                    score2=scorediv.find('strong').text.strip()
                else:score2="0/0"
            else:return "No live scores available! Try again later."
            print(3)
            p1=live_score_div.find('p',class_='ds-text-tight-xs ds-font-medium ds-truncate ds-text-typo')
            title=p1['title']
            summary = p1.find('span').text.strip()
            return f"**{title}**\n**{name1}** **{score1}**\n**{name2}** **{score2}**\n{summary}"
            

    return "No live scores available! Try again later."


def append_to_csv(data):
    with open('live_scores.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data])



def latest():
    response = requests.get(ESPN_CRICKET_URL,verify=False)
    if response.status_code == 200:
        
        text = finder2(response)

        return text

    return "Not available! Try again later."
