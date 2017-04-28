#! usr/bin/python3

import abc
import itertools
import collections

import sliding


Request = collections.namedtuple("Request", ["off"])
Response = collections.namedtuple("Response", ["seq"])


class Protocol(sliding.Protocol):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.send_seq = itertools.count()
        self.recv_seq = itertools.count()
        print()

    def send(self, fields):
        req = Request(fields)
        print("sending {}".format(req))
        return next(self.send_seq)

    def recv(self, timeout):
        try:
            resp = Response(next(self.recv_seq))
        except StopIteration:
            raise TimeoutError
        print("returning {}".format(resp))
        return resp

    def match(self, resp, cookie):
        return resp.seq == cookie


class SlidingWindow(sliding.SlidingWindow):

    def __init__(self, *args, **kw):
        super(SlidingWindow, self).__init__(*args, **kw)
        self.handled = []

window = SlidingWindow(10, 4)
