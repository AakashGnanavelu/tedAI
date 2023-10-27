from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from csv import writer

driver = webdriver.Chrome()
driver.maximize_window()

pages = 171

data_dict = {
    'URL': [],
    'Title' : [],
    'Speaker': [],
    'Date': [],
    'Views': [],
    'Likes': [],
    'Topics': [],
    'Description': [],
    'Transcript': []
}

data = pd.DataFrame(data_dict)

for x in range(51, pages - 1):
    driver.get(f"https://www.ted.com/talks/quick-list?page={x}")
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    links = soup.find_all('span', {'class' : 'l3'})

    for link in links:

        url = f"https://www.ted.com{link.find('a')['href']}"
        driver.get(url)
        try:
            driver.find_element(By.XPATH, '//button[@data-testid="description-toggle"]').click()
        except NoSuchElementException as e:
            pass
        try:
            driver.find_element(By.XPATH, '//button[text()="Read transcript"]').click()
        except NoSuchElementException as e:
            pass
        time.sleep(2)
        
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        try:
            speaker = soup.find('div', {'data-testid' : 'talk-presenter'}).get_text()[:-3]
        except AttributeError:
            pass

        try:
            title = soup.find('h1', {'class' : 'text-textPrimary-onLight font-light text-tui-2xl leading-tui-sm tracking-tui-tight md:text-tui-3xl md:tracking-tui-tightest lg:text-tui-4xl mr-5'}).get_text()
        except AttributeError:
            pass

        try:
            date = soup.find('div', {'data-testid' : 'talk-release-date'}).get_text()[3:]
        except AttributeError:
            pass

        try:
            views = soup.find('div', {'data-testid' : 'talk-view-count'}).get_text()[:-9]
        except AttributeError:
            pass

        try:
            likes = soup.find('button', {'data-testid' : 'LikeActionButton_TESTID'}).find('span').get_text()[2:-1]
        except AttributeError:

            pass
        try:
            desc = soup.find('span', {'data-testid' : 'talk-description-text'}).get_text()
        except AttributeError:
            pass
        try:
            topics_raw = soup.find('ul', {'class' : 'mb-6 inline-block'}).find_all('a', {'class' : 'inline-block py-1 text-tui-sm capitalize underline'})
            topics = []
            for topic in topics_raw:
                topics.append(topic.get_text())
            print(topics)
        except AttributeError:
            pass

        transcript = ''
        try:
            transcript_raw = soup.find('div', {'data-testid' : 'paragraphs-container'}).find_all('span', {'class' : 'inline cursor-pointer hover:bg-red-300 css-82uonn'})
            for text in transcript_raw:
                transcript += text.get_text().replace("\n", " ")
        except:
            print('No transcript exists')
        new_row = [url, title, speaker, date, views, likes, topics, desc, transcript]

        with open(os.path.join('data.csv'), "a") as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(new_row)
            print(new_row)
            f_object.close()