import grequests


def async_url_response(urls, timeout):
    for url in urls:
        yield grequests.get(url, timeout=timeout)
