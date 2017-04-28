#! /usr/bin/python3

import sliding

import helper


class TestSmallTransfer(helper.TestCase):

    def test_small_transfer(self):
        protocol = helper.Protocol()
        offs = range(7)
        sliding.run_sliding_window(protocol, None, 10, 0, iter(offs), 4)
        self.assertSequenceEqual(offs, protocol.handled)
