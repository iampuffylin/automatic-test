from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from seleniumwire import webdriver
from time import sleep
import codecs
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pathlib
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading
import numpy as np
import matplotlib.pyplot as plt
import requests
import csv
import config
import random


path = pathlib.Path(__file__).parent.resolve()
browser_list = [{'name': 'chrome', 'driver': 'chromedriver'}, {'name': 'firefox', 'driver': 'geckodriver'}]
environment_list = [{'name': 'TEST', 'url': 'https://XXX'}, {'name': 'QA', 'url': 'https://XXXX'}, {'name': 'PROD', 'url': 'https://www.motom.me'}]
login_list = [{'name': 'facebook'}, {'name': 'google'}, {'name': 'email'}]
setting_a = {'browser_type': 0, 'environment_type': 0, 'login_type': 1, 'userid': 'XXX@gmail.com', 'password': '***'}
setting_b = {'browser_type': 0, 'environment_type': 0, 'login_type': 1, 'userid': 'XXX@gmail.com', 'password': '***'}
setting_c = {'browser_type': 0, 'environment_type': 1, 'login_type': 2, 'userid': 'XXX@gmail.com', 'password': '***'}
setting_d = {'browser_type': 1, 'environment_type': 0, 'login_type': 0, 'userid': 'XXX@gmail.com', 'password': '***'}

setting_1 = {'browser_type': 0, 'environment_type': 0, 'login_type': 2, 'userid': 'XXX@gmail.com', 'password': '***'}
user_profile_pages = ['http://www.motom.me/@aestheticsthingz4/', 'https://www.motom.me/@k4teturner/',
                      'https://www.motom.me/@fitsandbits/', 'https://www.motom.me/@jennyxngyn/']
home_settings = [ {'browser_type': 0, 'environment_type': 0, 'login_type': 2, 'userid': 'XXX@gmail.com', 'password': '***'},
                  {'browser_type': 0, 'environment_type': 0, 'login_type': 2, 'userid': 'XXX@gmail.com', 'password': '***'},
                  {'browser_type': 0, 'environment_type': 0, 'login_type': 2, 'userid': 'XXX@gmail.com', 'password': '***'},
                  {'browser_type': 0, 'environment_type': 0, 'login_type': 2, 'userid': 'XXX@gmail.com', 'password': '***'},
                  {'browser_type': 0, 'environment_type': 0, 'login_type': 2, 'userid': 'XXX@gmail.com', 'password': '***'},
                  {'browser_type': 0, 'environment_type': 0, 'login_type': 2, 'userid': 'XXX@gmail.com', 'password': '***'},
                  {'browser_type': 0, 'environment_type': 0, 'login_type': 2, 'userid': 'XXX@gmail.com', 'password': '***'} ]
# quit_driver = None
time_cost = []
slaves = config.slaves
master = config.master

def main():
    # doLikeboardLoop()
    # doHomeLoop()
    doUserProfileLoop2()
    # doThread()
    print(time_cost)
    # logTimeCostCSV(time_cost)
    # logTimeCostAPI(time_cost)
    # drawChart()

def doLikeboardLoop(): #loop likeboard page
    wait = random.randrange(11)
    sleep(wait)
    time_cost.append([])
    timeout = time.time() + 20*1
    while True:
        # print(timeout - time.time())
        ScriptLikeboardPage(setting_c, 1)
        if time.time() > timeout:
            break

def doHomeLoop():
    begin_time = time.time()
    driver = openBrowser(home_settings[0]['browser_type'], 1)
    wait = random.randrange(11)
    sleep(wait)
    time_cost.append([])
    timeout = 60*3
    setting_index = 0
    total_cost = 0
    while True:
        # print(timeout - total_cost)
        cost = ScriptLoginHome(driver, home_settings[setting_index], 1)
        total_cost = total_cost + cost
        setting_index = 0 if setting_index == len(home_settings) - 1 else setting_index + 1
        if total_cost > timeout:
            if driver:
                driver.quit()
            break
    print('total cost:' + str(time.time() - begin_time))

def doUserProfileLoop(): #loop every user_profile_pages
    wait = random.randrange(11)
    sleep(wait)
    time_cost.append([])
    timeout = time.time() + 60*10
    while True:
        print(timeout - time.time())
        ScriptUserProfilePages(setting_c, 1)
        if time.time() > timeout:
            break

