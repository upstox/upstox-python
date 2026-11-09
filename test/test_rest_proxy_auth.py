# coding: utf-8

from __future__ import absolute_import

import socket
import threading
import unittest

import upstox_client
from upstox_client.rest import RESTClientObject, _split_proxy_auth


class TestSplitProxyAuth(unittest.TestCase):
    """Credentials in Configuration.proxy must reach the proxy as a header"""

    def test_no_credentials(self):
        url, headers = _split_proxy_auth('http://proxy.example.com:3128')
        self.assertEqual(url, 'http://proxy.example.com:3128')
        self.assertIsNone(headers)

    def test_credentials_moved_to_header(self):
        url, headers = _split_proxy_auth('http://user:pass@proxy.example.com:3128')
        self.assertEqual(url, 'http://proxy.example.com:3128')
        self.assertEqual(headers, {'proxy-authorization': 'Basic dXNlcjpwYXNz'})

    def test_url_encoded_credentials(self):
        # user "us@er", password "p:ss"
        url, headers = _split_proxy_auth('http://us%40er:p%3Ass@proxy.example.com:3128')
        self.assertEqual(url, 'http://proxy.example.com:3128')
        self.assertEqual(headers, {'proxy-authorization': 'Basic dXNAZXI6cDpzcw=='})

    def test_ipv6_proxy_host(self):
        url, headers = _split_proxy_auth('http://user:pass@[2001:db8::1]:3128')
        self.assertEqual(url, 'http://[2001:db8::1]:3128')
        self.assertIsNotNone(headers)


class TestProxyManagerSendsAuth(unittest.TestCase):

    def setUp(self):
        self.received = []
        self.server = socket.socket()
        self.server.bind(('127.0.0.1', 0))
        self.server.listen(5)
        self.port = self.server.getsockname()[1]
        thread = threading.Thread(target=self._serve)
        thread.daemon = True
        thread.start()

    def tearDown(self):
        self.server.close()

    def _serve(self):
        # Fake proxy: record the CONNECT request, then refuse it.
        while True:
            try:
                conn, _ = self.server.accept()
            except OSError:
                return
            self.received.append(conn.recv(4096).decode('latin-1'))
            conn.sendall(b'HTTP/1.1 407 Proxy Authentication Required\r\nContent-Length: 0\r\n\r\n')
            conn.close()

    def test_connect_carries_proxy_authorization(self):
        config = upstox_client.Configuration()
        config.proxy = 'http://user:pass@127.0.0.1:%d' % self.port
        client = RESTClientObject(config)
        with self.assertRaises(Exception):
            client.pool_manager.request('GET', 'https://api.upstox.com/v2/user/profile', retries=False)
        self.assertTrue(self.received)
        headers = dict(line.split(': ', 1) for line in self.received[0].split('\r\n')[1:] if ': ' in line)
        headers = dict((k.lower(), v) for k, v in headers.items())
        self.assertEqual(headers.get('proxy-authorization'), 'Basic dXNlcjpwYXNz')


if __name__ == '__main__':
    unittest.main()
