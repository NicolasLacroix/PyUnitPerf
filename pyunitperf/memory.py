"""
This package is dedicated to all the memory aspects testing.
"""
import tracemalloc
from copy import deepcopy
from functools import wraps
from typing import Callable, Iterable, Optional, List
import collections.abc as abc

ExcludeType = Optional[Iterable[str]]

DEFAULT_FILTERS = {
    tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
    tracemalloc.Filter(False, "<unknown>"),
    tracemalloc.Filter(False, __file__)
}


def _filter_snapshot(snapshot: tracemalloc.Snapshot, exclude: ExcludeType = None) -> tracemalloc.Snapshot:
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


def _get_overload(snapshot: tracemalloc.Snapshot, threshold: float, key_type: str = "lineno") -> \
        List[tracemalloc.Statistic]:
    """
    Returns a list of statistics that exceed the given threshold in KiB.
    :param snapshot: snapshot to analyze
    :param threshold: threshold not to exceed (in KiB)
    :param key_type: key used to order the snapshot's statistics

    :return: a list of statistics that exceed the given threshold
    """
    stats = snapshot.statistics(key_type)
    return [stat for stat in stats if stat.size / 1024 > threshold]


def _get_failure_details(stats: List[tracemalloc.Statistic]) -> str:
    """
    Returns a string containing details about the given stats which led to a failure.
    :param stats: statistics to describe
    :return: a string containing details about the given stats
             which led to a failure
    """
    details = "\n"
    for stat in stats:
        formatted_traceback = "\n".join(stat.traceback.format())
        details += "{} failed with size : [{} KiB]\n".format(formatted_traceback, stat.size / 1024)
    return details


def memory_not_exceed(threshold: float, exclude: ExcludeType = None) -> Callable:
    """
    Tests that the memory taken up by the given function
    doesn't exceed the given threshold in KiB.
    :param threshold: threshold in KiB
    :param exclude: element(s) to be excluded from the snapshot
    :return: the memeory_not_exceed's decorator
    """

    def memory_not_exceed_decorator(func: Callable) -> Callable:
        """
        memory_not_exceed's decorator.
        :param func: function to call
        :return: the memory_not_exceed's wrapper
        """
        @wraps(func)
        def memory_not_exceed_wrapper(*args) -> None:
            """
            memory_not_exceed's wrapper.
            :param args: wrapper's arguments
            """
            tracemalloc.start()
            func(*args)
            snapshot = tracemalloc.take_snapshot()
            tracemalloc.stop()
            snapshot = _filter_snapshot(snapshot, exclude=exclude)
            overload = _get_overload(snapshot, threshold=threshold)
            assert not overload, _get_failure_details(overload)

        return memory_not_exceed_wrapper

    return memory_not_exceed_decorator
