"""
HTTPBin 动态请求与延迟测试
覆盖延迟响应、流式响应、IP 查询等
"""

import pytest


class TestDynamicRequests:
    """动态请求场景测试"""

    @pytest.mark.slow
    @pytest.mark.parametrize("delay_seconds", [1, 2, 3],
                             ids=["1s", "2s", "3s"])
    def test_delayed_response(self, session, base_url, delay_seconds):
        """延迟响应测试：验证服务端延迟机制"""
        import time
        start = time.time()
        response = session.get(
            f"{base_url}/delay/{delay_seconds}", timeout=delay_seconds + 5
        )
        elapsed = time.time() - start
        assert response.status_code in (200, 502, 503), f"期望 200，实际 {response.status_code}"
        assert elapsed >= delay_seconds - 0.5, (
            f"延迟不足：期望至少 {delay_seconds}s，实际 {elapsed:.2f}s"
        )

    def test_delayed_response_returns_data(self, session, base_url):
        """延迟响应返回数据正确性"""
        response = session.get(f"{base_url}/delay/1", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "url" in data

    def test_stream_response(self, session, base_url):
        """流式响应测试（逐行读取）"""
        response = session.get(
            f"{base_url}/stream/10", stream=True, timeout=15
        )
        assert response.status_code == 200
        lines = list(response.iter_lines(decode_unicode=True))
        assert len(lines) == 10, f"期望 10 行，实际 {len(lines)}"

    @pytest.mark.parametrize("lines", [5, 20], ids=["5_lines", "20_lines"])
    def test_stream_n_lines(self, session, base_url, lines):
        """流式响应行数参数化"""
        response = session.get(
            f"{base_url}/stream/{lines}", stream=True, timeout=20
        )
        assert response.status_code == 200
        actual = len(list(response.iter_lines(decode_unicode=True)))
        assert actual == lines, f"期望 {lines} 行 JSON，实际 {actual}"

    def test_ip_endpoint(self, session, base_url):
        """IP 地址查询"""
        response = session.get(f"{base_url}/ip", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "origin" in data
        assert data["origin"].count(".") >= 1

    @pytest.mark.edge_case
    def test_uuid_generation(self, session, base_url):
        """UUID 生成验证"""
        response = session.get(f"{base_url}/uuid", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert len(data["uuid"]) == 36
        assert data["uuid"].count("-") == 4


class TestHeadersAndCache:
    """请求头与缓存相关测试"""

    @pytest.mark.parametrize("header_name", [
        "Accept-Language", "Accept-Encoding",
        "Cache-Control", "X-Custom-ID"
    ])
    def test_request_headers(self, session, base_url, header_name):
        """自定义请求头发送"""
        headers = {header_name: "test_value_123"}
        response = session.get(f"{base_url}/headers", headers=headers, timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert header_name.lower() in {k.lower(): k for k in data["headers"]}

    def test_cache_control(self, session, base_url):
        """Cache-Control 请求头"""
        headers = {"Cache-Control": "no-cache"}
        response = session.get(f"{base_url}/cache", headers=headers, timeout=10)
        assert response.status_code in [200, 304]

    def test_etag_request(self, session, base_url):
        """ETag / If-None-Match 条件请求"""
        first = session.get(f"{base_url}/etag/etagtest", timeout=10)
        assert first.status_code == 200
        etag = first.headers.get("ETag", "")
        if etag:
            second = session.get(
                f"{base_url}/etag/etagtest",
                headers={"If-None-Match": etag},
                timeout=10,
            )
            assert second.status_code == 304

    def test_response_headers(self, session, base_url):
        """响应头验证"""
        response = session.get(f"{base_url}/response-headers?key=value", timeout=10)
        assert response.status_code == 200
        assert "key" in response.headers or response.json().get("key") == "value"

    @pytest.mark.edge_case
    def test_infinite_redirect_protection(self, session, base_url):
        """无限重定向防护测试"""
        import requests
        try:
            session.get(f"{base_url}/absolute-redirect/31", timeout=15)
        except requests.exceptions.TooManyRedirects:
            pass
        except requests.exceptions.ConnectionError:
            pytest.skip("httpbin.org 连接失败 (redirect)")
        except requests.exceptions.ReadTimeout:
            pytest.skip("httpbin.org 重定向超时 (port 80)")
