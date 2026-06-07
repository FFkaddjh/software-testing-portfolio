"""TODO 边界场景与健壮性测试"""

import pytest


class TestEdgeCases:
    """边界场景测试"""

    def test_create_and_verify_response_structure(self, client):
        """验证创建响应包含所有必要字段"""
        resp = client.post("/api/todos", json={"title": "测试"})
        data = resp.get_json()
        expected_fields = {"id", "title", "status"}
        assert expected_fields.issubset(data.keys()), f"缺少字段: {expected_fields - data.keys()}"

    def test_id_auto_increment(self, client):
        """验证 ID 自增"""
        t1 = client.post("/api/todos", json={"title": "a"}).get_json()
        t2 = client.post("/api/todos", json={"title": "b"}).get_json()
        assert t2["id"] == t1["id"] + 1

    def test_serial_numbers_after_delete(self, client, sample_todos):
        """删除后 ID 不重复"""
        ids_before = {t["id"] for t in client.get("/api/todos").get_json()}
        client.delete(f"/api/todos/{sample_todos[0]['id']}")
        t3 = client.post("/api/todos", json={"title": "新项"}).get_json()
        assert t3["id"] not in ids_before

    @pytest.mark.parametrize("title", [
        "a",
        "你好世界",
        "test with spaces",
        "1234567890",
        "!@#$%^",
        "a" * 200,
    ], ids=["single_char", "chinese", "with_spaces", "numbers", "symbols", "max_length"])
    def test_various_title_types(self, client, title):
        """多种标题格式的创建"""
        resp = client.post("/api/todos", json={"title": title})
        assert resp.status_code == 201
        assert resp.get_json()["title"] == title

    def test_consecutive_operations(self, client):
        """连续操作：创建 → 更新 → 切换 → 删除"""
        # 创建
        resp = client.post("/api/todos", json={"title": "连续操作测试"})
        assert resp.status_code == 201
        todo_id = resp.get_json()["id"]

        # 更新
        resp = client.put(f"/api/todos/{todo_id}", json={"title": "已更新"})
        assert resp.get_json()["title"] == "已更新"

        # 切换
        resp = client.patch(f"/api/todos/{todo_id}/toggle")
        assert resp.get_json()["status"] == "completed"

        # 再切换回来
        resp = client.patch(f"/api/todos/{todo_id}/toggle")
        assert resp.get_json()["status"] == "pending"

        # 删除
        resp = client.delete(f"/api/todos/{todo_id}")
        assert resp.status_code == 200

        # 确认删除
        resp = client.get(f"/api/todos/{todo_id}")
        assert resp.status_code == 404

    def test_filter_by_status(self, client, sample_todos):
        """按状态过滤 TODO"""
        # 把第一个完成
        client.patch(f"/api/todos/{sample_todos[0]['id']}/toggle")

        pending = client.get("/api/todos?status=pending").get_json()
        completed = client.get("/api/todos?status=completed").get_json()

        assert len(pending) == 2, f"期望 2 个 pending，实际 {len(pending)}"
        assert len(completed) == 1, f"期望 1 个 completed，实际 {len(completed)}"

    def test_filter_invalid_status(self, client, sample_todos):
        """无效状态过滤：返回空列表"""
        resp = client.get("/api/todos?status=invalid")
        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_create_special_characters(self, client):
        """特殊字符标题"""
        special_titles = [
            "<script>alert('xss')</script>",
            "line1\nline2",
            " 前后有空格  ",
        ]
        for title in special_titles:
            resp = client.post("/api/todos", json={"title": title})
            assert resp.status_code == 201
            # 验证数据没有被截断或编码
            saved = resp.get_json()["title"]
            assert saved == title.strip() or saved == title
