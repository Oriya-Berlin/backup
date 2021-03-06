from general_functions import *


# Login to instagram
def login(driver, username, password):
    inputs = driver.find_elements_by_tag_name('input')
    buttons = driver.find_elements_by_tag_name('button')

    inputs[0].send_keys(username)  # username input
    inputs[1].send_keys(password)  # password input
    buttons[0].click()             # Log-in   input


# send msg in current user page
def send_msg(driver, msg):
    msg_btn = driver.find_element_by_xpath('//*[text()="Message"]')
    msg_btn.click()
    time.sleep(3)

    text = driver.find_element_by_tag_name('textarea')
    text.send_keys(msg)
    time.sleep(3)

    send = driver.find_element_by_xpath('//*[text()="Send"]')
    send.click()


# follow after user when we stand in current page
def follow_in_current_page(driver):
    try:
        follow = driver.find_element_by_xpath('//*[text()="Follow"]')
        follow.click()
    except:
        print("we all ready follow that target.")
        return False
    return True


# unfollow after user when we stand in current page
def unfollow_in_current_page(driver):

    spans = driver.find_elements_by_tag_name('span')
    flag = True

    for span in spans:
        if span.get_attribute('aria-label') == 'Following':
            span.click()
            flag = False
            break

    if flag:
        buttons = driver.find_elements_by_tag_name('button')
        for btn in buttons:
            if btn.get_attribute('innerHTML') == 'Requested':
                btn.click()
                break

    SLEEP(2)
    buttons = driver.find_elements_by_tag_name('button')
    for btn in buttons:
        if btn.get_attribute('innerHTML') == 'Unfollow':
            btn.click()
            return True
    return False


# boolean, when we are in current user page, it check if this user is our follower
def is_followed(driver):
    buttons = driver.find_elements_by_tag_name('button')
    for btn in buttons:
        if btn.get_attribute('innerHTML') == 'Follow':
            return False
    return True


# find search box element, and send the given value
def search(driver, value):
    search_boxes = driver.find_elements_by_tag_name('input')
    for input in search_boxes:
        if input.get_attribute('placeholder') == 'Search':
            input.send_keys(value)
            break


# find user by given name in the search result grid
def find_user_in_search_result(driver, value):
    try:
        spans = driver.find_elements_by_tag_name('span')
        for span in spans:
            if span.get_attribute('innerHTML') == value:
                span.click()
                return True

        links = driver.find_elements_by_tag_name('a')
        for link in links:
            if link.get_attribute('href') == f'/{value}/':
                link.click()
                return True
    except:
        print(f'ERROR on "find_user_in_search_result" function. user: {value}')
    return False

    #find = driver.find_element_by_xpath(f'//a[@href="/{value}/"]')
    #find.click()


# open followers list in current page
def open_followers_list_in_current_page(driver):
    followers_list = driver.find_element_by_xpath('//*[text()=" followers"]')
    followers_list.click()


# get rid of 'Save Your Login Info?' window when shooter connect
def save_your_login_info_window(driver):  #need to test that
    try:
        buttons = driver.find_elements_by_tag_name('button')
        for btn in buttons:
            if btn.get_attribute('innerHTML') == 'Not Now':
                """ 'Save Info' is the other option """
                btn.click()
                driver.refresh()
                SLEEP(2)
                return
    except:
        return


# get rid of 'not now' window when shooter connect
def not_now_window(driver):
    #if driver.find_element_by_xpath('//*[text()="Not Now"]') != None:
    #print('not now EXIST')
    try:
        buttons = driver.find_elements_by_tag_name('button')
        for btn in buttons:
            if btn.get_attribute('innerHTML') == 'Not Now':
                """ 'Not Now' is the other option """
                btn.click()
        #N_N = driver.find_element_by_xpath('//*[text()="Not Now"]')
        #N_N.click()
    except:
        return


# scroll followers list in current page till the end
def scroll_all_followers_list(driver):
    followers = driver.find_elements_by_tag_name('li')
    loaded_till_now = len(followers)
    total_followers = get_followers_number_on_PUBLIC_account(driver)  # maybe also with private
    total_followers = int(total_followers)
    print(total_followers)
    counter = 0
    while loaded_till_now < total_followers:
        print(loaded_till_now)
        try:
            SLEEP(1)
            followers[loaded_till_now - 10].location_once_scrolled_into_view
            SLEEP(2.5)
            followers = driver.find_elements_by_tag_name('li')
            loaded_till_now = len(followers)
        except:
            print(f' *  {counter}')
            continue
            
    SLEEP(1)

    for i in range(5):
        try:
            followers[loaded_till_now - 1].location_once_scrolled_into_view
            SLEEP(2.5)
            followers = driver.find_elements_by_tag_name('li')
            loaded_till_now = len(followers)
        except:
            continue


