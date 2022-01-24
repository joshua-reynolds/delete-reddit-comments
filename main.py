import os
import urllib.request
import bs4 as bs
import webbrowser
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

"""
delete all those comments that you made throughout the years
"""

#==============
# Functions
#==============

# delete comments function
def find_and_delete_comments():
    
    # track n comments deleted
    comments_deleted = 0
    
    # find comments
    comments = driver.find_elements(By.CLASS_NAME,'Comment')
    
    # loop thru gathered comments
    for c in comments:
        
        # find the buttons of the comment
        more_options = c.find_elements(By.TAG_NAME, 'button')
        
        # if the comment is interactable, otherwise its non-user
        if len(more_options) > 0:

            # click
            more_options[-1].click()
            
            # find the menu div
            menu =  driver.find_element(By.CSS_SELECTOR, "._2uYY-KeuYHKiwl-9aF0UiL.ehsOqYO6dxn_Pf9Dzwu37")
                    
            # find the delete button
            buttons = menu.find_elements(By.CSS_SELECTOR, "._10K5i7NW6qcm-UoCtpB3aK._3LwUIE7yX7CZQKmD2L87vf._2LNy1r5iuFMrf0PLh4UdV-._1oYEKCssGFjqxQ9jJMNj5G")
            
            # click, if the text of the button is 'delete'
            for b in buttons:
                name = b.text
                if name == 'Delete':
                    b.click()
                #else:
                    #print('found {} button'.format(name))
                
             # find the confirm delete button and click  
            confirm_button = driver.find_element(By.CSS_SELECTOR, '._17UyTSs2atqnKg9dIq5ERg.ogOEj4x-0BpDZWeccJwxx._2iuoyPiKHN3kfOoeIQalDT._10BQ7pjWbeYP63SAPNS8Ts.HNozj_dKjQZ59ZsfEegz8._2nelDm85zKKmuD94NequP0')
            confirm_button.click()
            
            # tracking
            print('I deleted a comment...')
            comments_deleted = comments_deleted + 1
              
        #else:
            #print('Skipping non-user comment...')      
        
    print(comments_deleted)
    return comments_deleted


# Wrapper for deleting comments
def delete_comments_wrapper(mode=0, n=1):
    
    # mode 0 deletes one set of comments
    if mode == 0:
        print('mode is set to 0')
        deleted = 0  
        deleted =  deleted + find_and_delete_comments()
        
    # mode 1 deletes a specifed amount(n) of sets of comments                        
    if mode == 1:
        print('mode is set to 1')
        deleted = 0
        for i in range(0,n):
            print('interation {}'.format(i))
            deleted =  deleted + find_and_delete_comments()
            driver.refresh()

        return deleted        
    
    # mode 2 keeps deleting sets of comments until failure                
    if mode == 2:
        print('mode is set to 2')
        
        status = 0
        deleted = 0
        while status == 0:
            try:
                deleted =  deleted + find_and_delete_comments()
                driver.refresh()
                
            except Exception as e: 
                print(e)
            else:
                status = 1
                print('\nAlert: No more comments or encountered an error')
                
        return deleted       

#$$$$$$$$$$$$$$$$
# MAIN
#$$$$$$$$$$$$$$$$

if __name__ == "__main__":
    
    # Open log file
    log = open('history.log', "a")
    
    # get current time
    now = datetime.now().strftime("%m/%d/%Y %H:%M")  
    log.write('{} Starting script'.format(now))
    log.write('\n')
    
    #=================================
    # Setup Chromedriver
    #=================================
    
    # disable pesky browser notifications
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    
    # get the path of ChromeDriverServer
    s=Service(".\chromedriver.exe")
    
    # create a new Chrome session
    driver = webdriver.Chrome(service=s, options=chrome_options)
    
    # get username and password from text file
    #f=open(r".\login.txt","r")
    f=open("login2.txt", "r")
    lines=f.readlines()
    username=lines[0]
    password=lines[1]
    f.close()
    
    # get the page text
    url = os.path.join('https://www.reddit.com/user', username)
    driver.get(url)
    html = driver.page_source
    soup = bs.BeautifulSoup(html, 'lxml')
    
    
    #================
    # Login
    #===============
    
    # find the login button and click it
    login_button = driver.find_element(By.XPATH,'//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[1]/header/div/div[2]/div/div[1]/a[1]')
    login_button.click()
    driver.implicitly_wait(3) # seconds
    
    # clicking login opens a new frame, switch to it
    driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[3]/div/div/iframe'))

    # find the username and password boxes
    un_field = driver.find_element(By.CSS_SELECTOR,'input[name="username"]')
    pw_field = driver.find_element(By.CSS_SELECTOR,'input[name="password"]')
    
    # login with username and password
    un_field.send_keys(username)
    pw_field.send_keys(password)
    
    # find login button and click
    login_button = driver.find_element(By.XPATH,'/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button')
    login_button.click()    
    
    #===================
    # Delete stuff
    #===================
    
    # get the total comments deleted
    total_deleted = delete_comments_wrapper(0)  
    
    # close browser window
    driver.close()
    
    #======================
    # Logging
    #======================
    
    # logging
    log.write('Number of comments deleted: {}'.format(total_deleted))
    log.write('\n')
    now = datetime.now().strftime("%m/%d/%Y %H:%M") 
    log.write('{} Ending script'.format(now))
    log.write('\n')
    log.write('\n')
    
    # close the log file
    log.close()
    
    


#============
# scrapyard     
#============

## get cookies and store them
#cookies = driver.get_cookies()
#for cookie in cookies:
    #driver.add_cookie(cookie)