def doUserProfileLoop2(): #loop every user profile
    driver = openBrowser(setting_c['browser_type'], 1)
    wait = random.randrange(11)
    sleep(wait)
    time_cost.append([])
    timeout = time.time() + 20*1
    url_index = 0
    while True:
        # print(timeout - time.time())
        ScriptUserProfilePages2(driver, setting_c, 1, url_index)
        url_index = 0 if url_index == len(user_profile_pages) - 1 else url_index + 1
        if time.time() > timeout:
            if driver:
                driver.quit()
            break

def doThread():
    t_list = []
    for i in range(1):
        time_cost.append([])
        t_list.append(threading.Thread(target=ScriptUserProfilePages, args=(setting_c, i + 1)))
    for t in t_list:
        t.start()
    for t in t_list:
        t.join()

def drawChart():
    # time_cost = [[10.474244832992554, 6.553020000457764, 7.974948167800903, 6.62608003616333, 3.783029079437256], [10.218952178955078, 5.943846225738525, 7.5698888301849365, 6.300737142562866, 3.8339157104492188]]
    years = [1,2,3,4,5]
    a = time_cost[0]
    b = time_cost[1]

    lines = plt.plot(years,a,years,b)
    
    plt.xticks(years)
    plt.plot(years,a, color=(255/255,100/255,100/255), label='First Driver')
    plt.plot(years,b, '--', color=(100/255,100/255,255/255), label='Second Driver')
    plt.title("Target User Profile Time Cost") # title
    plt.ylabel("Cost Time") # y label
    plt.xlabel("Target User") # x label
    plt.setp(lines,marker = "o") 
    plt.legend()
    plt.grid(True)
    plt.show()

def avgCostbyCSV():
    doc_name = 'api_csv'
    time_cost = []
    with open(os.path.join(path, 'test_log/', doc_name + '.csv'), newline='') as csvfile:
        rows = csv.reader(csvfile)
        avglist = list()
        for row in rows:
            total = 0
            for r in row:
                total = total + float(r)
            avg = total / len(row)
            avglist.append(avg)
        print(avglist)
        totalAvg = 0
        for a in avglist:
            totalAvg = totalAvg + float(a)
        print('*** Average of visit every User Profile page cost: ' + str(totalAvg / len(avglist)) + ' seconds ***')

def drawChartSample():
    years = [1950,1960,1965,1970,1975,1980,
            1985,1990,1995,2000,2005,
            2010,2015]
    pops = [2.5,2.7,3,3.3,3.6,4.0,
            4.4,4.8,5.3,6.1,6.5,6.9,7.3]
    deaths = [1.2,1.7,1.8,2.2,2.5,2.7,2.9,3,3.1,3.2,3.5,3.6,4]

    lines = plt.plot(years,pops,years,deaths)
    
    plt.plot(years,pops, color=(255/255,100/255,100/255))
    plt.plot(years,deaths, '--', color=(100/255,100/255,255/255))
    plt.title("Population Growth") # title
    plt.ylabel("Population in billions") # y label
    plt.xlabel("Population growth by year") # x label
    plt.setp(lines,marker = "o") 
    plt.grid(True)
    plt.show()

def performanceSample(setting_1):
    hyperlink = "https://www.qa.motom.me/"
    # driver = webdriver.Chrome()
    driver = openBrowser(setting_1['browser_type'])
    driver.get(hyperlink)
    
    ''' Use Navigation Timing  API to calculate the timings that matter the most '''   
    
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    
    ''' Calculate the performance'''
    backendPerformance_calc = responseStart - navigationStart
    frontendPerformance_calc = domComplete - responseStart
    
    print("Back End: %s" % backendPerformance_calc)
    print("Front End: %s" % frontendPerformance_calc)
    
    driver.quit()


