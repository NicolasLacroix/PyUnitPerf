# PyUnitPerf

![Python package](https://github.com/NicolasLacroix/PyUnitPerf/workflows/Python%20package/badge.svg?branch=master)
![Python versions](https://img.shields.io/badge/python-3.5,%203.6%2C%203.7%2C%203.8-blue?logo=python)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)

A simple and lightweight API for unit testing a Python 🐍 project's performances :zap::wheelchair:.

From **Python 3.5 to 3.8**, easily improve your project's performances tests through the use of dedicated **decorators**.

### Table of contents

- [Memory testing](#Memory-testing)
  - [Memory overload assertions](#Memory-overload-assertions)
  - [Memory leaks assertions](#Memory-leaks-assertions)

### Memory testing

#### Memory overload assertions

The memory overload assertions are possible thanks to the `@memory_not_exceed` decorator.

A simple *TestCase* associated to this decorator does the job :

```python
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
```

#### Memory leaks assertions

The memory leaks assertions are possible thanks to the `@memory_not_leak` decorator.

Once again, a simple *TestCase* associated to this decorator does the job :

```python
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
        valid_list = []
        valid_list.append("won't leak")
```
