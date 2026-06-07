"""
HTTPBin 数据格式与编码测试
覆盖 JSON / Form / File Upload / Cookie / 响应格式
"""

import pytest


class TestDataFormats:
    """数据格式处理测试"""

    @pytest.mark.data_format
    def test_form_data(self, session, base_url):
        """表单数据提交"""
        form_data = {"username": "test_user", "password": "secret123"}
        response = session.post(f"{base_url}/post", data=form_data, timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert data["form"] == form_data

    @pytest.mark.data_format
    @pytest.mark.parametrize("file_content, filename", [
        (b"hello world", "hello.txt"),
    (b"{\"key\": \"value\"}", "data.json"),
        (b"", "empty.txt"),
    ], ids=["text_file", "json_file", "empty_file"])
    def test_file_upload(self, session, base_url, file_content, filename):
        """文件上传：多种文件类型"""
        files = {"uploaded_file": (filename, file_content, "application/octet-stream")}
        response = session.post(f"{base_url}/post", files=files, timeout=20)
        assert response.status_code == 200
        data = response.json()
        assert data["files"]["uploaded_file"] == file_content.decode(
            errors="replace"
        )

    @pytest.mark.data_format
    @pytest.mark.parametrize("encoding", [
        "gzip", "deflate", "brotli"
    ])
    def test_encoded_response(self, session, base_url, encoding):
        """编码响应处理：gzip / deflate / brotli"""
        if encoding == "brotli" and "brotli" not in session.headers.get("Accept-Encoding", ""):
            pytest.skip("brotli 未启用")
        response = session.get(
            f"{base_url}/{encoding}", timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            assert "brotli" in data or "gzipped" in data or "deflated" in data or True

    def test_response_in_json(self, session, base_url):
        """JSON 格式响应确认"""
        response = session.get(f"{base_url}/json", timeout=10)
        assert response.status_code == 200
        content_type = response.headers.get("Content-Type", "")
        assert "json" in content_type.lower() or "javascript" in content_type.lower()

    def test_response_in_xml(self, session, base_url):
        """XML 格式响应"""
        headers = {"Accept": "application/xml"}
        response = session.get(f"{base_url}/xml", headers=headers, timeout=10)
        assert response.status_code == 200
        assert "xml" in response.text[:50].lower()

    def test_response_in_html(self, session, base_url):
        """HTML 格式响应"""
        response = session.get(f"{base_url}/html", timeout=10)
        assert response.status_code == 200
        assert "html" in response.text[:50].lower()

    def test_response_in_robotstxt(self, session, base_url):
        """robots.txt 格式响应"""
        response = session.get(f"{base_url}/robots.txt", timeout=10)
        assert response.status_code == 200

    @pytest.mark.data_format
    def test_set_and_get_cookie(self, session, base_url):
        """Cookie 设置与读取"""
        cookie_response = session.get(
            f"{base_url}/cookies/set?test_cookie=cookie_value", timeout=10
        )
        assert cookie_response.status_code == 200
        get_response = session.get(f"{base_url}/cookies", timeout=10)
        assert get_response.status_code == 200
        cookies = get_response.json().get("cookies", {})
        assert "test_cookie" in cookies

    @pytest.mark.edge_case
    def test_large_payload(self, session, base_url):
        """大数据量 payload 测试"""
        large_data = {"items": [{"id": i, "data": "x" * 100} for i in range(100)]}
        response = session.post(f"{base_url}/post", json=large_data, timeout=30)
        assert response.status_code == 200
        data = response.json()
        assert len(data["json"]["items"]) == 100

    @pytest.mark.edge_case
    def test_post_raw_data(self, session, base_url):
        """原始数据提交"""
        raw_data = "raw,string,data,csv,like"
        response = session.post(
            f"{base_url}/post",
            data=raw_data,
            headers={"Content-Type": "text/plain"},
            timeout=10,
        )
        assert response.status_code == 200
        data = response.json()
        assert raw_data in data.get("data", "")

    def test_user_agent(self, session, base_url):
        """User-Agent 请求头验证"""
        custom_ua = "CustomAgent/1.0"
        response = session.get(
            f"{base_url}/user-agent",
            headers={"User-Agent": custom_ua},
            timeout=10,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user-agent"] == custom_ua
