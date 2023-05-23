from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


def check_url(url, timeout=5):
    if urlsplit(url).scheme not in ("http", "https"):
        raise ValueError("Only HTTP links can be checked")
    try:
        try:
            with urlopen(Request(url, method="HEAD"), timeout=timeout) as response:
                return response.status, None
        except HTTPError as error:
            if error.code != 405:
                raise
        with urlopen(Request(url, method="GET"), timeout=timeout) as response:
            return response.status, None
    except HTTPError as error:
        return error.code, "HTTP %s" % error.code
    except (URLError, OSError) as error:
        return None, str(error)
