import unittest
from .BaseTest import BaseTestCase


class Test(BaseTestCase):
    def test(self):
      from deephaven_plugin_ptt_input import decode_text_command
      result = decode_text_command("test")
      self.assertEqual(result, "test")


if __name__ == "__main__":
    unittest.main()
