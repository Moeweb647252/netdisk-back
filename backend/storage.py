from typing import Dict


class DownloadLink:
    path: str
    token: str
    realpath: str


class globalStorage:
    downloadLinks: Dict[str, DownloadLink] = {}
