#! usr/bin/python3

import logging
import unittest
import itertools
import collections

import sliding


Request = collections.namedtuple("Request", ["off", "seq"])
Response = collections.namedtuple("Response", ["seq"])


class Protocol(sliding.Protocol):

    _logger = logging.getLogger("sliding.tests.protocol")

    def __init__(self):
        self.send_seq = itertools.count()
        self.recv_seq = itertools.count()
        self.ongoing = []
        self.handled = []

    def send(self, state, fields):
        self.ongoing.append(fields)
        req = Request(fields, next(self.send_seq))
        self._logger.info("sending %s", req)
        return req.seq

    def should_drop(self, resp):
        return False

    def recv(self, state, timeout):
        resp = Response(next(self.recv_seq))
        if self.should_drop(resp):
            self._logger.info("dropping %s", resp)
            self.ongoing.pop(0)
            raise TimeoutError()
        self.handled.append(self.ongoing.pop(0))
        self._logger.info("returning %s", resp)
        return resp.seq


class TestCase(unittest.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self._handler = logging.FileHandler(
            "tests/output/{}".format(type(self).__name__), "w")
        fmt = "%(asctime)s [%(levelname)8s] %(name)s: %(message)s"
        formatter = logging.Formatter(fmt)
        self._handler.setFormatter(formatter)
        logging.root.addHandler(self._handler)
        logging.root.setLevel(logging.DEBUG)

    def tearDown(self):
        super(TestCase, self).tearDown()
        self._handler.close()
        logging.root.removeHandler(self._handler)
