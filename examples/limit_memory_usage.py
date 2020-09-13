"""
This file contains classes that illustrate the use of the
pyunitperf.memory package.
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
        count = 0
        return [count * i for i in range(1000000)]

    @memory_not_exceed(threshold=1000)
    def test_memory_usage_not_exceed(self):
        """
        This test pass due to a very high threshold.
        """
        count = 0
        return [count * i for i in range(1000000)]


if __name__ == '__main__':
    unittest.main()
