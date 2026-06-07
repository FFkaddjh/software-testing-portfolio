import requests
import pytest


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://httpbin.org"


@pytest.fixture(scope="session")
def session(base_url: str) -> requests.Session:
    sess = requests.Session()
    sess.headers.update({
        "User-Agent": "pytest-httpbin-tests/1.0",
        "Accept": "application/json",
    })
    # 跳过系统代理，避免代理超时影响测试
    sess.trust_env = False
    yield sess
    sess.close()


@pytest.fixture
def test_data() -> dict:
    return {"name": "test_user", "age": 25, "active": True}