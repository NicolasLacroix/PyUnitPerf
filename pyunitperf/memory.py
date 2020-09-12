"""
This package is dedicated to all the memory aspects testing.
"""
import tracemalloc
from functools import wraps
from typing import Callable


def _get_overload(snapshot: tracemalloc.Snapshot, key_type: str = 'lineno', threshold: int = 10):
    """
    Returns a list of statistics that exceed the given threshold.
    :param snapshot: snapshot to analyze
    :param key_type: key used to order the snapshot's statistics
    :param threshold: threshold not to exceed
    :return: a list of statistics that exceed the given threshold
    """
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    stats = snapshot.statistics(key_type)
    return [stat for stat in stats if stat.size >= threshold]


def memory_not_exceed(threshold: int = 10):
    """
    Tests that the memory taken up by the given function
    doesn't exceed the given threshold.
    :param threshold: threshold in bytes
    """

    def test_memory_decorator(func: Callable):
        @wraps(func)
        def test_memory_wrapper(*args):
            tracemalloc.start()
            func(*args)
            snapshot = tracemalloc.take_snapshot()
            assert not _get_overload(snapshot, threshold=threshold), "Threshold reached"

        return test_memory_wrapper

    return test_memory_decorator