def ScriptLikeboardPage(setting_1, index):
    try:
        driver = openBrowser(setting_c['browser_type'], 1)
        start_time = time.time()
        logMsg('ScriptLikeboardPages Start】', index, setting_1)
        logStatus('Start', True, 'OK', index)
        driver.get('https://www.stress.motom.me/home/likeboards')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'hero-content')))
        logStatus('Loading', True, 'OK', index)
        i = 0
        while i < 10:
            try:
                driver.find_element(By.CLASS_NAME, 'loading')
                i = i + 1
                time.sleep(1)
            except:
                logStatus('Loaded', True, 'OK', index)
                break

        cost = time.time() - start_time
        # time_cost[index-1].append('"' + time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(start_time)) + ',' + str(cost) + '"')
        time_cost[index-1].append(cost)
        logStatus('Done', True, 'OK', index)
        logMsg('***** cost: ' + str(cost) + ' seconds *****', index)
        logMsg('ScriptLikeboardPages End】', index)
        # driver.quit()
    except Exception as e:
        print(str(e))
        logStatus('ScriptLikeboardPages End】', False, str(e), index)
        return time.time() - start_time
    finally:
        if driver:
            driver.quit()


def ScriptLoginHome(driver, setting_1, index):
    try:
        logMsg('【ScriptLoginHome Start】', index, setting_1)
        logStatus('Start', True, 'OK', index)
        goLogin(driver, setting_1, 1)
        start_time = time.time()
        driver.get(environment_list[setting_1['environment_type']]['url'])
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'trending-slider-list')))
        logStatus('Loading', True, 'OK', index)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]//div[@class="list home-list"]/div[@class="post-list"]//div[@class="post-wrap"]/article/footer')))
        i = 0
        while i < 20:
            try:
                driver.find_element(By.CLASS_NAME, 'loading')
                i = i + 1
                time.sleep(1)
            except:
                logStatus('Loaded', True, 'OK', index)
                break

        cost = time.time() - start_time
        # time_cost[index-1].append('"' + time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(start_time)) + ',' + str(cost) + '"')
        time_cost[index-1].append(cost)
        driver.get(environment_list[setting_1['environment_type']]['url'] + '/logout')
        logStatus('Logout', True, 'OK', index)
        logStatus('Done', True, 'OK', index)
        logMsg('***** Home Page costs: ' + str(cost) + ' seconds *****', index)
        logMsg('【ScriptLoginHome End】', index)
        return cost
        # driver.quit()
    except Exception as e:
        print(str(e))
        logStatus('【ScriptLoginHome End】', False, str(e), index)
        return time.time() - start_time


def ScriptUserProfilePages(setting_1, index):
    try:
        driver = openBrowser(setting_1['browser_type'], index)

        for url in user_profile_pages:
            start_time = time.time()
            logMsg('【ScriptUserProfilePages Start】', index, setting_1)
            logMsg('URL:' + url, index)
            
            if not driver == None:
                logStatus('Start', True, 'OK', index)
                driver.get(url)
                el = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'loading')))
                logStatus('Loading', True, 'OK', index)
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="motom-post-list"]/div[@class="list"]/div[@class="post-wrap"]/article/footer')))
                i = 0
                while i < 20:
                    try:
                        el = driver.find_element(By.CLASS_NAME, 'loading')
                        i = i + 1
                        time.sleep(1)
                    except:
                        logStatus('Done', True, 'OK', index)
                        break

            end_time = time.time()
            cost = end_time - start_time
            # time_cost[index-1].append('"' + time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(start_time)) + ',' + str(cost) + '"')
            time_cost[index-1].append(cost)
            logMsg('***** cost: ' + str(cost) + ' seconds *****', index)
            logMsg('【ScriptUserProfilePages End】', index)
        # driver.quit()
    except Exception as e:
        print(str(e))
        logStatus('【ScriptUserProfilePages End】', False, str(e), index)
    finally:
        if driver:
            driver.quit()


def ScriptUserProfilePages2(driver, setting_1, index, url_index):
    try:
        start_time = time.time()
        logMsg('【ScriptUserProfilePages Start】', index, setting_1)
        logMsg('URL:' + user_profile_pages[url_index], index)
        
        if not driver == None:
            logStatus('Start', True, 'OK', index)
            driver.get(user_profile_pages[url_index])
            el = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'loading')))
            logStatus('Loading', True, 'OK', index)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="motom-post-list"]/div[@class="list"]/div[@class="post-wrap"]/article/footer')))
            i = 0
            while i < 20:
                try:
                    el = driver.find_element(By.CLASS_NAME, 'loading')
                    i = i + 1
                    time.sleep(1)
                except:
                    logStatus('Done', True, 'OK', index)
                    break

        end_time = time.time()
        cost = end_time - start_time
        # time_cost[index-1].append('"' + time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(start_time)) + ',' + str(cost) + '"')
        time_cost[index-1].append(cost)
        logMsg('***** cost: ' + str(cost) + ' seconds *****', index)
        logMsg('【ScriptUserProfilePages End】', index)
        # driver.quit()
    except Exception as e:
        print(str(e))
        logStatus('【ScriptUserProfilePages End】', False, str(e), index)


