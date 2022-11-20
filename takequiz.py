#!/usr/bin/python3

import os
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv  


chrome_options = Options
chrome_options.binary_location = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe" 
s = Service(r'C:\Users\Prateek\anaconda3\pkgs\python-chromedriver-binary-108.0.5359.22.0-py39hcbf5309_0\Lib\site-packages\chromedriver_binary\chromedriver.exe')
driver = webdriver.Chrome(service = s)
driver.get('https://www.merriam-webster.com/word-games/vocabulary-quiz')

driver.maximize_window() #after executing this I should click on the window manually; code works then dunno why 
time.sleep(2)


button = driver.find_element(By.LINK_TEXT, 'START THE QUIZ')
button.click()

dt = str(datetime.now().replace( microsecond=0)) #doesn't give microseconds 
Date, Time = dt.split()


xpath1 = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/div/div/div[2]/div[2]/div[1]/p/b')
word1 = xpath1.text
print(word1)

diffwords = ''

option1 = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/div/div/div[2]/div[2]/div[2]/div[1]/a[1]')
option2 = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/div/div/div[2]/div[2]/div[2]/div[1]/a[2]')
option3 = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/div/div/div[2]/div[2]/div[2]/div[1]/a[3]')
option4 = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/div/div/div[2]/div[2]/div[2]/div[1]/a[4]')    


#driver.execute_script("window.open('');") #opens new tab in the same beta chrome window
#tss = "https://www.thesaurus.com/browse/" + word1 #creates the web address for thesaurus

#driver.switch_to.window(driver.window_handles[1]) #switches to the new tab; dunno what [1] means; copied from geeksforgeeks
#driver.get(tss) #goes to the thesaurus for the current word

tss = "https://www.thesaurus.com/browse/" + word1
setofsyns = set()
reqs = requests.get(tss)
soup = BeautifulSoup(reqs.text, 'lxml')
for tag in soup.find_all('div', {'data-testid': 'word-grid-container'}):
    for li in tag.find_all('li'):
        setofsyns.add(li.text.strip()) #strip method because it was having whitespace at the end
print('The set of synonyms is:', setofsyns)

driver.implicitly_wait(2)
setofoptions  = {option1.text, option2.text, option3.text, option4.text} #BIGGEST ISSUE: somehow the text from the web element is not stored in a variable/set always thus returning a null setofoptions
print ('The set of options is:', setofoptions, '\n')

intersection = setofsyns.intersection(setofoptions)
ans = ''.join(str(e) for e in intersection)

if len(intersection) == 1:
    ansbutton = driver.find_element(By.LINK_TEXT, ans)
    driver.implicitly_wait(2)
    ansbutton.click()
else:
    diffwords += ' '+word1
    rand_ans = str(random.choice(tuple(setofoptions)))
    rand_ansbutton = driver.find_element(By.LINK_TEXT, rand_ans)
    driver.implicitly_wait(2)
    rand_ansbutton.click()
    
#sometimes setofoptions is just empty and sometimes its appropriately filled
#I am getting nosuchelement exception, elementnotinteractable exception dunno what is wrong

next1 = driver.find_element(By.LINK_TEXT, 'Next')
next1.click()

d = {}
for i in range(2,11):
    
    xpath = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/div/div/div[2]/div[2]/div[1]/p/b'.format(i))
    d['word{0}'.format(i)] = xpath.text  
    c_word = d['word{0}'.format(i)]
    print('The word is:' + c_word)
    
    option1 = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/div/div/div[2]/div[2]/div[2]/div[1]/a[1]'.format(i))
    option2 = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/div/div/div[2]/div[2]/div[2]/div[1]/a[2]'.format(i))
    option3 = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/div/div/div[2]/div[2]/div[2]/div[1]/a[3]'.format(i))
    option4 = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/div/div/div[2]/div[2]/div[2]/div[1]/a[4]'.format(i))    
    
    tss = "https://www.thesaurus.com/browse/" + c_word
    setofsyns = set()
    reqs = requests.get(tss)
    soup = BeautifulSoup(reqs.text, 'lxml')
    for tag in soup.find_all('div', {'data-testid': 'word-grid-container'}):
        for li in tag.find_all('li'):
            setofsyns.add(li.text.strip()) #strip method because it was having whitespace at the end
    print('The set of synonyms is:', setofsyns)
    
    driver.implicitly_wait(10)
    setofoptions = {option1.text, option2.text, option3.text, option4.text}
    print ('The set of options is:', setofoptions, '\n')

    intersection = setofsyns.intersection(setofoptions)
    ans = ''.join(str(e) for e in intersection) #because simply using str function retained the curly brackets of the set causing an error

    if len(intersection) == 1:
        ansbutton = driver.find_element(By.LINK_TEXT, ans)
        driver.implicitly_wait(8)
        ansbutton.click()
    else:
        diffwords += ' '+c_word
        rand_ans = str(random.choice(tuple(setofoptions)))
        driver.implicitly_wait(8)
        rand_ansbutton = driver.find_element(By.LINK_TEXT, rand_ans)
        rand_ansbutton.click()        
    try:
        nextQ = driver.find_element(By.LINK_TEXT, 'Next')
        nextQ.click()    
    except:
        Results = driver.find_element(By.LINK_TEXT, 'Results')   
        Results.click()
    
