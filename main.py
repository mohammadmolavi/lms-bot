from webbot import Browser
from bs4 import BeautifulSoup
import re
from passwords import username , password
notifs = []
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
    web.go_to('http://lms.ui.ac.ir/activity/notifications/pulldown')
    web.go_to('http://lms.ui.ac.ir/activity/notifications')
    r = web.get_page_source()
    soup = BeautifulSoup(r, 'html.parser')
    s = soup.findAll('ul', id="notifications_main")
    for all_Notif in s[0].contents:
        try:
            if all_Notif.attrs['class'][0] != 'notifications_unread':
                continue
            for messages in all_Notif.contents:
                str = ''
                for message in messages:
                    try:
                        str += message.contents[0]
                    except:
                        if message != '\n':
                            str += message
                if str != '':
                    notifs.append(str)
        except:
            pass


login()
all_home_elements, lessons = extract_info()
show_new_all_message(all_home_elements)
print(notifs)




