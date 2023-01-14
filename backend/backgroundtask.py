import threading
from .storage import *
import time

def checkDownloadTokenExpiration():
  for i in globalStorage.downloadLinks.keys():
    if globalStorage.downloadLinks[i].expiration_date < time.time():
      globalStorage.downloadLinks.pop(i)
  time.sleep(100)

threading.Thread(target=checkDownloadTokenExpiration).start()