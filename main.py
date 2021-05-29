import string
import time
import urllib.request
from datetime import datetime
from random import choice, randint

import requests
import pyfiglet
from threading import Thread
from PIL import Image


def checkAPI():
    try:
        urlTest = "http://api.abadpun.com/imgStore"
        requestTest = requests.get(urlTest)
        dataT = requestTest.json()
        getImage = dataT['imageRating']
        return True
    except Exception as e:
        print(f"EXCEPTION : {e}")
        return False


def printUI():
    ascii_banner = pyfiglet.figlet_format("API-SPAM", "big")
    print("\n\n\n\n\n\n\n\n" + ascii_banner)
    print("Made by : KuebV#0111")
    print(f"[API Online : {checkAPI()}]")
    print("#########################################################")
    print("How would you like to enter in the images?")
    print("1. Reddit\n"
          "2. Via Link\n"
          "3. Quick Fill (Uses Multi-Threading\n"
          "4. Retrieve Image in Range")


def getTimeEstimate(amount):
    return float(amount) / 3.5

def postWeekly(threadName, subreddit):
    r = get_reddit(subreddit, "top", "100", "week")
    url = get_image_url(r)
    link = "http://api.abadpun.com/imgStore/url"
    print(f"[{threadName}] - Starting Process at {time.ctime(time.time())}")
    for x in url:
        obj = {'url': x}
        req = requests.post(link, data=str(obj))

    print(f"[{threadName}] - Completed Process")


def postMonthly(threadName, subreddit):
    r = get_reddit(subreddit, "top", "100", "month")
    url = get_image_url(r)
    link = "http://api.abadpun.com/imgStore/url"
    print(f"[{threadName}] - Starting Process at {time.ctime(time.time())}")
    for x in url:
        obj = {'url': x}
        req = requests.post(link, data=str(obj))

    print(f"[{threadName}] - Completed Process")


def postYearly(threadName, subreddit):
    r = get_reddit(subreddit, "top", "100", "year")
    url = get_image_url(r)
    link = "http://api.abadpun.com/imgStore/url"
    print(f"[{threadName}] - Starting Process at {time.ctime(time.time())}")
    for x in url:
        obj = {'url': x}
        req = requests.post(link, data=str(obj))

    print(f"[{threadName}] - Completed Process")

def getImage(lowerNum, higherNum, attempts):
    for i in range(0, int(attempts)):
        link = (
            f"http://api.abadpun.com/imgStore")
        r = requests.get(link)
        data = r.json()
        dataResponse = data['imageUrl']
        amount = data['imageNumber']

        imageNum = amount.split("/")

        if int(lowerNum) < int(imageNum[0]) < int(higherNum):
            return dataResponse

    return None


def get_reddit(subreddit, listing, entries, timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={entries}&t={timeframe}'
        request = requests.get(base_url, headers={'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()


def get_post_titles(r):
    posts = []
    for post in r['data']['children']:
        x = post['data']['title']
        posts.append(x)
    return posts


def get_image_url(r):
    posts = []
    for post in r['data']['children']:
        x = post['data']['url']
        posts.append(x)
    return posts


def is_video(r):
    video = r['data']['children'][0]['data']['is_video']
    if video:
        return True
    else:
        return False


fuck = False
while not fuck:
    printUI()

    inp = input("Choice (Ex. 1 or 2) : ")
    if '2' in inp:
        link = input("Input the link for the photo (ex . discord / img address)")
        loop = input("How many times would you like this to be looped?")
        completed = 0
        for i in range(0, int(loop)):
            inputLink = "http://api.abadpun.com/imgStore/url"
            obj = {'url': link}
            req = requests.post(inputLink, data=str(obj))
            completed = completed + 1
            print(f"({completed} / {loop}) has been completed")

    if '1' in inp:
        getLink = (
            f"http://api.abadpun.com/imgStore")
        r = requests.get(getLink)
        data = r.json()
        dataResponse = data['imageNumber']
        getNum = str(dataResponse).split("/")

        now = datetime.utcnow()
        print("\n\n\n\n\n\n\n\n\n\n")
        print(f"There are currently {getNum[1]} entries in the database")
        subreddit = input("Subreddit : ")
        entries = input("How many entries would you like : ")
        listing = input("Listing (Ex. top, hot, rising) : ")
        timeframe = input("Timeframe (Ex. day, week, month, year) : ")

        r = get_reddit(subreddit, listing, entries, timeframe)
        url = get_image_url(r)
        link = "http://api.abadpun.com/imgStore/url"

        completed = 0
        prompt = False

        t0 = time.time()

        print("Starting Process...")
        print(f"Time Estimate : {round(getTimeEstimate(entries), 1)} Seconds")

        for x in url:
            obj = {'url': x}
            req = requests.post(link, data=str(obj))
            timeNow = time.time()
            completed = completed + 1
            if (timeNow - t0) > round(getTimeEstimate(entries), 1) and prompt != True:
                print("Process is taking longer than expected... ")
                prompt = True
            elif prompt:
                print(f"[{completed} / {entries}] have been completed")

        t1 = time.time()
        print(f"Done! Process took {t1 - t0} Seconds")
    if '3' in inp:
        print("\n\n\n\n\n\n\n\n\n\n")
        subreddit = input("Subreddit : ")

        # Not going to lie, this probably isn't used properly, although it does make things easier for myself
        Thread(target=postWeekly("ThreadOne", subreddit)).start()
        Thread(target=postMonthly("ThreadTwo", subreddit)).start()
        Thread(target=postMonthly("ThreadThree", subreddit)).start()
        print("All Threads Done")
    if '4' in inp:
        print("\n\n\n\n\n\n\n\n\n\n")
        rangestr = input("Enter your image range : (Ex. 1000 - 2000)")
        attempts = input("Enter how many attempts you're willing to wait for : ")
        r = rangestr.split("-")
        lowerRange = str(r[0]).strip()
        upperRange = str(r[1]).strip()

        im = getImage(lowerRange, upperRange, attempts)
        if im is None:
            print("Ran out of attempts")
        else:
            # img = Image.open(requests.get(im, stream=True).raw)
            characters = string.ascii_letters
            fileName = "".join(choice(characters) for x in range(randint(8, 16)))
            urllib.request.urlretrieve(im, f'{fileName}.png')
            img = Image.open(f"{fileName}.png")
            img.show()

    else:
        print("Unknown Fuckery")
