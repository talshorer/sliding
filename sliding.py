#! /usr/bin/python3

import abc
import collections


def uptime():
    with open("/proc/uptime") as f:
        return float(f.read().split()[0])


Packet = collections.namedtuple("Packet", ["end_time", "retrans", "fields",
                                           "cookie"])


class Protocol(object):
    __metaclass__ = abc.ABCMeta

    class TimeoutError(Exception):
        pass

    @abc.abstractmethod
    def send(self, fields):
        "send a request according to given fields"

    @abc.abstractmethod
    def recv(self, state, timeout):
        "returns a response after handling it or raises TimeoutError"

    @abc.abstractmethod
    def match(self, resp, cookie):
        "decide whether a given response matches a former request by cookie"


class SlidingWindow(object):

    class NonmatchingResponse(Exception):
        pass

    def __init__(self, size, retrans):
        self.size = size
        self.retrans = retrans

    def _queue(self, window, protocol, iterator, timeout):
        try:
            fields = next(iterator)
        except StopIteration:
            return
        cookie = protocol.send(fields)
        window.append(Packet(uptime() + timeout, self.retrans, fields, cookie))

    def run(self, protocol, state, iterator, timeout):
        window = []
        for _ in range(self.size):
            self._queue(window, protocol, iterator, timeout)
        while window:
            try:
                resp = protocol.recv(window[0].end_time - uptime())
            except protocol.TimeoutError:
                packet = window.pop(0)
                packet -= 1
                if not packet.retrans:
                    raise
                packet.end_time = uptime() + timeout
                window.append(packet)
                continue
            for i, packet in enumerate(window):
                if protocol.match(resp, packet.cookie):
                    window.pop(i)
                    break
            else:  # no match
                raise self.NonmatchingResponse(resp)
            self._queue(window, protocol, iterator, timeout)
