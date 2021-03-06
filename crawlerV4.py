#-------------------------------------------------------------------------------
# Name:        Merriam Websters Crawler.
# Purpose:
#
# Author:      Mato
#
# Created:     24-07-2014
# Copyright:   (c) Mato 2014
# Licence:     MIT
#-------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains as x
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import re
import codecs
import time
import selenium

#Enter your MW user name and password:
USER_NAME = " ";
PASSWORD = " ";

exception_list = [u"\u2014 ",u"specifically"]
#letter space colon, paren num paren to be deleted

def main():
##    a = "sdsskfg \nsdfdjgndf"
##    print re.sub('^sd','NAAAH',a,0,re.MULTILINE)

    browser = webdriver.Chrome("C:\Program Files (x86)\Python 27\py\chromedriver.exe")
    browser.implicitly_wait(3)

    browser.get('http://unabridged.merriam-webster.com/advanced-search.php')


    username = browser.find_element_by_name('login_user')  # Find the search box
    username.send_keys(USER_NAME)

    password = browser.find_element_by_name('login_pass')  # Find the search box
    password.send_keys(PASSWORD + Keys.RETURN)
    all_letters = "rst" #letters in the dictinary to crawl

    for current_letter in all_letters:
##        current_letter = 'l'
        start_time = time.time()
        database = codecs.open('list '+current_letter+'.txt','a',encoding='utf-16')

        browser.get('http://unabridged.merriam-webster.com/advanced-search.php')

        select = Select(browser.find_element_by_name('fl'))
        select.select_by_visible_text("Adjective")

        search_box = browser.find_element_by_name('hw')  # Find the search box
        search_box.send_keys(current_letter+"*"+Keys.RETURN)
        new_wd_flag = 'a'
        new_wd = 'a'
        prev_wd = 'b'

        cur_list_page = 10

        if current_letter is 'r':
            cur_list_page = 320
        if current_letter is 'p':
            cur_list_page = 4600

        while new_wd_flag != prev_wd:
            cur_list_page += 10
            for cur_num in range(1,11):
                prev_wd = new_wd_flag
                try:
                    wd = browser.find_element_by_css_selector("div.hdword")
                except:
                        browser.back()
                        browser.forward()
                        wd = browser.find_element_by_css_selector("div.hdword")
                new_wd_flag = wd.text
                new_wd = re.sub('^[1-9]+', '', wd.text)
                new_wd = re.sub(u"\xb7",'',new_wd)
                print new_wd

                def_cur_word = []

                error_flag = False
                i = 1
                while error_flag is False:
                    try:
                        def_cur_word.append(browser.find_element_by_css_selector("div.sblk:nth-of-type("+str(i)+")").text)
                        i+=1
                    except selenium.common.exceptions.NoSuchElementException:
                        error_flag=True
    ##            print def_cur_word
                if len(def_cur_word) is 0:
                    try:
                        def_cur_word.append(browser.find_element_by_css_selector("div.d").text)
                    except:
                        pass

                for i in range(len(def_cur_word)):
                    result = def_cur_word[i]
                    result = re.sub("<.+>",'',result,0,re.MULTILINE)
                    result = re.sub("^[1-9]",'',result,0,re.MULTILINE)
                    result = re.sub("^:\s\s",'',result,0,re.MULTILINE)
                    result = re.sub("\n",' ',result,0,re.MULTILINE)
                    result = re.sub("^\s",'',result,0,re.MULTILINE)
                    def_cur_word[i] = result

    ##            print def_cur_word

                string_to_write = '\r\n'+new_wd
                for lines in def_cur_word:
                    string_to_write += '\t'+lines
    ##            print string_to_write
                database.write(string_to_write)
                try:
                    browser.execute_script("return select_ref_result("+str(cur_num)+", 'result-list-desktop');")
                except:
                    browser.back()
                    browser.forward()
                    browser.execute_script("return select_ref_result("+str(cur_num)+", 'result-list-desktop');")
                #There are 10 entries per page
            print cur_list_page
            try:
                browser.execute_script("return goto_results('result-list-desktop','"+str(cur_list_page)+"');")
            except:
                browser.back()
                browser.forward()
                browser.execute_script("return goto_results('result-list-desktop','"+str(cur_list_page)+"');")

            #Pages are itirated in multiples of 10


        database.write("### Total run time: "+str(time.time()-start_time)+" seconds.")
        database.close()




if __name__ == '__main__':
    main()