def ScriptInviteRegister(setting_1, setting_2):
    try:
        logMsg('【ScriptInviteRegister Start】', setting_1, setting_2)
        driver = openBrowser(setting_1['browser_type'])
        if not driver == None:
            goLogin(driver, setting_1)
            invite_url = invite(driver, setting_1)
            driver2 = openBrowser(setting_2['browser_type'])
            if not driver2 == None:
                register(driver2, setting_2, invite_url)
        logMsg('【ScriptInviteRegister End】')
    except Exception as e:
        logStatus('【ScriptInviteRegister End】', False, str(e))
    finally:
        if not quit_driver == None:
            sleep(quit_driver)
            driver.quit()

def ScriptRegister(setting_1):
    try:
        logMsg('【ScriptRegister Start】', setting_1)
        driver = openBrowser(setting_1['browser_type'])
        if not driver == None:
            register(driver, setting_1, None)
        logMsg('【ScriptRegister End】')
    except Exception as e:
        logStatus('【ScriptRegister End】', False, str(e))
    finally:
        if not quit_driver == None:
            sleep(quit_driver)
            driver.quit()

def ScriptLoginLogout(setting_1, index):
    try:
        logMsg('【ScriptLoginLogout】 - Start', index, setting_1)
        driver = openBrowser(setting_1['browser_type'])
        if not driver == None:
            start_time = time.time()
            goLogin(driver, setting_1, index)
            # sleep(5)
            logout(driver, setting_1, index)
        end_time = time.time()
        print('***** cost: ' + str(end_time - start_time) + ' seconds *****', index)
        logMsg('***** cost: ' + str(end_time - start_time) + ' seconds *****', index)
        logMsg('【ScriptLoginLogout】 - End', index)
        driver.quit()
    except Exception as e:
        logStatus('【ScriptLoginLogout】 - End', False, str(e), index)
    finally:
        if not quit_driver == None:
            sleep(quit_driver)
            driver.quit()

def ScriptCreateDeletePost(setting_1, index):
    try:
        logMsg('【ScriptCreateDeletePost】 - Start', index, setting_1)
        driver = openBrowser(setting_1['browser_type'])
        sleep(1)
        driver.maximize_window()
        if not driver == None:
            goLogin(driver, setting_1, index)
            createPost(driver, setting_1, 4, 0, index) #post_type:0-ins/1-yt;tag_type:None/0-motom/1-web
            deletePost(driver, setting_1, index)
        logMsg('【ScriptCreateDeletePost】 - End', index)
        driver.quit()
    except Exception as e:
        logStatus('【ScriptCreateDeletePost】 - End', False, str(e), index)
    finally:
        if not quit_driver == None:
            sleep(quit_driver)
            driver.quit()

def ScriptLikeBoard(setting_1):
    # access productdetails/user post
    # click like
    # show login popup
    # access productdetails/user post
    # click like
    # go to likeborad
    # unlike post/product
    try:
        logMsg('【ScriptLikeBoard Start】', setting_1)
        driver = openBrowser(setting_1['browser_type'])
        if not driver == None:
            likePost(driver, setting_1)

            # goLogin(driver, setting_1)
            # if countLikeBoardItems(driver, setting_1) > 0:
            #     logStatus('LikePost', True, 'OK')

        logMsg('【ScriptLikeBoard End】')
    except Exception as e:
        logStatus('【ScriptLikeBoard End】', False, str(e))
    finally:
        if not quit_driver == None:
            sleep(quit_driver)
            driver.quit()

