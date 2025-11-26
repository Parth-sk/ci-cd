from app import add_task, remove_task

def test_add():
    assert add_task([], "task1") == ["task1"]

def test_remove():
    assert remove_task(["task1"], "task1") == []
    