Score = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[7]/div/div/div/div/div[1]/div[1]/div/div/div/p[1]')    
print('The dictionary words is:', d, '\n')
print('The Total Score out of 4200 is:', Score.text)

Data = [Date, Time, Score.text, diffwords]

with open('AutoMerriamData.csv', 'a') as f: #adding "'newline = ''" doesn't work, empty row still there
    writer = csv.writer(f, delimiter = ' ')
    writer.writerow(Data)

print(rand_ans)

button = driver.find_element(By.LINK_TEXT, 'START THE QUIZ')
button.click()

tss = "https://www.merriam-webster.com/word-games/vocabulary-quiz"
setofoptions = set()
reqs = requests.get(tss)
soup = BeautifulSoup(reqs.text, 'lxml')
for tag in soup.find_all('div', {'class': 'question-gstage__choices fade-in'}):
    for li in tag.find_all('li'):
        setofoptions.add(li.text.strip()) #strip method because it was having whitespace at the end
print('The set of soptions is:', setofoptions)


d = {}
for i in range(1,11):
    
    xpath = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/div[{0}]/div/div/div[2]/div[2]/div[1]/p/b'.format(i))
    d['word{0}'.format(i)] = xpath.text  
    c_word = d['word{0}'.format(i)]
    print('The word is:' + c_word)
   
    
    option1 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/div[{0}]/div/div/div[2]/div[2]/div[2]/div[1]/a[1]'.format(i))
    option2 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/div[{0}]/div/div/div[2]/div[2]/div[2]/div[1]/a[2]'.format(i))
    option3 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/div[{0}]/div/div/div[2]/div[2]/div[2]/div[1]/a[3]'.format(i))
    option4 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/div[{0}]/div/div/div[2]/div[2]/div[2]/div[1]/a[4]'.format(i))    
    
    setofoptions  = {option1.text, option2.text, option3.text, option4.text}
    print ('The set of options is:', setofoptions)
    
    tss = "https://www.thesaurus.com/browse/" + c_word
    setofsyns = set()
    reqs = requests.get(tss)
    soup = BeautifulSoup(reqs.text, 'lxml')
    for tag in soup.find_all('div', {'data-testid': 'word-grid-container'}):
        for li in tag.find_all('li'):
            setofsyns.add(li.text.strip()) #strip method because it was having whitespace at the end
    print('The set of synonyms is:', setofsyns)

    intersection = setofsyns.intersection(setofoptions)
    ans = ''.join(str(e) for e in intersection) #because simply using str function retained the curly brackets of the set causing an error

    if len(intersection) == 1:
        ansbutton = driver.find_element(By.LINK_TEXT, ans)
        driver.implicitly_wait(2)
        ansbutton.click()
    else:
        rand_ans = str(random.choice(tuple(setofoptions)))
        driver.implicitly_wait(10)
        rand_ansbutton = driver.find_element(By.LINK_TEXT, rand_ans)
        rand_ansbutton.click()        
    try:
        nextQ = driver.find_element(By.LINK_TEXT, 'Next')
        nextQ.click()    
    except:
        Results = driver.find_element(By.LINK_TEXT, 'Results')   
        Results.click()
    
Score = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[7]/div/div/div/div/div[1]/div[1]/div/div/div/p[1]')    
print('The dictionary words is:', d)
print(Score.text)