def openBrowser(browser_type, index):
    # check browser
    try:
        if browser_type == 0:
            o = webdriver.ChromeOptions()
            # prefs = {
            #     'profile.default_content_setting_values': {
            #         'notifications': 2
            #     }
            # }
            # o.add_experimental_option('prefs', prefs)
            # o.add_experimental_option('detach', True)
            # o.add_argument('--headless')
            o.add_argument('--disable-gpu')
            o.add_argument('ignore-certificate-errors')
            o.add_experimental_option("excludeSwitches", ['enable-automation'])
            o.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
            o.add_argument("--remote-debugging-port=9222")
            s = Service(os.path.join(path, browser_list[browser_type]['driver']))
            driver = webdriver.Chrome(service=s,options=o)
        else:
            # driver = webdriver.Firefox(executable_path=path + browser_list[browser_type]['driver'])
            s = Service(os.path.join(path, browser_list[browser_type]['driver']))
            driver = webdriver.Firefox(service=s)
        return driver
    except Exception as e:
        logStatus('Open browser(' + browser_list[browser_type]['name'] + ')', False, str(e), index)
        return None

def goLogin(driver, setting, index):
    try:
        driver.get(environment_list[setting['environment_type']]['url'])
        # sleep(3)
        # driver.find_element(By.CLASS_NAME, 'login-link').click()
        # driver.find_element(By.XPATH, '//span[contains(text(), "Log In")]').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Log In")]'))).click()
        # sleep(1)
        login(driver, setting, index)
    except Exception as e:
        logStatus('Login', False, str(e), index)

def login(driver, setting, index):
    try:
        # check log in by
        if setting['login_type'] == 0: #Facebook login
            driver.find_element(By.CLASS_NAME, 'btns').find_element(By.CLASS_NAME, 'facebook').click()
            sleep(3)
            driver.find_element(By.ID, 'email').send_keys(setting['userid'])
            driver.find_element(By.ID, 'pass').send_keys(setting['password'])
            driver.find_element(By.ID, 'loginbutton').click()
        elif setting['login_type'] == 1: #Google login
            driver.find_element(By.CLASS_NAME, 'btns').find_element(By.CLASS_NAME, 'google').click()
            sleep(3)
            driver.find_element(By.ID, 'identifierId').send_keys(setting['userid'])
            driver.find_element(By.CLASS_NAME, 'VfPpkd-vQzf8d').click()
            sleep(3)
            driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(setting['password'])
            driver.find_element(By.CLASS_NAME, 'VfPpkd-vQzf8d').click()
        elif setting['login_type'] == 2: #Email login
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Continue with email")]'))).click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'js-login-email'))).send_keys(setting['userid'])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'js-login-password'))).send_keys(setting['password'])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Log In")]'))).click()
        # click Got it!
        # sleep(3)
        # driver.find_element(By.XPATH, '//span[contains(text(), "Got it!")]').click()
        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Got it!")]'))).click()
        # sleep(1)
        # if isLogin(driver):
        logStatus('Login', True, 'OK', index)
    except Exception as e:
        logStatus('Login', False, str(e), index)

def logout(driver, setting, index):
    try:
        if isLogin(driver):
            driver.get(environment_list[setting['environment_type']]['url'] + '/logout')
        if isLogout(driver):
            logStatus('Logout', True, 'OK', index)
    except Exception as e:
        logStatus('Logout', False, str(e), index)

def invite(driver, setting):
    # return 'http://www.qa.motom.me/?referral_id=6A21LzQu6&client_group_token=a5afde001ac6e9c2bcf283e9b40c875a'
    try:
        sleep(1)
        # driver.get(environment_list[setting['environment_type']]['url'] + '/me')
        driver.find_element(By.CLASS_NAME, 'login-register').click()
        sleep(1)
        driver.find_element(By.XPATH, '//span[contains(text(), " Invite")]').click()
        invite_url = driver.find_element(By.TAG_NAME, 'input').get_attribute('value')
        if not invite_url == None:
            logStatus('Invite(invite_url:' + invite_url + ')', True, 'OK')
        return invite_url
    except Exception as e:
        logStatus('Invite', False, str(e))
        return None

