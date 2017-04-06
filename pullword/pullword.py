#!/usr/bin/env python
# coding=utf-8

from requests.packages.urllib3.connectionpool import HTTPConnectionPool


def _make_request(self, conn, method, url, **kwargs):
    response = self._old_make_request(conn, method, url, **kwargs)
    sock = getattr(conn, 'sock', False)
    if sock:
        setattr(response, 'peer', sock.getpeername())
    else:
        setattr(response, 'peer', None)
    return response

HTTPConnectionPool._old_make_request = HTTPConnectionPool._make_request
HTTPConnectionPool._make_request = _make_request

import requests
post_url = "http://api.pullword.com/post.php"


class ServerError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def split_word(words):
    words = words.split()
    words_list = []
    for i in words:
        if len(i) == 0:
            continue
        words_list.append(i.split(":"))
    return words_list


def pullword(source="", threshold=0, debug=1):
    payload = {"source": source.encode(
        "utf8"), "param1": threshold, "param2": debug}
    pw = requests.post(post_url, data=payload)
    print pw.url
    print pw.raw._original_response.peer

    if pw.status_code != 200:
        raise ServerError("server return %s" % pw.status_code)
    print pw.content
    return split_word(pw.content)
