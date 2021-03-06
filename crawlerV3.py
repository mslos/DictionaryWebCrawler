#-------------------------------------------------------------------------------
# Name:        MW Crawler V3.
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

#Enter your MW user name and password:
USER_NAME = " ";
PASSWORD = " ";


exception_list = [u"\u2014 ",u"specifically"]
#letter space colon, paren num paren to be deleted

def main():
##    a = "sdsskfg \nsdfdjgndf"
##    print re.sub('^sd','NAAAH',a,0,re.MULTILINE)
    current_letter = 'l'
    browser = webdriver.Chrome("C:\Program Files (x86)\Python 27\py\chromedriver.exe")
    browser.implicitly_wait(10)

    start_time = time.time()
    browser.get('http://unabridged.merriam-webster.com/advanced-search.php')

    username = browser.find_element_by_name('login_user')  # Find the search box
    username.send_keys(USER_NAME)

    password = browser.find_element_by_name('login_pass')  # Find the search box
    password.send_keys(PASSWORD + Keys.RETURN)


    browser.get('http://unabridged.merriam-webster.com/advanced-search.php')

    select = Select(browser.find_element_by_name('fl'))
    select.select_by_visible_text("Adjective")

    search_box = browser.find_element_by_name('hw')  # Find the search box
    search_box.send_keys(current_letter+'*'+Keys.RETURN)

    database = codecs.open('list '+current_letter+'.txt','w',encoding='utf-16')

##    find_element_by_css_selector(":nth-of-type()")

    for cur_list_page in range(10,1420,10):
        for cur_num in range(1,11):
            wd = browser.find_element_by_css_selector("div.hdword")
            new_wd = re.sub('^[1-9]+', '', wd.text)
            new_wd = re.sub(u"\xb7",'',new_wd)
##            for i in range(5):
    ##            try:
    ##                new_wd = new_wd.replace(u'.','')
    ##            except:
    ##                pass


    ##        num_of_meanings = int((re.search('^[1-9]+', wd.text)).group(0))
    ##        print new_wd
    ##        print num_of_meanings

            all_def = browser.find_element_by_css_selector("div.d")
            ##    for cur_num in range(1,num_of_meanings+1):
            ##        all_def = browser.find_element_by_css_selector("span.ssens:nth-of-type("+str(cur_num)+")")
##            print all_def.text
            result = re.sub("<.+>",'',all_def.text,0,re.MULTILINE)
            result = re.sub("^[1-9]",'',result,0,re.MULTILINE)
            result = re.sub("^:  ",'',result,0,re.MULTILINE)
            result = re.sub("^\([1-9]\) : ",'',result,0,re.MULTILINE) #here
            result = re.sub("^[a-z] : ",'',result,0,re.MULTILINE)
            result = re.sub("^[a-z] \([1-9]\) : ",'',result,0,re.MULTILINE)
            result = re.sub("^: such as",'',result,0,re.MULTILINE)
            result = re.sub("^[a-g] ",'',result,0,re.MULTILINE)

            final_result = result.split('\n')
## final_resulprintt

            stop_token1 = False
            while stop_token1==False:
                try:
                    final_result.remove(u'')
                except:
                    stop_token1 = True
##            print final_result

            stop_token2 = False
            while stop_token2==False:
                try:
                    final_result.remove('\n')
                except:
                    stop_token2 = True
##            print final_result

            for i in range(0,len(final_result)):
                try:
                    if u"\xb7" in final_result[i]:
                            del final_result[i]
                except:
                    pass

            for possibility in exception_list:
                for i in range(0,len(final_result)):
                    try:
                        if re.match(possibility,final_result[i]) != None:
                            final_result[i-1] += final_result[i]
                            del final_result[i]
                    except:
                        pass
            """Trying to account for all the exceptions"""

            string_to_write = '\r\n'+new_wd
            for lines in final_result:
                string_to_write += '\t'+lines
##            print final_result
            database.write(string_to_write)
            browser.execute_script("return select_ref_result("+str(cur_num)+", 'result-list-desktop');")
            #There are 10 entries per page

        browser.execute_script("return goto_results('result-list-desktop','"+str(cur_list_page)+"');")
        #Pages are itirated in multiples of 10
    database.write("### Total run time: "+str(time.time()-start_time)+" seconds.")
    database.close()



if __name__ == '__main__':
    main()