def register(driver, setting, invite_url):
    try:
        if not invite_url == None:
            driver.get(invite_url)
            sleep(3)
        else:
            driver.get(environment_list[setting['environment_type']]['url'])
            sleep(3)
            driver.find_element(By.CLASS_NAME, 'login-link').click()
            sleep(1)
        # check log in by
        if setting['login_type'] == 0:
            driver.find_element(By.CLASS_NAME, 'btns').find_element(By.CLASS_NAME, 'facebook').click()
            sleep(3)
            driver.find_element(By.ID, 'email').send_keys(setting['userid'])
            driver.find_element(By.ID, 'pass').send_keys(setting['password'])
            driver.find_element(By.ID, 'loginbutton').click()
        elif setting['login_type'] == 1:
            driver.find_element(By.CLASS_NAME, 'btns').find_element(By.CLASS_NAME, 'google').click()
            sleep(3)
            driver.find_element(By.ID, 'identifierId').send_keys(setting['userid'])
            driver.find_element(By.CLASS_NAME, 'VfPpkd-vQzf8d').click()
            sleep(3)
            driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(setting['password'])
            driver.find_element(By.CLASS_NAME, 'VfPpkd-vQzf8d').click()
        # step 1
        sleep(5)
        driver.find_element(By.XPATH, '//span[contains(text(), "Skip")]').click()
        # step 2
        if driver.find_element(By.XPATH, '//input[@type="email"]').get_attribute('value') == setting['userid']:
            driver.find_element(By.XPATH, '//span[contains(text(), "Next")]').click()
        else:
            logStatus('Register step2', False, 'input userid is not match')
        # step 3
        sleep(2)
        driver.find_element(By.XPATH, '//input[@placeholder="First name"]').send_keys('Test')
        driver.find_element(By.XPATH, '//input[@placeholder="Last name"]').send_keys('Motom')
        driver.find_element(By.XPATH, '//span[contains(text(), "Non-Binary / Other")]').click()
        driver.find_element(By.XPATH, '//input[@placeholder="Zip code"]').send_keys('10000')
        driver.find_element(By.XPATH, '//span[contains(text(), "Submit")]').click()
        # jump
        sleep(2)
        driver.find_element(By.XPATH, '//span[contains(text(), "Jump right in")]').click()
        # click Got it!
        sleep(2)
        driver.find_element(By.XPATH, '//span[contains(text(), "Got it!")]').click()
        sleep(1)
        # Maybe later
        sleep(2)
        driver.find_element(By.XPATH, '//span[contains(text(), "Maybe later")]').click()
        sleep(1)
        if isLogin(driver):
            logStatus('Register', True, 'OK')
    except Exception as e:
        logStatus('After login can\'t find Maybe later', False, str(e))