# get following number on PRIVATE account
def get_following_number_on_PRIVATE_account(driver):  # maybe we need to add name parameter
    elements = driver.find_elements_by_tag_name('span')
    for element in elements:
        inner_text = element.get_attribute('innerHTML')
        try:
            exist = inner_text.endswith(' following')
            if exist:
                number = extract_and_convert_number(element.text)
                return number
        except:
            pass


#  here we need the following number
def get_following_number_on_PUBLIC_account(driver, name):  # maybe we need to add name parameter
    links = driver.find_elements_by_tag_name('a')
    #name = get_user_name_in_PUBLIC_current_page(driver)  # that row
    for link in links:
        if link.get_attribute('href') == f'https://www.instagram.com/{name}/following/':
            number = extract_and_convert_number(link.text)
            return number


# scrap the followers number on current PUBLIC user page
def get_followers_number_on_PUBLIC_account(driver):
    elements = driver.find_elements_by_tag_name('a')
    for element in elements:
        inner_text = element.get_attribute('innerHTML')
        exist = inner_text.endswith(' followers')
        if exist:
            number = extract_and_convert_number(element.text)
            return number


# scrap the followers number on current PRIVATE user page
def get_followers_number_on_PRIVATE_account(driver):
    elements = driver.find_elements_by_tag_name('span')
    for element in elements:
        inner_text = element.get_attribute('innerHTML')
        try:
            exist = inner_text.endswith(' followers')
            if exist:
                number = extract_and_convert_number(element.text)
                return number
        except:
            pass


# watch story of user if exist
def watch_story(driver, username):

    attribute = f"{username}'s profile picture"
    images = driver.find_elements_by_tag_name('img')
    for img in images:
        if img.get_attribute('alt') == attribute:
            img.click()
            return True


# take all the 'a' elements, extract the names and return them on array
def all_followers_to_list(driver):
    followers_list = []
    links = driver.find_elements_by_tag_name('a')

    for link in links:
        text = link.get_attribute('innerHTML')
        title = link.get_attribute('title')
        href = clean_url(link.get_attribute('href'))

        if text == title and text == href:
            followers_list.append(text)

    return followers_list


# close story
def close_story(driver):
    try:
        story = driver.find_element_by_class_name('coreSpriteCloseLight')
        story.click()
    except:
        return False
    return True


# close followers list of user
def close_followers_list(driver):
    buttons = driver.find_elements_by_tag_name('svg')
    for btn in buttons:
        if btn.get_attribute('aria-label') == 'Close':
            btn.click()
            return


# clean search box
def clean_search_box(driver):
    search_boxes = driver.find_elements_by_tag_name('input')
    for input in search_boxes:
        if input.get_attribute('placeholder') == 'Search':
            input.clear()
            break


# extract users names after we scrolled all the followers list
def get_user_name_in_followers_list(driver):
    links = driver.find_elements_by_tag_name('a')

    for link in links:
        text = link.get_attribute('innerHTML')
        title = link.get_attribute('title')
        href = clean_url(link.get_attribute('href'))

        if text == title and text == href:
            name = text
            return name


# extract user name when we in PUBLIC current page
def get_user_name_in_PUBLIC_current_page(driver):
    tags = driver.find_elements_by_tag_name('h2')
    links = driver.find_elements_by_tag_name('a')
    for tag in tags:
        name1 = tag.get_attribute('innerHTML')
        for link in links:
            name2 = clean_url(link.get_attribute('href'))
            if name1 == name2:
                return name1


# extract user name when we in PRIVATE current page
def get_user_name_in_PRIVATE_current_page(driver):
    tags = driver.find_elements_by_tag_name('h2')
    name = tags[0].get_attribute('innerHTML')
    return name


# boolean, return true if account is private
def check_if_current_page_is_private(driver):
    tags = driver.find_elements_by_tag_name('h2')
    for tag in tags:
        if tag.get_attribute('innerHTML') == 'This Account is Private':
            return True
    return False




