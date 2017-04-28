#! /usr/bin/python3

import sliding

import helper


class TestSmallTransfer(helper.TestCase):

    def test_small_window_transfer(self):
        protocol = helper.Protocol()
        seqs = range(7)
        sliding.run_sliding_window(protocol, None, 10, 0, iter(seqs), 4)
        self.assertSequenceEqual(seqs, protocol.handled)
