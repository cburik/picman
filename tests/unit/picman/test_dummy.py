import picman


def test_dummy():
    version = picman.__version__
    assert isinstance(version, str)
