import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))


@pytest.fixture
def app():
    """创建测试用的 Flask 应用实例"""
    from app import app as flask_app, reset
    reset()
    flask_app.config.update({
        "TESTING": True,
    })
    return flask_app


@pytest.fixture
def client(app):
    """Flask 测试客户端"""
    return app.test_client()


@pytest.fixture
def sample_todos(client):
    """预置测试数据：创建几个 TODO 项"""
    todos_data = [
        {"title": "完成测试用例编写"},
        {"title": "完善简历投递"},
        {"title": "复习面试题"},
    ]
    created = []
    for data in todos_data:
        resp = client.post("/api/todos", json=data)
        created.append(resp.get_json())
    return created
