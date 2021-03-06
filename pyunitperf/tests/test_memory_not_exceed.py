"""
This package contains unit tests for pyunitperf.memory.
"""
import tracemalloc
import unittest
from collections.abc import Iterable
from tracemalloc import Snapshot

from pyunitperf.memory import _get_overload, memory_not_exceed, _filter_snapshot, DEFAULT_FILTERS


class TestMemoryNotExceed(unittest.TestCase):
    """
    This class tests the memory_not_exceed decorator and associated functions
    in the package pyunitperf.memory.
    """

    def test_filter_snapshot(self):
        """
        Tests the _filter_snapshot function.
        """

        for exclude in [None] + [filter.filename_pattern  for filter in DEFAULT_FILTERS]:
            with self.subTest("test _filter_snapshot with empty statistics and exclude={}"
                                      .format(exclude), exclude=exclude):
                tracemalloc.start()
                list(range(1000000))
                snapshot = tracemalloc.take_snapshot()
                tracemalloc.stop()
                filtered_snapshot = _filter_snapshot(snapshot, exclude=exclude)
                stats_files = [
                    frame.filename for stat in filtered_snapshot.statistics("lineno")
                    for frame in stat.traceback
                ]
                if isinstance(exclude, str):
                    self.assertNotIn(exclude, stats_files)
                elif isinstance(exclude, Iterable):
                    for e in exclude:
                        self.assertNotIn(e, stats_files)

    def test_get_overload(self):
        """
        Tests the _get_overload function.
        """
        with self.subTest("test _get_overload with empty statistics"):
            snapshot = Snapshot((), 0)
            expected = []
            result = _get_overload(snapshot, threshold=10)
            self.assertListEqual(expected, result)
        with self.subTest("test _get_overload with filled statistics and low threshold"):
            tracemalloc.start()
            list(range(1000000))
            snapshot = tracemalloc.take_snapshot()
            tracemalloc.stop()
            expected = snapshot.statistics("lineno")
            result = _get_overload(snapshot, threshold=0)
            self.assertListEqual(expected, result)
        with self.subTest("test _get_overload with filled statistics and high threshold"):
            tracemalloc.start()
            list(range(0))
            snapshot = tracemalloc.take_snapshot()
            tracemalloc.stop()
            expected = []
            result = _get_overload(snapshot, threshold=100)
            self.assertListEqual(expected, result)

    def test_memory_not_exceed_decorator(self):
        """
        Tests the memory_not_exceed decorator.
        """

        @memory_not_exceed(threshold=0)
        def exceed():
            """
            This function exceeds the specified threshold and
            should raise an AssertionError.
            """
            return list(range(10)) * 1

        with self.subTest("test_memory_not_exceed_decorator with failure"):
            self.assertRaises(AssertionError, exceed)


        @memory_not_exceed(threshold=100)
        def not_exceed():
            """
            This function doesn't exceed the specified threshold and
            shouldn't raise an AssertionError.
            """

        with self.subTest("test_memory_not_exceed_decorator without failure"):
            not_exceed()


if __name__ == '__main__':
    unittest.main()
