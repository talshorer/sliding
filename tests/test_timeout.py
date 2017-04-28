#! /usr/bin/python3

import sliding

import helper


class TestTimeout(helper.TestCase):

    class Protocol(helper.Protocol):

        def should_drop(self, resp):
            # always drop a request with this offset
            return self.ongoing[0] == 3

    def test_timeout(self):
        protocol = self.Protocol()
        offs = range(20)
        with self.assertRaises(TimeoutError):
            sliding.run_sliding_window(protocol, None, 10, 1, iter(offs), 4)
