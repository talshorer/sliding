#! /usr/bin/python3

import sliding

import helper


class TestCommonCase(helper.TestCase):

    def test_common_case(self):
        protocol = helper.Protocol()
        offs = range(100)
        sliding.run_sliding_window(protocol, None, 10, 0, iter(offs), 4)
        self.assertSequenceEqual(offs, protocol.handled)
