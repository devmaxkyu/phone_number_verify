import os
import zipfile
import requests
import sys
import random
from queue import Queue as Queue
from requests.exceptions import RequestException
import time
from os import path
from bs4 import BeautifulSoup
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
from random import randint
import selenium.webdriver.common.alert
import time
from threading import Thread
import pyautogui

# feed thread
# maker thread
 
class proxyChecker(Thread):
   ''' Checks proxies for Elite Status and other confirmations to ensure anonymity '''

   def __init__(self,proxy_check,proxy_return,proxy_ask):
        Thread.__init__(self)
        self.proxy_check = proxy_check	 
        self.proxy_return = proxy_return
        self.used_proxies = []
        self.proxy_ask = proxy_ask

	      
   def run(self):
        print ("A Proxy checker thread is starting") 
		
        while True:
 
        # pause checking proxies if we have one for each thread + a back-up 
         if self.proxy_return.qsize() < 1:
		  
          proxy = self.proxy_check.get()
          if proxy == "kill":
             print ("Proxy checker being killed")
             sys.exit()
          #print ("Got a proxy")	
          try:		  
             s = requests.session()
             r = requests.get('https://www.mytescomobile.com/', proxies=proxy, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                           ' Chrome/67.0.3396.99 Safari/537.36'}, timeout=60)
  					
             print("proxy: " + proxy)

             if "Request unsuccessful" in str(r.content):
               self.proxy_ask.put("no")	  		   
  		   
             if "Request unsuccessful" not in str(r.content):		   
               print("here000")
               proxy.update({'http':'http://'+proxy['https']})
               self.proxy_return.put(proxy)
               self.proxy_ask.put("yep")
               print ("Proxy Checker: Found a good proxy")
          except:
           self.proxy_ask.put("no")	
		   
			
			# sleep to conserve resources		   
         if self.proxy_return.qsize() >= 1:
          time.sleep(5)
		
