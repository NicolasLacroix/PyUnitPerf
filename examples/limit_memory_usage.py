"""
This file contains a class that illustrates the use of the
memory limit assertions using the pyunitperf.memory package.
"""
import unittest

from pyunitperf.memory import memory_not_exceed


class TestLimitMemoryUsage(unittest.TestCase):
    """
    This class illustrates the use of the memory_not_exceed decorator.
    """
    @memory_not_exceed(threshold=0)
    def test_memory_usage_exceed(self):
        """
        This test won't pass due to a very low threshold.
        """
        return list(range(1000)) * 1

    @memory_not_exceed(threshold=1000)
    def test_memory_usage_not_exceed(self):
        """
        This test passes due to a very high threshold.
        """
        return list(range(1000)) * 1


if __name__ == '__main__':
    unittest.main()
