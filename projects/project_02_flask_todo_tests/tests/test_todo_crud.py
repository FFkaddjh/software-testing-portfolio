"""TODO 更新、删除、状态切换测试"""

import pytest


class TestUpdateTodo:
    """更新 TODO — PUT /api/todos/<id>"""

    def test_update_title(self, client, sample_todos):
        """更新 TODO 标题"""
        todo_id = sample_todos[0]["id"]
        resp = client.put(f"/api/todos/{todo_id}", json={"title": "新标题"})
        assert resp.status_code == 200
        assert resp.get_json()["title"] == "新标题"

    def test_update_status(self, client, sample_todos):
        """更新 TODO 状态为 completed"""
        todo_id = sample_todos[0]["id"]
        resp = client.put(f"/api/todos/{todo_id}", json={"status": "completed"})
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "completed"

    def test_update_title_and_status(self, client, sample_todos):
        """同时更新标题和状态"""
        todo_id = sample_todos[0]["id"]
        resp = client.put(f"/api/todos/{todo_id}", json={"title": "已完成", "status": "completed"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["title"] == "已完成"
        assert data["status"] == "completed"

    @pytest.mark.edge_case
    def test_update_empty_title(self, client, sample_todos):
        """更新时标题为空：应返回 400"""
        todo_id = sample_todos[0]["id"]
        resp = client.put(f"/api/todos/{todo_id}", json={"title": ""})
        assert resp.status_code == 400

    @pytest.mark.edge_case
    def test_update_invalid_status(self, client, sample_todos):
        """设置无效状态：应返回 400"""
        todo_id = sample_todos[0]["id"]
        resp = client.put(f"/api/todos/{todo_id}", json={"status": "deleted"})
        assert resp.status_code == 400

    @pytest.mark.edge_case
    def test_update_nonexistent_todo(self, client):
        """更新不存在的 TODO：应返回 404"""
        resp = client.put("/api/todos/99999", json={"title": "新标题"})
        assert resp.status_code == 404


class TestDeleteTodo:
    """删除 TODO — DELETE /api/todos/<id>"""

    def test_delete_todo(self, client, sample_todos):
        """正常删除 TODO"""
        todo_id = sample_todos[0]["id"]
        resp = client.delete(f"/api/todos/{todo_id}")
        assert resp.status_code == 200
        # 确认已删除
        resp = client.get(f"/api/todos/{todo_id}")
        assert resp.status_code == 404

    def test_delete_reduces_count(self, client, sample_todos):
        """删除后列表长度减少"""
        todo_id = sample_todos[0]["id"]
        before = len(client.get("/api/todos").get_json())
        client.delete(f"/api/todos/{todo_id}")
        after = len(client.get("/api/todos").get_json())
        assert after == before - 1

    @pytest.mark.edge_case
    def test_delete_nonexistent(self, client):
        """删除不存在的 TODO：应返回 404"""
        resp = client.delete("/api/todos/99999")
        assert resp.status_code == 404


class TestToggleTodo:
    """切换状态 — PATCH /api/todos/<id>/toggle"""

    def test_toggle_pending_to_completed(self, client, sample_todos):
        """从 pending 切换到 completed"""
        todo_id = sample_todos[0]["id"]
        resp = client.patch(f"/api/todos/{todo_id}/toggle")
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "completed"

    def test_toggle_completed_to_pending(self, client, sample_todos):
        """从 completed 切换到 pending"""
        todo_id = sample_todos[0]["id"]
        client.patch(f"/api/todos/{todo_id}/toggle")  # pending -> completed
        resp = client.patch(f"/api/todos/{todo_id}/toggle")  # completed -> pending
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "pending"

    @pytest.mark.edge_case
    def test_toggle_nonexistent(self, client):
        """切换不存在的 TODO：应返回 404"""
        resp = client.patch("/api/todos/99999/toggle")
        assert resp.status_code == 404


class TestClearCompleted:
    """清除已完成的 TODO — POST /api/todos/clear"""

    def test_clear_completed(self, client, sample_todos):
        """清除所有已完成项目"""
        # 先完成两个
        client.patch(f"/api/todos/{sample_todos[0]['id']}/toggle")
        client.patch(f"/api/todos/{sample_todos[1]['id']}/toggle")
        resp = client.post("/api/todos/clear")
        assert resp.status_code == 200
        remaining = client.get("/api/todos").get_json()
        assert len(remaining) == 1  # 只剩一个未完成的

    def test_clear_no_completed(self, client, sample_todos):
        """没有已完成项目时清除"""
        resp = client.post("/api/todos/clear")
        assert resp.status_code == 200
        assert "0" in resp.get_json()["message"]
