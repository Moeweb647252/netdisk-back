from typing import Dict
class DownloadLink:
  expiration_date:int
  token:str
  real_path:str
  
  def __init__(self, expiration_date, token, real_path) -> None:
    self.expiration_date = expiration_date
    self.token = token
    self.real_path = real_path

class GlobalStorage:
  downloadLinks:Dict[str, DownloadLink] = {}
  

globalStorage = GlobalStorage()