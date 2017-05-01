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
        """Sends a request according to given fields and returns a cookie."""

    @abc.abstractmethod
    def recv(self, state, timeout):
        """
        Rreceives and handles a response or raises TimeoutError.
        Returns a cookie (matching previous request's cookie).
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
    """
    Runs a sliding window, calling back protocol when necessary.
    Arguments:
    protocol -- stateless object that exposes the Protocol class interface.
    state -- a state object that's passed to protocol's methods.
        this is useful for cases where the same protocol object is used
        concurrently with multiple state objects.
    size -- size of the sliding window, in packets.
    retrans -- max retransmissions for each packet before raising TimeoutError.
    iterator -- an iterable object from which to extract fields for packets.
        each call to protocol.send will provide one object from this iterator,
        which can be of any arbitrary type.
    timeout -- timeout for a single packet for a single transmission.
        The actual timeout for a packet is therefore (timeout * retrans).
    """
    window = collections.OrderedDict()
    for _ in range(size):
        _queue(window, protocol, state, retrans, iterator, timeout)
    while window:
        try:
            first_cookie, packet = next(iter(window.items()))
            new_cookie = protocol.recv(state, packet.end_time - uptime())
        except TimeoutError:
            window.pop(first_cookie)
            if not packet.retrans:
                raise
            __queue(window, protocol, state, packet.retrans - 1,
                    packet.fields, timeout)
            continue
        try:
            window.pop(new_cookie)
        except KeyError:
            raise NonmatchingResponse(new_cookie)
        _queue(window, protocol, state, retrans, iterator, timeout)
