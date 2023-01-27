from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from time import sleep
import json


# Workaround for webdriver.execute_cdp_cmd(command, params) -> send(webdriver, command, params)

def send(driver, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    new_url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', new_url, body)
    return response.get('value')


def get_users(file):
    out = []
    with open(file, "r") as jsondump:
        out = json.load(jsondump)
    return out


def set_users(file, accounts):
    with open(file, 'w') as f:
        f.write(json.dumps(accounts, indent=4))


def build_html():
    summe = 0
    out = "<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"UTF-8\">\n<title>Casa de Papel</title>\n<style>\ntable, th, td {\npadding: 10px;\nborder: 1px solid black; \nborder-collapse:\ncollapse;\n}\n</style>\n</head>\n<body style=\"background-color:#303030; color:white;\"\nalign=\"center\">\n⢰⣶⣶⡆⠀⠀⠀⢰⣶⣶⣶⡆⠀⠀⠀⠀⢠⣶⣶⣿⣷⣶⣄⠀⠀⣶⣶⣶⣶⠀⠀⣠⣶⣿⣿⣷⣦⡀⠀⢰⣶⣶⣶⡆⠀⠀⢸⣶⡶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⢾⠀⢰⣶⣶⣶⣶⣶⣦⠀⢰⣶⣶⣶⡆⠀⢰⣶⣶⣶⣶⣶⣄⢰⣶⣶⣶⣶⠀⣶⣶⡆⠀⠀\n⢸⣿⣿⡇⠀⠀⠀⣾⣿⣿⣿⡇⠀⠀⠀⠀⣿⣿⣿⠋⣿⣿⣿⠁⢠⣿⣿⣿⣿⡄⠀⣿⣿⣿⠙⣿⣿⡇⠀⢸⣿⣿⣿⣿⠀⠀⢸⣿⣻⡽⡞⠓⠛⠚⢷⠛⠚⠓⣟⡾⢯⠀⢸⣿⣿⡏⣿⣿⣿⠀⣼⣿⣿⣿⣇⠀⢸⣿⣿⡏⣿⣿⣿⢸⣿⣿⡏⠉⠀⣿⣿⡇⠀⠀\n⢸⣿⣿⡇⠀⠀⠀⣿⣿⢹⣿⣿⠀⠀⠀⠀⣿⣿⣿⠀⣿⣿⣿⠀⢸⣿⡟⣿⣿⡇⠀⣿⣿⣷⣀⠿⠿⠇⠀⣿⣿⣿⣿⣿⡀⠀⢸⣽⣳⣟⡇⠀⣗⠀⢸⠀⠀⣶⢯⣟⡿⠀⢸⣿⣿⡇⣿⣿⣿⠀⣿⣿⢻⣿⣿⠀⢸⣿⣿⡇⣿⣿⣿⢸⣿⣿⣇⣀⠀⣿⣿⡇⠀⠀\n⢸⣿⣿⡇⠀⠀⢸⣿⣿⢸⣿⣿⠀⠀⠀⠀⣿⣿⣿⠀⠉⠉⠉⠀⣾⣿⡇⣿⣿⣷⠀⠹⣿⣿⣿⣷⣀⠀⠀⣿⣿⠏⣿⣿⡇⠀⢸⢿⡿⣟⡇⠀⡿⠀⢸⠀⠀⠋⣿⣿⣻⠀⢸⣿⣿⡇⣿⣿⣿⢀⣿⣿⢸⣿⣿⠀⢸⣿⣿⡇⣿⣿⣿⢸⣿⣿⣿⣿⠀⣿⣿⡇⠀⠀\n⢸⣿⣿⡇⠀⠀⢸⣿⡟⠸⣿⣿⡆⠀⠀⠀⣿⣿⣿⠀⣶⣶⣶⠠⣿⣿⡇⢹⣿⣿⠀⣄⣀⡙⢿⣿⣿⡇⣰⣿⣿⠀⣿⣿⡇⠀⢸⢯⡿⣽⡇⠀⣟⠀⢸⠀⠀⣿⣻⡞⣷⠀⢸⣿⣿⣿⣿⣿⡿⢸⣿⣿⠈⣿⣿⡇⢸⣿⣿⣿⣿⣿⡿⢸⣿⣿⡏⠉⠀⣿⣿⡇⠀⠀\n⢸⣿⣿⡇⠀⠀⣿⣿⣿⣶⣿⣿⡇⠀⠀⠀⣿⣿⣿⠀⣿⣿⣿⢀⣿⣿⣷⣾⣿⣿⡄⣿⣿⡟⠀⣿⣿⡇⣸⣿⣿⣶⣿⣿⣿⠀⢸⣯⣟⡷⡇⠀⠋⠀⢸⠀⠀⠓⣯⣟⡷⠀⢸⣿⣿⡇⠀⠀⠀⣽⣿⣿⣶⣿⣿⣇⢸⣿⣿⡇⠀⠀⠀⢸⣿⣿⡇⠀⠀⣿⣿⡇⠀⠀\n⢸⣿⣿⣿⣾⡗⣿⣿⡟⠛⣿⣿⣿⠀⠀⠀⢻⣿⣿⣶⣿⣿⣿⢸⣿⣿⠛⠻⣿⣿⡇⢿⣿⣿⣶⣿⣿⡇⣿⣿⡟⠛⢻⣿⣿⠀⢸⡷⣾⡽⣷⣾⣽⡾⣿⢶⡷⣶⣻⢾⡽⠀⢸⣿⣿⡇⠀⠀⠀⣿⣿⡟⠛⣿⣿⣿⢸⣿⣿⡇⠀⠀⠀⢸⣿⣿⣷⣶⠠⣿⣿⣷⣿⡇\n⠘⠙⠉⠋⠙⠋⠉⠋⠁⠀⠘⠉⠛⠀⠀⠀⠀⠉⠛⠛⠛⠋⠁⠈⠙⠙⠀⠀⠋⠋⠑⠈⠙⠛⠛⠛⠉⠀⠋⠛⠃⠀⠈⠋⠙⠃⠘⠛⠓⠛⠓⠛⠚⠛⠛⠛⠛⠓⠛⠛⠛⠀⠘⠛⠛⠃⠀⠀⠀⠉⠋⠁⠀⠈⠙⠙⠘⠛⠛⠃⠀⠀⠀⠘⠛⠛⠛⠛⠀⠙⠉⠋⠙⠛\n<table align=\"center\">\n<tr>\n<th>User</th>\n<th>Points</th>\n<th>Error happened</th>\n<th>Reset Cookie</th>\n<th>Remove Account</th>\n</tr>\n"
    for user in get_users('../accounts.json'):
        out += build_user_entry(user)
        summe += int(user["points"])
    out += "<tr>\n" + "<td>Sum</td>\n<td>" + str(summe) + "</td>\n</tr>\n"
    out += "</table>\n<a href=\"file:///newuser\">Add a new user</a>\n<p>Since this is just dumb html, the links will first take you to non-existing sites in order to paste the Cookies and to then redirect you</p>\n<p>If your login doesnt work anymore, this is mostly if it hasnt been used for a while or if the account got locked down</p>\n</body>\n</html>"
    html = open('index.html', 'w')
    html.write(out)
    html.close()


def build_user_entry(user):
    return "<tr>\n" + "<td><a href=\"file:///" + user["username"] + "\">" + user["username"] + "</a></td>\n<td>" + str(user["points"]) + "</td>\n<td>" + str(user["error"]) + "</td>\n<td><a href=\"file:///_" + user["username"] + "\">Relogin</a></td>\n<td><a href=\"file:///__" + user["username"] + "\">Remove</a></td>\n</tr>\n"


def get_user_index(query):
    index = 0
    for user in get_users('../accounts.json'):
        if user["username"] == query:
            return index
        index += 1
    return -1


def create_cookie(cookiename, cookievalue):
    return {'domain': 'login.live.com', 'name': cookiename, 'value': cookievalue, 'secure': True, 'httpOnly': True}


def open_dashboard(driver, index):
    driver.get("https://rewards.bing.com")
    send(driver, 'Network.enable', {})
    send(driver, 'Network.setCookie', create_cookie('__Host-MSAAUTHP', get_users('../accounts.json')[index]["cookie"]))
    send(driver, 'Network.disable', {})
    sleep(1)
    driver.get("https://rewards.bing.com")


def reload_html(driver):
    send(driver, 'Network.clearBrowserCookies', {})
    build_html()
    driver.get('file:///home/seluser/index.html')


def add_userconf(file, u_name, cookie):
    accounts = get_users(file)
    accounts.append({"username": u_name, "cookie": cookie, "points": 0, "error": "false"})
    set_users(file, accounts)
    print("adding success")


def remove_userconf(file, u_name):
    accounts = get_users(file)
    accounts.pop(get_user_index(u_name))
    set_users(file, accounts)
    print("removal success")


def reload_userconf(file, u_name, cookie):
    accounts = get_users(file)
    u_index = get_user_index(u_name)
    accounts[u_index]['cookie'] = cookie
    accounts[u_index]['error'] = "false"
    set_users(file, accounts)
    print("reloading success")


def new_user(driver):
    wait = WebDriverWait(driver, 10)
    send(driver, 'Network.clearBrowserCookies', {})
    driver.get('https://rewards.bing.com/Signin?idru=%2F')
    while not driver.current_url.__contains__('https://rewards.bing.com'):
        sleep(0.1)
    emailstring = wait.until(
        EC.presence_of_element_located((By.ID, 'mectrl_currentAccount_picture'))).get_dom_attribute('onclick')
    email = emailstring[92:len(emailstring) - 2]
    while driver.current_url.__contains__('https://login.live.com'):
        sleep(0.1)
    driver.get('https://login.live.com/oauth20_authorize.srf?client_id=0')
    cookie = driver.get_cookie('__Host-MSAAUTHP')
    add_userconf("../accounts.json", email, cookie['value'])
    print("Success")
    reload_html(driver)


def remove_user(driver, user):
    remove_userconf("../accounts.json", user)
    reload_html(driver)


def reload_user(driver):
    wait = WebDriverWait(driver, 10)
    send(driver, 'Network.clearBrowserCookies', {})
    driver.get('https://rewards.bing.com/Signin?idru=%2F')
    while not driver.current_url.__contains__('https://rewards.bing.com'):
        sleep(0.1)
    emailstring = wait.until(
        EC.presence_of_element_located((By.ID, 'mectrl_currentAccount_picture'))).get_dom_attribute('onclick')
    email = emailstring[92:len(emailstring) - 2]
    while driver.current_url.__contains__('https://login.live.com'):
        sleep(0.1)
    driver.get('https://login.live.com/oauth20_authorize.srf?client_id=0')
    cookie = driver.get_cookie('__Host-MSAAUTHP')
    reload_userconf("../accounts.json", email, cookie)
    reload_html(driver)


def create_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86 64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/106.0.1370.52')
    options.add_argument('log-level=3')
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    browser = WebDriver(command_executor='http://dashboard:4444', options=options)
    browser.maximize_window()
    browser.get('file:///home/seluser/index.html')
    browser.fullscreen_window()
    return browser


def session_run():
    build_html()
    driver = create_browser()
    try:
        while True:
            build_html()
            url = driver.current_url
            userindex = get_user_index(url[8:len(url)])
            if url == "file:///home/seluser/index.html":
                sleep(0.1)
            elif url == "file:///newuser":
                new_user(driver)
            elif url.startswith("file:///_"):
                username = url.split("_")[-1]
                if url.startswith("file:///__"):
                    remove_user(driver, username)
                else:
                    reload_user(driver)
            elif userindex > -1:
                open_dashboard(driver, userindex)
            sleep(0.1)
    except selenium.common.exceptions.WebDriverException:
        print(driver.get_log('driver')[-1])
        driver.quit()


while True:
    session_run()
