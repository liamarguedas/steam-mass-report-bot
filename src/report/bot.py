



import json
import time
from datetime import datetime

from pathlib import Path

from steam.client import SteamClient
from steam.guard import generate_twofactor_code

from colorama import Fore, Back, Style, init


import random
import requests


EXECUTION_TIME = datetime.now()

# Paths
ROOT_PATH = Path(__file__).parents[2]
BOTS_PATH = ROOT_PATH / "src" / "report" / "accounts" / "bots.txt" 
LOGS_PATH = ROOT_PATH / "src" / "report" / "logs" 

# Configs
ACCOUNTS_TO_REPORT = [] # READ FROM DISCORD CHANNEL? API POST?
APPID = "730"
DELAY_BETWEEN_REPORTS = "5000" # Delay between each report in ms
VERIFIED_ACCOUNTS = True #Limited: false no money spent /true: $5 spent

EREPORT_ID = 12

def main():


    bots = get_bots()
    comments = load_comments() 

    logger(f"Total {len(bots)} bots found.")
    

    # Counters

    logins_sucessful, loggins_failed = 0, 0
    reports_successful, reports_failed = 0, 0
    
    # Executing each bot
    for bot in bots:

        credentials = bot.split(":")

        username = credentials[0]
        password = credentials[1]
        secret = None if not VERIFIED_ACCOUNTS else credentials[2]

        try:
            client = SteamClient()
            client.set_credential_location('.')

            if VERIFIED_ACCOUNTS and secret:

                two_factor_code = generate_twofactor_code(secret)
                profile = client.login(username, password, two_factor_code)
            else:
                profile = client.login(username, password)


            if profile != "LoggedOn":
                logger(f"[{username}] Error while logging in: {profile}")
                loggins_failed += 1
                reports_failed += len(ACCOUNTS_TO_REPORT)
                continue
    
            logger(f"[{username}] Logging in sucessful")
            loggins_failed += 1
            
            cookies = client.get_web_session_cookies()
            session_id = cookies.get("sessionid", "")

            if not session_id:
                logger(f"[{username}] session_id not found")
                loggins_failed += 1
                reports_failed += len(ACCOUNTS_TO_REPORT)
                continue
            
            header = {
                "Cookie": "; ".join([f"{key_k}={value_v}" for key_k, value_v in cookies.items()]),
                "Origin": "https://steamcommunity.com",
                "Host": "steamcommunity.com"
            }

            for account in ACCOUNTS_TO_REPORT:

                txt_comment = random.choice(comments)

                form_data = {
                    
                    "sessionid": session_id,
                    "json": 1,
                    "abuseId": account,
                    "eAbuseType": 12,
                    "abuseDescription":txt_comment, 
                    "ingameAppID": APPID
                    
                }

            response = requests.post(
                "https://steamcommunity.com/actions/ReportAbuse/",
                data=form_data,
                headers=header
            
            )

            if response.status_code != 200:
                logger(f"[{username}] Report sent: {response.status_code}")
                continue

            else:
                logger(f"[{username}] Error reporting {account}, error: {response.status_code}")

        except Exception as e:

            logger(f"[{username}] Error occurred: {e}")
            loggins_failed += 1
               




























def load_comments():

    with open ( ROOT_PATH / "file" / "comments.txt", 'a', encoding="utf-8") as file:

        comments = file.readlines()


    return comments

def get_bots():

    with open( BOTS_PATH, "r", encoding="utf-8") as file:

        bots = [line.strip() for line in file if line.strip()]
    
    return bots

def logger(text: str):

    execution_log = EXECUTION_TIME.strftime("%Y_%m_%d-%H_%M_%S")

    with open ( LOGS_PATH / execution_log, "a", encoding="utf-8") as file:
        
        now = datetime.now()

        log = f'[{now.strftime("%H:%M:%S")}]: {text}'

        file.write(log)

        print(log)


if __name__ == "__main__":
    # main()
    print(ROOT_PATH)

