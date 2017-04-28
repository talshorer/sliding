#! /usr/bin/python3

import sliding

import helper


class TestCommonCase(helper.TestCase):

    def test_common_case(self):
        protocol = helper.Protocol()
        seqs = range(100)
        sliding.run_sliding_window(protocol, None, 10, 4, iter(seqs), 4)
        self.assertSequenceEqual(seqs, protocol.handled)
