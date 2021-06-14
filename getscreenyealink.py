import requests
from config import *


def getscreenyealink(ipyealink="10.45.4.172", macyealink="1q2w3e4r5t6y"):
    filename = "static/screenshot/" + macyealink + ".jpg"
    f = open(filename, "wb")
    ufr = requests.get("http://" + loginyealink + ":" + passyealink + "@" + ipyealink + "/screencapture/download")
    f.write(ufr.content)
    f.close()


# getscreenyealink()