def createPost(driver, setting, post_type, tag_type, index):
    try:
        driver.find_element(By.CLASS_NAME, 'create-button').click()
        sleep(1)
        driver.find_element(By.XPATH, '//textarea[@placeholder="Add a caption here…"]').send_keys('test')
        if post_type == 0:
            driver.find_element(By.CLASS_NAME, 'type-instagram').click()
            driver.find_element(By.XPATH, '//a[contains(text(), "Link from Instagram")]').click()
            element = driver.find_element(By.XPATH, '//input[@placeholder="https://www.instagram.com/..."]')
            element.send_keys('https://www.instagram.com/tv/CVem2UFlUX_/')
            element.send_keys(Keys.ENTER)
        elif post_type == 1:
            driver.find_element(By.CLASS_NAME, 'type-video').click()
            driver.find_element(By.XPATH, '//a[contains(text(), "Link from YouTube")]').click()
            element = driver.find_element(By.XPATH, '//input[@placeholder="https://www.youtube.com/..."]')
            element.send_keys('https://www.youtube.com/watch?v=3OFRFYtAuNM&list=WL&index=1')
            element.send_keys(Keys.ENTER)
        elif post_type == 2:
            driver.find_element(By.CLASS_NAME, 'type-tiktok').click()
            driver.find_element(By.XPATH, '//a[contains(text(), "Link from TikTok")]').click()
            element = driver.find_element(By.XPATH, '//input[@placeholder="https://www.tiktok.com/..."]')
            element.send_keys('https://www.tiktok.com/@blackpink_blinke/video/7012194291133074689')
            element.send_keys(Keys.ENTER)
        elif post_type == 3:
            driver.find_element(By.CLASS_NAME, 'type-image').click()
            driver.find_element(By.CLASS_NAME, 'wrapper-holder').find_element(By.XPATH, '//input[@type="file"]').send_keys(os.path.join(path, 'test_picture.jpeg'))
            sleep(1)
            if not tag_type == None:
                driver.find_element(By.XPATH, '//span[contains(text(), "Next")]').click()
                sleep(1)
                element = driver.find_element(By.CLASS_NAME, 'image-item')
                action_chains = ActionChains(driver)
                action_chains.move_to_element_with_offset(element, 200, 200).perform()
                action_chains.click().perform()
        elif post_type == 4:
            driver.find_element(By.CLASS_NAME, 'type-thisorthat').click()
            driver.find_element(By.CLASS_NAME, 'wrapper').find_elements(By.XPATH, '//input[@type="file"]')[0].send_keys(os.path.join(path, 'test_picture.jpeg'))
            sleep(1)
            driver.find_element(By.CLASS_NAME, 'wrapper').find_elements(By.XPATH, '//input[@type="file"]')[1].send_keys(os.path.join(path, 'test_picture_2.jpeg'))
            sleep(1)
            if not tag_type == None:
                driver.find_element(By.XPATH, '//span[contains(text(), "Next")]').click()
                sleep(1)
                element = driver.find_element(By.CLASS_NAME, 'tot-item')
                action_chains = ActionChains(driver)
                action_chains.move_to_element_with_offset(element, 200, 200).perform()
                action_chains.click().perform()
        sleep(3)
        if not tag_type == None:
            sleep(1)
            if post_type == 3 or post_type == 4:
                driver.find_element(By.XPATH, '//span[contains(text(), "Add Product")]').click()
            else:
                driver.find_element(By.CLASS_NAME, 'goto-tag').click()
            sleep(3)
            tagProduct(driver, setting, tag_type, index)
            if post_type == 3 or post_type == 4:
                driver.find_element(By.XPATH, '//span[contains(text(), "Save")]').click()
        driver.find_element(By.XPATH, '//span[contains(text(), "Post")]').click()
        sleep(5)
        logStatus('CreatePost', True, 'OK', index)
    except Exception as e:
        logStatus('CreatePost', False, str(e), index)

def tagProduct(driver, setting, tag_type, index):
    try:
        if tag_type == 0:
            driver.find_element(By.CLASS_NAME, 'tag-products--list').find_element(By.TAG_NAME, 'li').click()
            driver.find_element(By.XPATH, '//span[contains(text(), "Tag It")]').click()
            # sleep(1)
            # driver.find_element(By.XPATH, '//span[contains(text(), "Look-alike")]').click()
        else:
            driver.find_element(By.CLASS_NAME, 'tag-menu').find_element(By.XPATH, '//a[contains(text(), "Web")]').click()
            driver.find_element(By.XPATH, '//input[@placeholder="Paste URL for Product here"]').send_keys('https://www.gap.tw/pdp/000754605/1_000754605_SP09-23437')
            driver.find_element(By.XPATH, '//span[contains(text(), "Next")]').click()
            sleep(2)
            driver.find_element(By.CLASS_NAME, 'select-image').find_element(By.TAG_NAME, 'li').click()
            driver.find_element(By.XPATH, '//span[contains(text(), "Next")]').click()
            # Enter and edit product details
            sleep(1)
            driver.find_element(By.ID, 'product_name').send_keys('T-shirt')
            driver.find_element(By.ID, 'brand_name').send_keys('Gap')
            driver.find_element(By.ID, 'price').send_keys('50')
            driver.find_element(By.XPATH, '//span[contains(text(), "Done")]').click()
            # sleep(1)
            # driver.find_element(By.XPATH, '//span[contains(text(), "Look-alike")]').click()
        sleep(3)
    except Exception as e:
        logStatus('TagProduct', False, str(e), index)

def deletePost(driver, setting, index):
    try:
        driver.get(environment_list[setting['environment_type']]['url'] + '/me')
        sleep(2)
        driver.execute_script("window.scrollBy(0, 400);")
        sleep(2)
        driver.find_element(By.CLASS_NAME, 'list').find_element(By.CLASS_NAME, 'post-wrap').find_element(By.CLASS_NAME, 'new-post--edit-post').click()
        sleep(2)
        driver.find_element(By.XPATH, '//span[contains(text(), "Delete")]').click()
        sleep(2)
        driver.find_element(By.XPATH, '//span[contains(text(), "Yes")]').click()
        logStatus('DeletePost', True, 'OK', index)
        sleep(2)
    except Exception as e:
        logStatus('DeletePost', False, str(e), index)

