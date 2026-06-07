"""TODO API 基础功能测试"""

import pytest


class TestCreateTodo:
    """创建 TODO — POST /api/todos"""

    @pytest.mark.smoke
    def test_create_todo_success(self, client):
        """正常创建 TODO"""
        resp = client.post("/api/todos", json={"title": "学习 pytest"})
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["title"] == "学习 pytest"
        assert data["status"] == "pending"
        assert "id" in data

    @pytest.mark.edge_case
    def test_create_todo_empty_title(self, client):
        """标题为空：应返回 400"""
        resp = client.post("/api/todos", json={"title": ""})
        assert resp.status_code == 400
        assert "标题" in resp.get_json()["error"]

    @pytest.mark.edge_case
    def test_create_todo_only_spaces(self, client):
        """标题只有空格：应返回 400"""
        resp = client.post("/api/todos", json={"title": "   "})
        assert resp.status_code == 400

    @pytest.mark.edge_case
    def test_create_todo_no_body(self, client):
        """没有请求体：应返回 400"""
        resp = client.post("/api/todos", data="")
        assert resp.status_code == 400

    @pytest.mark.edge_case
    def test_create_todo_no_title_field(self, client):
        """缺少 title 字段：应返回 400"""
        resp = client.post("/api/todos", json={"status": "completed"})
        assert resp.status_code == 400

    @pytest.mark.edge_case
    def test_create_todo_long_title(self, client):
        """超长标题：应返回 400"""
        resp = client.post("/api/todos", json={"title": "x" * 201})
        assert resp.status_code == 400

    def test_create_todo_max_length_title(self, client):
        """恰好 200 字符的标题：应成功"""
        resp = client.post("/api/todos", json={"title": "x" * 200})
        assert resp.status_code == 201


class TestGetTodos:
    """获取 TODO — GET /api/todos"""

    @pytest.mark.smoke
    def test_get_all_todos(self, client, sample_todos):
        """获取所有 TODO 列表"""
        resp = client.get("/api/todos")
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data) == 3
        assert data[0]["title"] == "完成测试用例编写"

    def test_get_empty_todos(self, client):
        """列表为空时返回空数组"""
        resp = client.get("/api/todos")
        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_get_todo_by_id(self, client, sample_todos):
        """按 ID 获取单个 TODO"""
        todo_id = sample_todos[0]["id"]
        resp = client.get(f"/api/todos/{todo_id}")
        assert resp.status_code == 200
        assert resp.get_json()["id"] == todo_id

    @pytest.mark.edge_case
    def test_get_nonexistent_todo(self, client):
        """获取不存在的 TODO：应返回 404"""
        resp = client.get("/api/todos/99999")
        assert resp.status_code == 404
