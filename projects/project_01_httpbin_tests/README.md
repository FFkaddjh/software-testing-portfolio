# HTTPBin API 接口测试

## 这个项目是干嘛的

用 pytest + requests 对 httpbin.org 做接口测试，一共86条用例，81条通过。

httpbin.org 是一个专门让人练手接口测试的网站，提供各种 HTTP 端点用来测试。我拿它来练习 pytest 写接口测试的各种写法。

## 测试了哪些内容

- GET/POST/PUT/PATCH/DELETE 五种方法
- Basic Auth / Bearer Token / Digest Auth 认证
- 30+ 种 HTTP 状态码
- JSON、表单、文件上传、Cookie
- 延迟响应、流式响应、重定向

## 怎么跑

```bash
cd project_01_httpbin_tests
pip install -r requirements.txt
python -m pytest -v -m "not slow"
```

不想跑慢的延迟测试可以加 `-m "not slow"`。

## 结果

81 pass, 4 skip, 1 fail（skip和fail都是 httpbin 服务端的问题，不是代码bug）

## 学到的东西

- pytest 的参数化机制非常适合接口测试
- HTTP 查询参数在传输中都是字符串，断言时要注意类型
- 测外部API要考虑服务端不稳定的情况
