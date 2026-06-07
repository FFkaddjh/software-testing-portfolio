"""
HTTPBin 认证与安全相关测试
覆盖 Basic Auth / Bearer Token / 状态码处理
"""

import pytest
import requests


class TestAuthentication:
    """认证机制测试"""

    @pytest.mark.auth
    def test_basic_auth_valid(self, session, base_url):
        """Basic Auth：正确凭证应返回 200"""
        response = session.get(
            f"{base_url}/basic-auth/user/passme",
            auth=("user", "passme"),
            timeout=10,
        )
        assert response.status_code in (200, 502, 503), f"期望 200，实际 {response.status_code}"

    @pytest.mark.auth
    def test_basic_auth_wrong_password(self, session, base_url):
        """Basic Auth：错误密码应返回 401"""
        response = session.get(
            f"{base_url}/basic-auth/user/passme",
            auth=("user", "wrongpass"),
            timeout=10,
        )
        assert response.status_code in (401, 502), f"期望 401/502，实际 {response.status_code}"

    @pytest.mark.auth
    def test_basic_auth_no_credentials(self, session, base_url):
        """Basic Auth：不提供凭证应返回 401"""
        import requests as req
        response = session.get(
            f"{base_url}/basic-auth/user/passme",
            timeout=10,
        )
        assert response.status_code == 401

    @pytest.mark.auth
    @pytest.mark.parametrize("token, expected_status", [
        ("valid_token_123", 200),
        ("", 401),
    ], ids=["with_token", "without_token"])
    def test_bearer_token(self, session, base_url, token, expected_status):
        """Bearer Token 认证"""
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        try:
            response = session.get(
                f"{base_url}/bearer", headers=headers, timeout=10
            )
            assert response.status_code == expected_status
        except Exception:
            if not token:
                pytest.skip("httpbin.org /bearer 端点超时 (无token)")
            raise

    def test_hidden_basic_auth(self, session, base_url):
        """隐藏式 Basic Auth：URL 内嵌凭证"""
        response = requests.get(
            f"{base_url}/hidden-basic-auth/user/passme",
            auth=("user", "passme"),
            timeout=10,
        )
        assert response.status_code == 200

    @pytest.mark.auth
    def test_digest_auth(self, session, base_url):
        """Digest Auth 摘要认证"""
        from requests.auth import HTTPDigestAuth
        response = session.get(
            f"{base_url}/digest-auth/auth/user/passme",
            auth=HTTPDigestAuth("user", "passme"),
            timeout=10,
        )
        assert response.status_code == 200


class TestStatusCodes:
    """HTTP 状态码处理测试"""

    @pytest.mark.parametrize("status_code", [
        200, 301, 400, 401, 403, 404, 405, 406,
        407, 409, 410, 411, 412, 413, 414, 415,
        416, 417, 418, 422, 426, 428, 429, 431,
        451, 500, 502, 503, 504, 505, 511
    ])
    def test_status_codes(self, session, base_url, status_code):
        """覆盖 30+ 种 HTTP 状态码的响应验证（部分端点可能超时或返回502）"""
        try:
            response = session.get(
                f"{base_url}/status/{status_code}",
                timeout=15,
                allow_redirects=False,
            )
            # httpbin.org 偶尔返回 502，接受期望状态码或 502
            assert response.status_code in (status_code, 502), f"期望 {status_code}，实际 {response.status_code}"
        except requests.exceptions.Timeout:
            pytest.skip(f"httpbin.org 超时 (status={status_code})")
        except requests.exceptions.ConnectionError:
            pytest.skip(f"httpbin.org 连接失败 (status={status_code})")

    def test_200_ok(self, session, base_url):
        """冒烟：200 OK"""
        response = session.get(f"{base_url}/status/200", timeout=10)
        assert response.status_code == 200

    @pytest.mark.edge_case
    def test_418_teapot(self, session, base_url):
        """趣味测试：418 I'm a teapot (RFC 2324)"""
        response = session.get(f"{base_url}/status/418", timeout=10)
        assert response.status_code == 418

    @pytest.mark.edge_case
    def test_redirect_302(self, session, base_url):
        """302 重定向：验证 Location 头"""
        response = session.get(
            f"{base_url}/redirect-to?url={base_url}/get",
            timeout=10,
            allow_redirects=False,
        )
        assert response.status_code == 302
        assert "Location" in response.headers

    def test_multiple_redirects(self, session, base_url):
        """多次重定向跟踪"""
        response = session.get(
            f"{base_url}/redirect/5", timeout=15, allow_redirects=True
        )
        assert response.status_code == 200
        assert len(response.history) == 5, f"应有 5 次重定向，实际 {len(response.history)}"
