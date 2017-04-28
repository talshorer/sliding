#! /usr/bin/python3

import sliding

import helper


class TestRetransmission(helper.TestCase):

    class Protocol(helper.Protocol):

        def should_drop(self, resp):
            return resp.seq == 3

    def test_retrnasmission(self):
        protocol = self.Protocol()
        offs = range(20)
        sliding.run_sliding_window(protocol, None, 10, 1, iter(offs), 4)
        self.assertSequenceEqual(offs, sorted(protocol.handled))
