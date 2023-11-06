import time

from webbot import Browser
from bs4 import BeautifulSoup
import re
from passwords import username , password

web = Browser()


def login():
    web.go_to('http://lms.ui.ac.ir')
    web.type(username)
    web.press(web.Key.TAB)
    web.type(password)
    web.press(web.Key.ENTER)


def extract_info():
    r = web.get_page_source()
    soup = BeautifulSoup(r, 'html.parser')
    s = soup.find('div', class_="layout_group_profile_groups")
    divs = []
    lessons = []
    for lesson in s.find_all('div'):
        divs.append(lesson.text)
    for temp in divs:
        temp = re.sub("\n", "", temp)
        temp = re.sub('\t', '', temp)
        temp = re.sub('[»«]', '', temp)
        temp = re.sub(r'[0-9]', '', temp)
        temp = re.sub(r'[۱-۹]', '', temp)
        temp = re.sub('-', '', temp)
        temp = re.sub('کد درس: ', '', temp)
        temp = re.sub('  ', '', temp)

        if temp != ' ' and temp != '':
            lessons.append(temp)

    return s, lessons


def show_new_all_message(all_home_elements):
    r = web.get_page_source()
    soup = BeautifulSoup(r, 'html.parser')
    s=soup.find_all('a',id='updates_toggle')
    try :
        print(s[0].contents[3].contents[0])
    except:
        return 0
    web.go_to('http://lms.ui.ac.ir/activity/notifications/update')
    web.go_to('http://lms.ui.ac.ir/activity/notifications/pulldown')
    r = web.get_page_source()
    soup = BeautifulSoup(r, 'html.parser')
    s = soup.findAll('div', id="global_content")
    for all_Notif in s:
        for messages in all_Notif.contents[3:]:
            try:
                for message in messages.contents[1].contents:
                    try:
                        print(message.contents[0],end='')
                    except:
                        print(message,end='')
            except: pass

    web.go_back()
    web.go_back()
    web.go_to('http://lms.ui.ac.ir/activity/notifications/markread')
    time.sleep(10)



login()
all_home_elements, lessons = extract_info()
show_new_all_message(all_home_elements)
#4012013129
#6570091522



