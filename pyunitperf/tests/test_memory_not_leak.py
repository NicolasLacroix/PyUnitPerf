"""
This package contains unit tests for pyunitperf.memory.
"""
import unittest

from pyunitperf.memory import memory_not_leak


class TestMemoryNotLeak(unittest.TestCase):
    """
    This class tests the memory_not_leak decorator and associated functions
    in the package pyunitperf.memory.
    """
    leaking_list = []

    def test_get_leaks(self):
        """
        Tests the _get_leaks function.
        """

    def test_memory_not_leak_decorator(self):
        """
        Tests the memory_not_leak decorator.
        """
        @memory_not_leak()
        def leaks():
            """
            Generates a memory leak involving the leaking_list.
            """
            self.leaking_list.append("will leak")

        with self.subTest("test_memory_not_leak_decorator with failure"):
            self.assertRaises(AssertionError, leaks)

        @memory_not_leak()
        def not_leaks():
            """
            This function doesn't leak and shouldn't raise
            an AssertionError.
            """

        with self.subTest("test_memory_not_leak_decorator without failure"):
            not_leaks()

        @memory_not_leak(threshold=10)
        def leaks_no_failure():
            """
            This function's memory leak doesn't exceed the specified threshold and
            shouldn't raise an AssertionError.
            """
            self.leaking_list.append("will leak")

        with self.subTest("test_memory_not_leak_decorator with memory leak but "
                          "no failure (high threshold)"):
            leaks_no_failure()


if __name__ == '__main__':
    unittest.main()
