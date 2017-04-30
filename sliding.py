#! /usr/bin/python3

import abc
import collections


def uptime():
    with open("/proc/uptime") as f:
        return float(f.read().split()[0])


Packet = collections.namedtuple("Packet", ["end_time", "retrans", "fields"])


class Protocol(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def send(self, state, fields):
        "send a request according to given fields and returns a cookie"

    @abc.abstractmethod
    def recv(self, state, timeout):
        """
        receives and handles a response or raises TimeoutError
        returns response, cookie (matching previous request's cookie)
        """


class NonmatchingResponse(Exception):
    pass


def __queue(window, protocol, state, retrans, fields, timeout):
    cookie = protocol.send(state, fields)
    window[cookie] = Packet(uptime() + timeout, retrans, fields)


def _queue(window, protocol, state, retrans, iterator, timeout):
    try:
        fields = next(iterator)
    except StopIteration:
        return
    __queue(window, protocol, state, retrans, fields, timeout)


def run_sliding_window(protocol, state, size, retrans, iterator,
                       timeout):
    window = collections.OrderedDict()
    for _ in range(size):
        _queue(window, protocol, state, retrans, iterator, timeout)
    while window:
        try:
            resp, cookie = protocol.recv(state,
                                         next(iter(window.values())).end_time -
                                         uptime())
        except TimeoutError:
            packet = window.popitem(False)[1]
            if not packet.retrans:
                raise
            __queue(window, protocol, state, packet.retrans - 1,
                    packet.fields, timeout)
            continue
        try:
            window.pop(cookie)
        except KeyError:
            raise NonmatchingResponse(resp)
        _queue(window, protocol, state, retrans, iterator, timeout)
