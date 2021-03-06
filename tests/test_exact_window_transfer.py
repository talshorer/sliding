#! /usr/bin/python3

import sliding

import helper


class TestExactWindowTransfer(helper.TestCase):

    def test_exact_window_transfer(self):
        protocol = helper.Protocol()
        offs = range(10)
        sliding.run_sliding_window(protocol, None, 10, 0, iter(offs), 4)
        self.assertSequenceEqual(offs, protocol.handled)
