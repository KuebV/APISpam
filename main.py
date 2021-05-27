import time
from datetime import datetime
import requests
import pyfiglet

def printUI():
    ascii_banner = pyfiglet.figlet_format("API-SPAM", "big")
    print("\n\n\n\n\n\n\n\n" + ascii_banner)
    print("Made by : KuebV#0111")
    print("#########################################################")
    print("How would you like to enter in the images?")
    print("1. Reddit\n"
          "2. Via Link")

def get_reddit(subreddit,listing,entries,timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={entries}&t={timeframe}'
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
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

        t0 = time.time()

        print("Starting Process...")

        for x in url:
            obj = {'url': x}
            req = requests.post(link, data=str(obj))

        t1 = time.time()
        print(f"Done! Process took {t1 - t0} Seconds")