class proxyWorker(Thread):

   def __init__(self,proxy_ask,proxy_return,proxy_check,proxy_check_return):
        Thread.__init__(self)
        self.proxy_ask = proxy_ask	 
        self.proxy_return = proxy_return
        self.used_proxies = []
        self.good_proxies = []
        self.bad_proxies = []
        self.proxy_check = proxy_check
        self.proxy_check_return = proxy_check_return
        self.done_fig = 0		
	   
        def get_ssl_proxies():
          _proxies = []
          try:
            page_source = requests.get(
                'https://www.sslproxies.org/uk-proxy.html',
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/67.0.3396.99 Safari/537.36'},timeout=20).text
          except requests.exceptions.ConnectionError:
            print('Unable to read free proxies. retrying....')
            time.sleep(.3)
          else:
            soup = BeautifulSoup(page_source, 'lxml')
            for row in soup.find('tbody').find_all('tr'):
                cols = row.find_all('td')
                if cols[4].text == 'elite proxy' and cols[6].text == 'yes':
                    ip = cols[0].text
                    port = cols[1].text
                    _proxies.append({'https': ip + ':' + port})
          return _proxies		   
        maybe = ["217.182.51.231:1080","217.182.120.165:1080","213.86.5.211:8080","217.182.51.224:1080","217.182.120.164:1080","217.182.120.162:1080","51.38.71.101:8080","217.182.120.167:1080","51.144.56.58:8080","217.182.120.161:1080","217.182.120.160:1080","217.182.120.166:1080","195.171.16.146:8080","217.182.51.225:1080","217.182.51.228:1080","217.182.51.229:1080","217.182.51.230:1080","217.182.51.231:8080","217.182.51.226:1080","217.182.51.227:1080","217.182.120.163:1080","103.105.48.16:80","165.22.120.80:8118","178.32.59.233:53281","35.178.70.89:80","51.140.142.44:3128","92.2.46.88:8080","138.68.161.60:3128","2.57.77.96:8085","194.156.124.148:8085","176.58.118.148:8080","91.222.236.157:8085","2.57.76.152:8085","139.59.169.246:3128","2.57.76.110:8085","84.19.38.158:51885","185.14.194.91:8085","164.39.202.75","46.101.26.4:8080","176.58.104.122:8080","198.50.172.162:1080","81.199.32.90:40045","81.22.47.144:8085","212.115.51.153:8085","84.19.38.41:51885","138.68.165.154:8080","195.171.16.146:8080","134.209.16.40:3128","46.231.12.250:30249","195.206.190.165:8080","193.93.192.184:8085","206.189.122.137:8080","2.57.77.102:8085","45.77.227.215:8080","134.209.20.60:8118","91.222.236.130:8085","2.57.76.157:8085","185.251.14.152:8085","51.38.80.159:80","212.115.51.231:8085","212.115.51.218:8085","185.251.14.146:8085","193.93.192.73:8085","68.183.42.181:3128","178.128.173.71:8080","159.65.93.38:3128","79.141.170.56:3128","167.99.194.67:3128","176.35.250.108:8080","212.42.173.71:8080","185.14.194.124:8085","136.244.68.96:8080","185.251.14.56:8085","212.115.51.183:8085","79.110.28.49:8085","188.68.0.131:8085","91.222.239.78:8085","185.251.14.238:8085","79.110.28.108:8085","185.251.14.13:8085","194.156.125.57:8085","2.57.76.35:8085","193.93.192.49:8085","185.251.14.33:8085","79.110.28.103:8085","194.156.125.53:8085","2.57.76.219:8085","209.250.231.124:8080","51.75.170.50:8118","79.110.28.111:8085","185.14.194.62:8085","209.97.183.38:83","206.189.121.203:8118","178.32.59.233","193.93.192.120:8085","2.57.76.90:8085","136.244.67.99:8080","198.50.172.167:1080","95.210.2.206:32407","78.32.35.22:41346","188.68.0.231:8085","185.251.14.23:8085","176.119.141.66:8085","46.101.26.142:3128","104.248.167.58:80","198.50.172.160:1080","95.85.80.94:8085","178.79.138.216:8080","138.68.161.14:8080","95.85.80.20:8085","193.117.138.126:48523","138.68.173.29:8080","209.97.131.118:8080","193.93.192.220:8085","185.251.14.227:8085","91.222.239.111:8085","95.179.202.80:8080","194.156.124.54:8085","95.85.80.174:8085","104.248.167.98:3128","82.197.66.103:443","136.244.70.96:8080","2.57.77.52:8085","136.244.64.142:8080","104.248.166.9:1080","212.115.51.156:8085","167.99.196.162:3128","194.156.125.109:8085","51.38.71.101:8080","198.50.172.166:1080","91.222.239.182:8085","136.244.111.171:8080","185.251.15.12:8085","198.50.172.161:1080","77.68.77.181:80","176.119.141.77:8085","198.50.172.165:1080","134.209.30.57:8118","95.179.230.150:8080","51.68.215.30:3128","134.209.24.240:8118","212.115.51.192:8085","134.209.180.95:80","2.57.76.105:8085","212.71.235.248:8080","2.57.76.244:8085","194.156.125.235:8085","91.222.239.180:8085","194.156.124.131:8085","84.54.58.86:8085","134.209.30.2:3128","35.178.70.89:80","46.32.228.122:3128","79.170.192.142:42642","213.86.5.211:8080","194.156.125.253:8085","178.62.1.143:45798","178.62.47.34:8118","198.50.172.164:1080","104.248.168.101:8080","68.183.42.181:3128","212.71.234.208:8080","212.115.51.118:8085","188.68.0.201:8085","2.57.76.28:8085","142.93.36.245:8118","68.183.42.155:3128","2.57.76.62:8085","91.222.236.225:8085"]
		
        self.maybe_proxies = get_ssl_proxies() + [{'https': x} for x in maybe]
        random.shuffle(self.maybe_proxies)		
        random.shuffle(self.maybe_proxies)	
        random.shuffle(self.maybe_proxies)		
        random.shuffle(self.maybe_proxies)		
        random.shuffle(self.maybe_proxies)	
        random.shuffle(self.maybe_proxies)			
		
   def run(self):
    print ("Proxy worker: checking proxies")  
    # check proxies and feed to proxy_return queue 
    for proxy in self.maybe_proxies:      
      self.proxy_check.put(proxy)
	  
    # monitor how many proxies have been checked
    while self.done_fig != len(self.maybe_proxies):
      check = self.proxy_ask.get()
      self.done_fig += 1
      print ("Proxies to check:",len(self.maybe_proxies),"Checked:",self.done_fig)
    # kill the proxy checkers
    for x in range(3): 
      self.proxy_check.put("kill")
	
    # kill this thread to save resources
    sys.exit()
	

              		  
class Master_Worker(Thread):
   ''' makes calls to GiffGaff'''

   def __init__(self,proxy_ask,proxy_return,number_queue,account_queue,return_queue):
       Thread.__init__(self)
       self.proxy_ask = proxy_ask
       self.proxy_return = proxy_return
       self.number_queue = number_queue
       self.account_queue = account_queue
       self.page_status = "new_driver"     
       self.return_queue = return_queue	   
       self.method = 0
	   
       with open("user_agents.txt","r",encoding="utf-8") as agent_file:
          useragents = list(agent_file)
       self.user_agents = useragents
	   
   def run(self):
       print ("hello")
	   
       def check_response(_driver):
	   
          reload = ["ERR_TUNNEL_CONNECTION_FAILED"]

          new_driver = ["ERR_EMPTY_RESPONSE","Request unsuccessful","This site cant be reached","No internet"]
          for item in reload:
           if item in str(_driver.page_source):
             _driver.refresh
             for item in reload:
                if item in str(_driver.page_source):            
                   return "dead_driver", _driver

          for item in new_driver:
           if item in str(_driver.page_source):
              return "dead_driver", _driver
                   
          return 1, _driver				

		 
       def get_new_driver():
         # get a new account
         account = self.account_queue.get()		 

         # quick hack to add 0 because excel removes leading 0's from phone numbers		 
         username = account[0]
         if len(username) == 10:
          try: 
            test = int(username[0])
            test = int(username[1])
            test = int(username[2])
            test = int(username[3])
            test = int(username[4])        
            username = '0'+account[0]
          except:
            test = 0
			
         password = account[1]
 
         # get/wait for a proxy 
         print ("Main Thread: Waiting for a proxy server")
         proxy = self.proxy_return.get()
         print ("Main Thread: Got a proxy server, initializing	")
			
         # set up Chromedriver		
         useragent = random.choice(self.user_agents)[:-1]
         chrome_options = Options()
         chrome_options.add_argument("--user-agent='"+useragent+"'") 
        # chrome_options.add_argument("--headless")
         chrome_options.add_argument('log-level=2')
         chrome_options.add_argument('--proxy-server='+str(proxy['https']))
         _driver = webdriver.Chrome(options=chrome_options)	 
         return _driver, username, password
		 
       def login_etc():
         
         _driver, username, password = get_new_driver()
        		 
         # OPENING MAIN PAGE IS REQUIRED
         _driver.get('https://www.giffgaff.com/')
         try:
          _driver.get('https://www.giffgaff.com/auth/login')
         except:
          _driver.close()
          login_etc()
         check_val,_driver = check_response(_driver)
         if check_val != 1:
            _driver.close()
            login_etc()
							
	     # LOG IN

         _driver.find_element_by_xpath('//*[@id="nickname"]').send_keys(username)   
      #   ##driver.switch_to_window(driver.window_handles[0])
         _driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
      #   ##driver.switch_to_window(driver.window_handles[0])
         _driver.find_element_by_xpath('//*[@id="login_submit_button"]').click()	 
         print ("logged in")       
         t = 0
         while True:
                     if 'dashboard' not in str(_driver.current_url):
                         if t > 10:
                             login_etc()
                         time.sleep(.5)
                         t += 1
                     else:
                         break
         print ("On user dashboard page") 						 
         html = BeautifulSoup(_driver.page_source, 'html.parser')

         # all_links = html.findAll('a')

         # links = []
         # for item in all_links:
           # if 'profile' in str(item):
            # if "//" not in str(item):
             # if item['href'] not in links:
               # links.append(item['href'])  
         # print ("Got list of links for random link walk")			   
		 
         def do_random_link_walk(links,driver):
            ''' decides how many links to visit, visits a link, decides whether to scroll the page, decides  to wait or not before on a number to wait before scrolling page, scrolls the page'''
            num_of_link_visits = 1 #randint(1,1)   
            print ("Decided to visit",num_of_link_visits,"random links")
            links_to_visit = []
            for x in range(num_of_link_visits):
              link = random.choice(links)
              links_to_visit.append(link)
            for link_a in links_to_visit:
               print ("visiting a link: ",link_a)
               _driver.get('https://giffgaff.com'+link_a)
               scroll_or_not = randint(0,1)
               print ("To scroll the page or not to scroll: ",scroll_or_not)
               if scroll_or_not == 1:
                 random_scroll_value = randint(100,1000)
                 print ("Random scroll amount chosen as ",random_scroll_value)
                 time.sleep(get_random_1())
                 _driver.execute_script("window.scrollTo(0, "+str(random_scroll_value)+");")
                 time.sleep(get_random_1())              
                 print ("Scrolling back to the top of the page")
                 _driver.execute_script("window.scrollTo(0,0);")               
                 time.sleep(get_random_1())
            return _driver
			
         # do_random_link_walk(links_driver)
         # print ("Going back to the dashboard page")			
         # _driver.get('https://www.giffgaff.com/dashboard')
         time.sleep(get_random_1())
         print ("Scrolling down the page")
         _driver.execute_script("window.scrollTo(0,500);")
         time.sleep(get_random_1())
         try:
           print ("Clicking button to go to the top_up page")
           ##driver.switch_to_window(_driver.window_handles[0])
           top_up_button = _driver.find_element_by_id("button_topup")
           ##driver.switch_to_window(_driver.window_handles[0])		   
           top_up_button.click() 
         except:
          den = 1# top_up_button = _driver.find_element_by_xpath("button_topup")
         print ("sleeping 15 secs")		 
         time.sleep(15)
         #source = _driver.page_source
         check_val = check_response(_driver)
         if check_val == 1:
            print ("Check response was ok")
         if check_val == "dead_driver":
            self.number_queue.put(number)
            self.method = 0
            _driver.close()
            _driver = login_etc()
         time.sleep(get_random_1())
         return _driver		

       def check_number(_driver):
           number = self.number_queue.get()        
           source = _driver.page_source
           check_val = check_response(_driver)
           if check_val == 1:
              print ("Check response was ok")
           if check_val == "dead_driver":
              self.number_queue.put(number)
              self.method = 0
              _driver.close()
              return "new_driver"	
			 
			 #ERR_TUNNEL_CONNECTION_FAILED
			 
           if self.method == 0: 
             _driver.get('https://www.giffgaff.com/top-up')
             check_val = check_response(_driver)
             if check_val == 1:
               print ("Check response was ok")
             if check_val == "dead_driver":
                self.number_queue.put(number)
                self.method = 0
                _driver.close()
                return "new_driver"		   
             ##driver.switch_to_window(_driver.window_handles[0])
             open_nub = _driver.find_element_by_xpath('//*[@id="changeTopupNumber"]')     
             open_nub.click()
 
           ##driver.switch_to_window(_driver.window_handles[0	
			
		   
           try:
             open_nub = _driver.find_element_by_xpath('//*[@id="changeTopupNumber"]')     
             open_nub.click()
           except:
             nothing = 0
			 

           try: 		   
             phone_num = _driver.find_element_by_xpath('//*[@id="phone_number"]') 
           except:
             print ("EXCEPTION on phone number",_driver.current_url)
             phone_num = _driver.find_element_by_xpath('//*[@id="phone_number"]')
           time.sleep(get_random_1())
           pyautogui.press('backspace')  
		   
		   
           try:
             phone_num.clear()	  
           except:
             _driver.get('https://www.giffgaff.com/top-up')
             check_val = check_response(_driver)
             if check_val == 1:
               print ("Check response was ok")
             if check_val == "dead_driver":
                self.number_queue.put(number)
                self.method = 0
                _driver.close()
                return "new_driver"	


             phone_num = _driver.find_element_by_xpath('//*[@id="phone_number"]') 
             phone_num.clear()	  
			 
           pyautogui.press('backspace')
           time.sleep(get_random_1())	
           ##driver.switch_to_window(_driver.window_handles[0])		   
           for item in number:
             phone_num.send_keys(item)
             time.sleep(get_random_2())		   
           pyautogui.press('tab')	
           time.sleep(get_random_1())
           pyautogui.press('enter') 	 
           ##driver.switch_to_window(_driver.window_handles[0
           button = _driver.find_element_by_xpath('//*[@id="msisdn-btn"]')
           button.click()
           button.click()
           time.sleep(6)
           src = str(_driver.page_source)

           if 'Enter a valid giffgaff mobile number' in str(src):
              self.return_queue.put(['invalid',number])
              print ("Valid number found")
              self.method = 1			  
              return "success"

           if 'Fellow giffgaffer' in str(src):
              self.return_queue.put(['valid',number])
              print ("Valid number found")	
              return "success"
              self.method = 1
           if 'Enter a valid giffgaff mobile number' not in str(src):	  
            if 'Fellow giffgaffer' not in str(src):          	
              _driver.get('https://www.giffgaff.com/top-up')
              check_val = check_response(_driver)
              if check_val == 1:
                print ("Check response was ok but no number found on page")
                self.number_queue.put(number)
                return "success"
                self.method = 1				
              if check_val == "dead_driver":
                self.number_queue.put(number)
                self.method = 0
                _driver.close()
                return "new_driver"					
		 
       def get_random_1():
          ''' sleep between 0 & 3 second '''
          second = randint(0,3)
          milisecond = randint(10,99)
          time_string = str(second)+"."+str(milisecond)
          time_string = float(time_string)
          return time_string	
		   
       def get_random_2():
          ''' sleep between 0 and 1 second '''
          milisecond = randint(10,99)
          time_string = str(0)+"."+str(milisecond)
          time_string = float(time_string)
          return time_string		
		  
       def get_random_3():
          ''' sleep between 0 and 1 second '''
          milisecond = randint(10,50)
          time_string = str(0)+"."+str(milisecond)
          time_string = float(time_string)
          return time_string		

       while True:
         
		 # if we are just starting or have been blocked
         if self.page_status == "new_driver":  
            print ("Starting login code/getting new _driver")
            _driver = login_etc()
			
         print ("Checking number")
         status = check_number(_driver)
         print ("STATUS from check number:",status)
         if status == "success":
           self.method = 1
         self.page_status = status

           
         

		 
def login():
# LOGIN CREDENTIALS
    LOGIN_USERNAME = 'clareberryx' #'Razali2016' #07518405409'  : :
    LOGIN_PASSWORD = 'asda111' #Yusaf786' #Barbetti92'     clareberryx:asda111
	

    sess = random.random()
    session_id = sess
    PROXY_HOST = 'zproxy.lum-superproxy.io'  # rotating proxy
    PROXY_PORT = 22225
    PROXY_USER = 'lum-customer-hl_7f21a978-zone-static-country-gb-session-' + str(session_id)
    PROXY_PASS = '2s7f4pf9ucfx'
	
    super_proxy_url = ('http://%s-country-gb-session-%s:%s@zproxy.lum-superproxy.io:%d' %
        (PROXY_USER, session_id, PROXY_PASS, PROXY_PORT ))
    prox = '36.90.106.253:80'
    super_proxy_url = prox
    proxies = {
        'http': super_proxy_url,
        'https': super_proxy_url,
    }
    
    chrome_options = Options()
    chrome_options.add_argument("--user-agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'") 
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument('--proxy-server='+super_proxy_url)
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    _driver = webdriver.Chrome(options=chrome_options)
    
    def enter_proxy_auth(proxy_username, proxy_password):
        time.sleep(9)
        pyautogui.typewrite(proxy_username)
        pyautogui.press('tab')
        pyautogui.typewrite(proxy_password)
        pyautogui.press('enter')
        print ("DONDODNOND")
    	
    #Thread(target=enter_proxy_auth, args=(PROXY_USER, PROXY_PASS)).start()
    
    _driver.get('https://httpbin.org/ip')
    time.sleep(5)
    print (_driver.page_source)
	
    # OPENING MAIN PAGE IS REQUIRED
    _driver.get('https://www.giffgaff.com/')
    _driver.get('https://www.giffgaff.com/auth/login')
	
    import json

    #har = json.loads(_driver.get_log('har')[0]['message']) # get the log
  #  print('headers: ', har['log']['entries'][0]['request']['headers'])

	# LOG IN
    _driver.find_element_by_xpath('//*[@id="nickname"]').send_keys(LOGIN_USERNAME)   
    _driver.find_element_by_xpath('//*[@id="password"]').send_keys(LOGIN_PASSWORD)
    _driver.find_element_by_xpath('//*[@id="login_submit_button"]').click()


            # WAITING FOR DASHBOARD
    t = 0
    while True:
                if 'dashboard' not in _driver.current_url:
                    if t > 5:
                        raise ValueError
                    time.sleep(.5)
                    t += 1
                else:
                    break

    _cookies = {cookie['name']: cookie['value'] for cookie in _driver.get_cookies()}
    print ("cookies",_cookies)
    _driver.get('https://www.giffgaff.com/top-up/')
    time.sleep(30)
    open_nub = _driver.find_element_by_xpath('//*[@id="changeTopupNumber"]')     
    open_nub.click()
    print ("clicn on nub")
    phone_num = _driver.find_element_by_xpath('//*[@id="phone_number"]')  
    print ("phone_num.tex",phone_num.text)
    time.sleep(1.2)
    phone_num.clear()
    time.sleep(1.3)
    phone_num.send_keys('07851923377')   
    time.sleep(1.1)
    pyautogui.press('tab')	
    time.sleep(1)
    pyautogui.press('enter')
   ## button = _driver.find_element_by_xpath('//*[@id="msisdn-btn"]') # //*[@id="phone_number"]
  #  time.sleep(1)
 #   button.click()
    print ("clicked")
    src = str(_driver.page_source)

    if 'Enter a valid giffgaff mobile number' in src:
        print ("YNOOOOOOOOOOOOO")
        #return False
    if 'Fellow giffgaffer' in src:
        print ("YES I AM A FELLOW GIFFGAFFER")
	   
class Return_Worker(Thread):
   ''' Get's returned data and saves it'''

   def __init__(self,data_in_queue,return_queue,number_queue):
       Thread.__init__(self)
       self.data_in_queue = data_in_queue
       self.return_queue = return_queue
       self.number_queue = number_queue
       self.to_do = 0
       self.done = 0
       self.dona = 0
	   
   def run(self):
   
     def write_output(msg,method):
	 
         if method == 0:
            f_path = "Invalid_Numbers.txt"
         if method == 1:
            f_path = "Valid_Numbers.txt"
	 
         if path.isfile(f_path) == True:
		  
            with open(f_path,"a",encoding="utf-8") as valid_file:
              valid_file.write(str(msg)+"\n")
			  
         if path.isfile(f_path) == False:       
		  
            with open(f_path,"w",encoding="utf-8") as valid_file:
              valid_file.write(str(msg)+"\n")
			  
     while True:
       
       return_data = self.return_queue.get()
       
       if return_data[0] == "to_do":
         self.to_do = return_data[1]
		 
       if return_data[0] == "valid":
          write_output(return_data[1],1)	
          self.done += 1		  
          
       if return_data[0] == "invalid":
          write_output(return_data[1],0)			 
          self.done += 1

       if return_data[0] == "donea":
          self.dona += 1		  		  
		  
       if return_data[0] == "invalida":
          write_output(return_data[1],0)			 
          self.dona += 1		  
	   
       if self.dona == self.to_do:
          
          self.number_queue.put(["kill"])
          print ("Killing Number Worker")     

       if self.to_do > 0:
	
         print ("RETURN WORKER: to_do:",self.to_do,"Done:",self.done)	   

       # kill the return worker thread		 
       if self.to_do == self.done:
          self.data_in_queue.put(["kill"])
          print ("All tasks finished - Killing Return Worker")
          sys.exit()

		  
if __name__ == "__main__":

       # set-up queues to pass data between threads
       number_queue = Queue()
       return_queue = Queue()
       data_in_queue = Queue()
       feed_queue = Queue()
       proxy_ask = Queue()
       proxy_return = Queue()
       proxy_check = Queue()
       proxy_check_return = Queue()
       account_queue = Queue()

       # add all the accounts to a queue so that the Master workers can take them as needed	   
       with open("accounts.csv","r",encoding="utf-8") as account_file:
          accounts = csv.reader(account_file)
          accounts = list(accounts)

       # quick hack, add the accounts to the queue 5 times(=5x the number of accounts to use)
       x = 0
       while x < 5:	   
        for item in accounts:
          account_queue.put(item) 
        x += 1
		
       NUMBER_OF_MASTER_THREADS = 3
		 
       # start the proxy worker	thread 
       for x in range(1):
         r_worker = proxyWorker(proxy_ask,proxy_return,proxy_check,proxy_check_return)
         r_worker.daemon = False
         r_worker.start()
		 
        # start the proxy checker threads
       for x in range(3):
          n_worker = proxyChecker(proxy_check,proxy_return,proxy_ask)
          n_worker.daemon = False
          n_worker.start()

       # start the return thread		 
       for x in range(1):
         r_worker = Return_Worker(data_in_queue,return_queue,feed_queue)
         r_worker.daemon = False
         r_worker.start()
		 
       # start the master worker threads		 		 
       for x in range(3):
         n_worker = Master_Worker(proxy_ask,proxy_return,number_queue,account_queue,return_queue)
         n_worker.daemon = False
         n_worker.start()

       # get numbers to be checked
       with open("numbers.txt","r",encoding="utf-8") as num_file:
          num_list = list(num_file)

       # define how many numbers we are working with		  
       return_queue.put(["to_do",len(num_list)])
	   
       # send the numbers to the number queue ready to be taken by the master workers		  
       for number in num_list:
          number_queue.put(number.replace("\n",""))