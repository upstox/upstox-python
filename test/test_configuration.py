# coding: utf-8
"""Unit tests for Configuration sandbox/live switching (no network)."""

import unittest

from upstox_client.configuration import Configuration


class TestConfigurationSandboxSwitch(unittest.TestCase):
    def setUp(self):
        Configuration._default = None

    def tearDown(self):
        Configuration._default = None

    def test_sandbox_flag_honored_after_live_default_cached(self):
        live = Configuration()
        self.assertEqual(live.host, "https://api.upstox.com")
        sandbox = Configuration(sandbox=True)
        self.assertTrue(sandbox.sandbox)
        self.assertEqual(sandbox.host, "https://api-sandbox.upstox.com")
        self.assertEqual(sandbox.order_host, "https://api-sandbox.upstox.com")

    def test_positional_sandbox_arg_honored(self):
        Configuration()
        sandbox = Configuration(True)
        self.assertEqual(sandbox.host, "https://api-sandbox.upstox.com")

    def test_bare_calls_still_share_cached_default(self):
        first = Configuration()
        second = Configuration()
        self.assertIsNot(first, second)
        self.assertEqual(first.host, second.host)
        self.assertEqual(first.host, "https://api.upstox.com")

    def test_explicit_live_after_sandbox(self):
        Configuration(sandbox=True)
        live = Configuration(sandbox=False)
        self.assertEqual(live.host, "https://api.upstox.com")
        self.assertEqual(live.order_host, "https://api-hft.upstox.com")


if __name__ == "__main__":
    unittest.main()
