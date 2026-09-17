# test_first.py

def test_add():
    assert 1 + 1 == 2

def test_string():
    assert "hello".upper() == "HELLO"

def test_will_fail():
    assert 1 + 1 == 3  # 故意失败，看报错长什么样