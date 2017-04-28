#! usr/bin/python3

import abc
import logging
import unittest
import itertools
import collections

import sliding


Request = collections.namedtuple("Request", ["off", "seq"])
Response = collections.namedtuple("Response", ["seq"])


class Protocol(sliding.Protocol):
    __metaclass__ = abc.ABCMeta

    _logger = logging.getLogger("sliding.tests.protocol")

    def __init__(self):
        self.send_seq = itertools.count()
        self.recv_seq = itertools.count()
        self.handled = []

    def send(self, fields):
        req = Request(fields, next(self.send_seq))
        self._logger.info("sending {}".format(req))
        return req.seq

    def recv(self, timeout):
        try:
            resp = Response(next(self.recv_seq))
        except StopIteration:
            raise TimeoutError
        self.handled.append(resp.seq)
        self._logger.info("returning {}".format(resp))
        return resp

    def match(self, resp, cookie):
        return resp.seq == cookie


class TestCase(unittest.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        handler = logging.FileHandler(
            "tests/output/{}".format(type(self).__name__), "w")
        fmt = "%(asctime)s [%(levelname)8s] %(name)s: %(message)s"
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        logging.root.addHandler(handler)
        logging.root.setLevel(logging.DEBUG)
