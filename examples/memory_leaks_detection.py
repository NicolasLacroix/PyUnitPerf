"""
This file contains a class that illustrates the use of the
memory leaks assertions using the pyunitperf.memory package.
"""
import unittest

from pyunitperf.memory import memory_not_leak


class TetsMemoryLeaksDetection(unittest.TestCase):
    """
    This class illustrates the use of the memory_not_leak decorator.
    """
    leaking_list = []

    def leak(self):
        """
        Generates a memory leak involving the leaking_list.
        """
        self.leaking_list.append("will leak")

    @memory_not_leak()
    def test_memory_leaks(self):
        """
        This test won't pass due to a memory leak.
        """
        self.leak()

    @memory_not_leak()
    def test_memory_not_leak(self):
        """
        This test passes due to the absence of memory leak.
        """
        pass


if __name__ == '__main__':
    unittest.main()
