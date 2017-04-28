#! /usr/bin/python3

import unittest

import helper


class TestCommonCase(unittest.TestCase):

    def test_common_case(self):
        protocol = helper.Protocol()
        helper.window.run(protocol, None, iter(range(100)), 4)
