import os
import time
import urllib.request
from datetime import datetime
from os import path

import requests
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
        return False

def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()

def printPun():
    print(" _____  _    _ _   _               _____ _____ ")
    print("|  __ \| |  | | \ | |        /\   |  __ \_   _|")
    print("| |__) | |  | |  \| |______ /  \  | |__) || | ")
    print("|  ___/| |  | | . ` |______/ /\ \ |  ___/ | | ")
    print("| |    | |__| | |\  |     / ____ \| |    _| |_ ")
    print("|_|     \____/|_| \_|    /_/    \_\_|   |_____|\n")


def printUI():
    print("\n\n\n\n\n\n\n\n")
    printPun()
    print("Made by : KuebV#0111")
    if not checkAPI():
        print("API is currently offline!")
        exit()

    stats = getStats()
    print(f"API Response Time : {round(stats[0], 1)} ms")
    print(f"Amount of Images : {stats[1]}")
    print("#########################################################")
    print("How would you like to enter in the images?")
    print("1. Reddit\n"
          "2. Via Link\n"
          "3. Quick Fill (Uses Multi-Threading\n"
          "4. Retrieve Image in Range\n"
          "5. Mass Retrieve Image in Range\n"
          "6. Retrieve Images from Subreddit")
    return round(stats[0], 1)


def getTimeEstimate(amount, rate):
    return (float(amount) / rate) * checkAPIPing()


def massFill(threadName, subreddit, timeperiod):
    r = get_reddit(subreddit, "top", "100", timeperiod)
    url = get_image_url(r)
    link = "http://api.abadpun.com/imgStore/url"
    print(f"[{threadName}] - Starting Process at {time.ctime(time.time())}")
    for x in progressBar(url, prefix = 'Progress : ', suffix='Complete : ', length=100):
        try:
            obj = {'url': x}
            req = requests.post(link, data=str(obj))
            time.sleep(0.1)
        except:
            pass

    print(f"[{threadName}] - Completed Process")
    
def massGrab(threadName, subreddit, timeperiod, dir):
    r = get_reddit(subreddit, "top", "100", timeperiod)
    url = get_image_url(r)
    time1 = time.time()
    print(f"[{threadName}] - Started")

    if not path.exists(f"{dir}/{subreddit}"):
        p = os.path.join(dir, subreddit)
        os.mkdir(p)

    for x in url:
        try:
            urlSplit = x.split("/")

            if 'gif' in x:
                if not path.exists(f"{dir}/{subreddit}/{urlSplit[-1]}.gif"):
                    urllib.request.urlretrieve(str(x), f'{dir}/{subreddit}/{urlSplit[-1]}.gif')
            else:
                if not path.exists(f"{dir}/{subreddit}/{urlSplit[-1]}.png"):
                    urllib.request.urlretrieve(str(x), f'{dir}/{subreddit}/{urlSplit[-1]}.png')
        except:
            pass

    time0 = time.time()
    print(f"[{threadName}] - Completed after {(time0 - time1)} Seconds")




def getImage(lowerNum, higherNum, attempts):
    t1 = time.time()
    for i in range(0, int(attempts)):
        link = (
            f"http://api.abadpun.com/imgStore")
        r = requests.get(link)
        data = r.json()
        dataResponse = data['imageUrl']
        amount = data['imageNumber']
        t0 = time.time()

        imageNum = amount.split("/")
        times = t0 - t1

        if int(lowerNum) < int(imageNum[0]) < int(higherNum):
            return [dataResponse, imageNum[0], times]

    return None


