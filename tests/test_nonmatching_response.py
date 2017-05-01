#! /usr/bin/python3

import sliding

import helper


class TestNonmatchingResponse(helper.TestCase):

    class Protocol(helper.Protocol):

        def recv(self, state, timeout):
            cookie = super(TestNonmatchingResponse.Protocol, self).recv(
                state, timeout)
            if cookie == 3:
                cookie = -1
            return cookie

    def test_nonmatching_response(self):
        protocol = self.Protocol()
        offs = range(20)
        with self.assertRaises(sliding.NonmatchingResponse):
            sliding.run_sliding_window(protocol, None, 10, 1, iter(offs), 4)
