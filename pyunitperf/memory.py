"""
This package is dedicated to all the memory aspects testing.
"""
import tracemalloc
from copy import deepcopy
from functools import wraps
from typing import Callable, Iterable, Optional
import collections.abc as abc

ExcludeType = Optional[Iterable[str]]

DEFAULT_FILTERS = {
    tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
    tracemalloc.Filter(False, "<unknown>"),
    tracemalloc.Filter(False, __file__)
}


def _filter_snapshot(snapshot: tracemalloc.Snapshot, exclude: ExcludeType = None):
    """
    Filters the given snapshot using the exclude value and the DEFAULT_FILTERS.
    :param snapshot: snapshot to be filtered
    :param exclude: element(s) to be excluded from the snapshot
    :return: the filtered snapshot
    """
    filters = deepcopy(DEFAULT_FILTERS)
    if isinstance(exclude, str):
        filters.add(tracemalloc.Filter(False, exclude))
    elif isinstance(exclude, abc.Iterable):
        filters.update(
            {tracemalloc.Filter(False, e) for e in exclude if isinstance(e, str)}
        )
    return snapshot.filter_traces(tuple(filters))


def _get_overload(snapshot: tracemalloc.Snapshot, threshold: float, key_type: str = "lineno"):
    """
    Returns a list of statistics that exceed the given threshold in KiB.
    :param snapshot: snapshot to analyze
    :param threshold: threshold not to exceed (in KiB)
    :param key_type: key used to order the snapshot's statistics

    :return: a list of statistics that exceed the given threshold
    """
    stats = snapshot.statistics(key_type)
    return [stat for stat in stats if stat.size / 1024 > threshold]


def memory_not_exceed(threshold: float, exclude: ExcludeType = None):
    """
    Tests that the memory taken up by the given function
    doesn't exceed the given threshold in KiB.
    :param threshold: threshold in KiB
    :param exclude: element(s) to be excluded from the snapshot
    :return: the memeory_not_exceed's decorator
    """

    def memory_not_exceed_decorator(func: Callable):
        """
        memory_not_exceed's decorator.
        :param func: function to call
        :return: the memory_not_exceed's wrapper
        """
        @wraps(func)
        def memory_not_exceed_wrapper(*args):
            """
            memory_not_exceed's wrapper.
            :param args: wrapper's arguments
            """
            tracemalloc.start()
            func(*args)
            snapshot = tracemalloc.take_snapshot()
            tracemalloc.stop()
            snapshot = _filter_snapshot(snapshot, exclude=exclude)
            assert not _get_overload(snapshot, threshold=threshold), "Threshold reached"

        return memory_not_exceed_wrapper

    return memory_not_exceed_decorator
