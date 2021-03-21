from ramona.library import Library
import pytest

def test_library():
    lib = Library()
    assert(lib is not None)
    with pytest.raises(FileNotFoundError):
        lib.pushdir("foo")
    lib.pushdir("../data")
    print(lib.list())