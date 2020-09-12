import linecache
import tracemalloc
from functools import wraps
from typing import List


def display_top(snapshot, key_type='lineno', limit=10):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        print("#%s: %s:%s: %.1f KiB"
              % (index, frame.filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


def _get_overload(snapshot, key_type='lineno', threshold=10):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    stats = snapshot.statistics(key_type)
    overload_stats = [stat for stat in stats if stat.size >= threshold]
    return overload_stats

def _get_infos(stats: List[tracemalloc.Statistic]):
    pass


def test_memory(threshold=10):
    # TODO: move in class
    def test_memory_decorator(func):
        @wraps(func)
        def test_memory_wrapper(*args, **kwargs):
            tracemalloc.start()
            func(*args)
            snapshot = tracemalloc.take_snapshot()
            assert len(_get_overload(snapshot, threshold=threshold)) == 0, "Threshold reached"

        return test_memory_wrapper

    return test_memory_decorator


@test_memory(threshold=1000)
def loop():
    count = 0
    return [count * i for i in range(1000000000)]


if __name__ == '__main__':
    loop()
