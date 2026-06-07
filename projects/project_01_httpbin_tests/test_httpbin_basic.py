"""
HTTPBin 基础 HTTP 方法测试套件
覆盖 GET / POST / PUT / PATCH / DELETE 五种核心方法
"""

import pytest


class TestHTTPMethods:
    """测试 HTTP 基本方法的正确性"""

    @pytest.mark.smoke
    @pytest.mark.parametrize("endpoint", [
        "/get", "/post", "/put", "/patch", "/delete"
    ], ids=["GET", "POST", "PUT", "PATCH", "DELETE"])
    def test_basic_methods(self, session, base_url, endpoint):
        """冒烟测试：五种核心 HTTP 方法是否正常响应"""
        method = endpoint.lstrip("/")
        response = getattr(session, method)(f"{base_url}{endpoint}", timeout=10)
        assert response.status_code == 200, f"{method.upper()} 请求失败: {response.status_code}"
        data = response.json()
        assert "url" in data, f"{method.upper()} 响应缺少 url 字段"

    @pytest.mark.smoke
    def test_get_with_query_params(self, session, base_url):
        """GET 请求 + 查询参数"""
        params = {"search": "test", "page": "1", "limit": "10"}
        response = session.get(f"{base_url}/get", params=params, timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert data["args"] == params, f"查询参数不匹配: {data['args']} != {params}"

    @pytest.mark.smoke
    def test_get_with_headers(self, session, base_url):
        """GET 请求 + 自定义请求头"""
        custom_headers = {"X-Test-Header": "test-value", "X-Custom": "hello"}
        response = session.get(f"{base_url}/headers", headers=custom_headers, timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert data["headers"]["X-Test-Header"] == "test-value"

    @pytest.mark.parametrize("payload", [
        {"key": "value"},
        {"numbers": [1, 2, 3], "nested": {"a": 1}},
        {"empty": None, "boolean": True},
    ], ids=["simple", "complex", "special"])
    def test_post_json(self, session, base_url, payload):
        """POST JSON 数据：多种 payload 结构"""
        response = session.post(f"{base_url}/post", json=payload, timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert data["json"] == payload, f"返回的 JSON 不匹配: {data['json']}"

    def test_put_update(self, session, base_url):
        """PUT 请求：更新资源"""
        payload = {"id": 1, "title": "updated", "status": "done"}
        response = session.put(f"{base_url}/put", json=payload, timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert data["json"] == payload

    def test_patch_partial(self, session, base_url):
        """PATCH 请求：部分更新"""
        payload = {"status": "in_progress"}
        response = session.patch(f"{base_url}/patch", json=payload, timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert data["json"] == payload

    def test_delete_request(self, session, base_url):
        """DELETE 请求"""
        response = session.delete(f"{base_url}/delete", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "url" in data

    @pytest.mark.edge_case
    def test_get_without_params(self, session, base_url):
        """边缘：GET 请求不传任何参数"""
        response = session.get(f"{base_url}/get", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert data["args"] == {}, "不传参数时 args 应为空字典"

    @pytest.mark.edge_case
    def test_post_without_body(self, session, base_url):
        """边缘：POST 请求不传 body"""
        response = session.post(f"{base_url}/post", timeout=10)
        assert response.status_code == 200
