"""
Flask TODO 应用 — 测试目标
一个简单的待办事项管理 Web 应用
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

# 用列表模拟数据库
todos = []
next_id = 1


@app.route("/")
def index():
    """首页：显示所有 TODO"""
    return render_template("index.html", todos=todos)


@app.route("/api/todos", methods=["GET"])
def get_todos():
    """获取所有 TODO（支持 status 过滤）"""
    status = request.args.get("status")
    if status:
        filtered = [t for t in todos if t["status"] == status]
        return jsonify(filtered)
    return jsonify(todos)


@app.route("/api/todos", methods=["POST"])
def create_todo():
    """创建新的 TODO"""
    global next_id
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "标题不能为空"}), 400
    if len(title) > 200:
        return jsonify({"error": "标题不能超过 200 个字符"}), 400

    todo = {
        "id": next_id,
        "title": title,
        "status": "pending",  # pending | completed
    }
    todos.append(todo)
    next_id += 1
    return jsonify(todo), 201


@app.route("/api/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    """获取单个 TODO"""
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if not todo:
        return jsonify({"error": "TODO 不存在"}), 404
    return jsonify(todo)


@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """更新 TODO（标题和/或状态）"""
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if not todo:
        return jsonify({"error": "TODO 不存在"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    if "title" in data:
        title = data["title"].strip()
        if not title:
            return jsonify({"error": "标题不能为空"}), 400
        if len(title) > 200:
            return jsonify({"error": "标题不能超过 200 个字符"}), 400
        todo["title"] = title

    if "status" in data:
        if data["status"] not in ("pending", "completed"):
            return jsonify({"error": "状态只能为 pending 或 completed"}), 400
        todo["status"] = data["status"]

    return jsonify(todo)


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """删除 TODO"""
    global todos
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if not todo:
        return jsonify({"error": "TODO 不存在"}), 404
    todos = [t for t in todos if t["id"] != todo_id]
    return jsonify({"message": "删除成功"}), 200


@app.route("/api/todos/<int:todo_id>/toggle", methods=["PATCH"])
def toggle_todo(todo_id):
    """切换 TODO 完成状态"""
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if not todo:
        return jsonify({"error": "TODO 不存在"}), 404
    todo["status"] = "completed" if todo["status"] == "pending" else "pending"
    return jsonify(todo)


@app.route("/api/todos/clear", methods=["POST"])
def clear_completed():
    """清除所有已完成的 TODO"""
    global todos
    completed = [t for t in todos if t["status"] == "completed"]
    todos = [t for t in todos if t["status"] != "completed"]
    return jsonify({"message": f"已清除 {len(completed)} 个已完成项"}), 200


def reset():
    """重置状态（用于测试）"""
    global todos, next_id
    todos.clear()
    next_id = 1


if __name__ == "__main__":
    app.run(debug=True, port=5000)