def likePost(driver, setting):
    try:
        driver.get(environment_list[setting['environment_type']]['url'] + '/user/2616/posts')
        sleep(3)
        is_login = isLogin(driver)
        element = driver.find_element(By.CLASS_NAME, 'post-wrap')
        driver.execute_script("arguments[0].scrollIntoView();", element)
        element.find_element(By.CLASS_NAME, 'post--footer').find_element(By.TAG_NAME, 'li').click()
        if not is_login:
            login(driver, setting)
            element = driver.find_element(By.CLASS_NAME, 'post-wrap')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.find_element(By.CLASS_NAME, 'post--footer').find_element(By.TAG_NAME, 'li').click()
        sleep(5)
        if countLikeBoardItems(driver, setting) > 0:
            logStatus('LikePost', True, 'OK')
    except Exception as e:
        logStatus('LikePost', False, str(e))

def countLikeBoardItems(driver, setting):
    try:
        driver.get(environment_list[setting['environment_type']]['url'] + '/me/likeboards')
        sleep(5)
        info = driver.find_element(By.CLASS_NAME, 'likeboard-item').find_element(By.CLASS_NAME, 'info').find_element(By.TAG_NAME, 'p').text
        return int(info[0:info.index(' items')])
    except Exception as e:
        logStatus('LikePost', False, str(e))

def logStatus(do, status, message, index = None):
    current_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    status_msg = 'SUCCESS' if status == True else 'FAILURE'
    doc_name = 'test_log_' + str(index) if index else 'test_log'
    with open(os.path.join(path, 'test_log/', doc_name + '.txt'), 'a') as f:
        f.write(current_time + '\t' + do + '\t' + status_msg + '\t' + message + '\n')

def logMsg(message, index = None, setting_1 = None, setting_2 = None):
    current_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    if setting_1 is not None and setting_2 is not None:
        message = (message + '\n'
        + current_time + '\t' + 'setting:' + environment_list[setting_1['environment_type']]['name'] + ';' + login_list[setting_1['login_type']]['name'] + ';' + setting_1['userid']
        + ';userid2:' + setting_2['userid'] + '')
    elif setting_1 is not None:
        message = (message + '\n'
        + current_time + '\t' + 'setting:' + environment_list[setting_1['environment_type']]['name'] + ';' + login_list[setting_1['login_type']]['name'] + ';' + setting_1['userid'] + '')
    else:
        message + '\t' + current_time
    doc_name = 'test_log_' + str(index) if index else 'test_log'
    with open(os.path.join(path, 'test_log/', doc_name + '.txt'), 'a') as f:
        f.write(message + '\n')

def logTimeCostCSV(arr_time):
    time_cost = ''
    for a in arr_time:
        for t in a:
            time_cost = time_cost + str(t) + ','
    if time_cost != '':
        time_cost = time_cost[:-1]
    doc_name = 'test_csv'
    with open(os.path.join(path, 'test_log/', doc_name + '.csv'), 'a') as f:
        f.write(time_cost + '\n')

def logTimeCostAPI(arr_time):
    time_cost = ''
    for a in arr_time:
        for t in a:
            time_cost = time_cost + str(t) + ','
    if time_cost != '':
        time_cost = time_cost[:-1]
    response = requests.post('http://' + master + ':5000/LogData', json = { "time_cost": time_cost })

def isLogin(driver):
    try:
        # driver.find_element(By.CLASS_NAME, 'login-link')
        header = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="right"]/div[1]/div[@class="notification-icon"]')))
        if header:
            return True
        else:
            return False
    except:
        return False

def isLogout(driver):
    try:
        # driver.find_element(By.CLASS_NAME, 'login-link')
        header = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'header-inner')))
        if header.find_element(By.XPATH, '//span[contains(text(), "Log In")]'):
            return True
        else:
            return False
    except:
        return False

if __name__ == '__main__':
    main()
    # logStatus('Test', True, 'OK')