def get_reddit(subreddit, listing, entries, timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={entries}&t={timeframe}'
        request = requests.get(base_url, headers={'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()


def getStats():
    t1 = time.time()
    urlTest = "http://api.abadpun.com/imgStore"
    requestTest = requests.get(urlTest)
    dataT = requestTest.json()
    getImage = dataT['imageNumber']
    imageNum = getImage.split("/")

    t0 = time.time()
    secs = t0 - t1

    return [secs, imageNum[1]]


def checkAPIPing():
    t1 = time.time()
    urlTest = "http://api.abadpun.com/imgStore"
    requestTest = requests.get(urlTest)
    dataT = requestTest.json()
    getImage = dataT['imageRating']
    t0 = time.time()
    secs = t0 - t1
    return secs


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
    stats = printUI()
    respTime = stats

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
        print(f"Time Estimate : {round(getTimeEstimate(entries, 4.5), 1)} Seconds")

        for x in url:
            obj = {'url': x}
            req = requests.post(link, data=str(obj))
            timeNow = time.time()
            completed = completed + 1
            if (timeNow - t0) > round(getTimeEstimate(entries, 4.5), 1) and prompt != True:
                print("Process is taking longer than expected... ")
                prompt = True
            elif prompt:
                print(f"[{completed} / {entries}] have been completed")

        t1 = time.time()
        print(f"Done! Process took {t1 - t0} Seconds")
    if '3' in inp:
        print("\n\n\n\n\n\n\n\n\n\n")
        subreddit = input("Subreddit : ")

        massFill('Weekly', subreddit, 'week')
        massFill('Monthly', subreddit, 'month')
        massFill('Yearly', subreddit, 'year')

    if '4' in inp:
        print("\n\n\n\n\n\n\n\n\n\n")
        rangestr = input("Enter your image range : (Ex. 1000 - 2000)")
        attempts = input("Enter how many attempts you're willing to wait for : ")
        if int(attempts) > 500:
            print("Estimated Time : <10 Seconds")
        else:
            print(f"Estimated Time : {round(getTimeEstimate(attempts, 2.7))} Seconds")

        r = rangestr.split("-")
        lowerRange = str(r[0]).strip()
        upperRange = str(r[1]).strip()

        t1 = time.time()

        im = getImage(lowerRange, upperRange, attempts)
        if im is None:
            print("Ran out of attempts")
            t0 = time.time()
            print("Process took {} Seconds".format((t1 - t0)))
        else:
            # img = Image.open(requests.get(im, stream=True).raw)
            imgLink = im[0]
            imgNum = im[1]
            if 'gif' in imgLink:
                if not path.exists(f"Images/IMG-{str(imgNum)}.gif"):
                    urllib.request.urlretrieve(str(imgLink), f'Images/IMG-{str(imgNum)}.gif')
                    img = Image.open(f'Images/IMG-{str(imgNum)}.gif')
                    img.show()
                else:
                    print("File Already Exists")
                    img = Image.open(f'Images/IMG-{str(imgNum)}.gif')
                    img.show()
            else:
                if not path.exists(f"Images/IMG-{str(imgNum)}.png"):
                    urllib.request.urlretrieve(str(imgLink), f'Images/IMG-{str(imgNum)}.png')
                    img = Image.open(f'Images/IMG-{str(imgNum)}.png')
                    img.show()
                else:
                    print("File Already Exists")
                    img = Image.open(f'Images/IMG-{str(imgNum)}.png')
                    img.show()

    if '5' in inp:
        print("\n\n\n\n\n\n\n\n\n\n")
        rangestr = input("Enter your image range : (Ex. 1000 - 2000)")
        attempts = input("Enter how many images you want : ")
        if (float(respTime) * float(attempts)) > 300:
            print(f"Estimated Time : {(float(respTime) * float(attempts)) / 60} Minutes")
        else:
            print(f"Estimated Time : {(float(respTime) * float(attempts))}")

        completion = 0

        r = rangestr.split("-")
        lowerRange = str(r[0]).strip()
        upperRange = str(r[1]).strip()
        for i in range(0, int(attempts)):
            im = getImage(lowerRange, upperRange, 100)
            if im is not None:
                imgLink = im[0]
                imgNum = im[1]
                findTime = im[2]
                if 'gif' in imgLink:
                    if not path.exists(f"Images/IMG-{str(imgNum)}.gif"):
                        urllib.request.urlretrieve(str(imgLink), f'Images/IMG-{str(imgNum)}.gif')

                else:
                    if not path.exists(f"Images/IMG-{str(imgNum)}.png"):
                        urllib.request.urlretrieve(str(imgLink), f'Images/IMG-{str(imgNum)}.png')
                completion = completion + 1
                print(f"[{completion}/{attempts}] has been completed in {findTime} seconds")
    if '6' in inp:
        subred = input("Subreddit to Grab : ")
        massGrab("Weekly", subred, "week", "RedditGrab")
        massGrab("Monthly", subred, "month", "RedditGrab")
        massGrab("Yearly", subred, "year", "RedditGrab")
        print("Done")

    else:
        print("Unknown Fuckery")
