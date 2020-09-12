import tracemalloc
from functools import wraps
from typing import List

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
