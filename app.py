from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Fixed keys, initially unbound (None)
keys = {
    "7GmR9bVz2XpQkL8J": None,
    "w3DzP5nKvRxF1YmT": None,
    "Hs7LfC9mW8QpjVz": None,
    "tNr5XqMzYY6VwsR": None,
    "BpWfE7UzVsVxMkL9": None,
    "gQJ3ZpRxYN6tHaBD": None,
    "d2CXLTfHmVzq8PgN": None,
    "Snx76LVkMwJFpbRY": None,
    "yQc94RpXVsBMLoT1": None,
    "Ah2WM7NkqVzJPfES": None,
    "TzFK83YwqLoXpCnR": None,
    "mNPJ94qKsVbwZEtX": None,
    "Xqf3LsWMbRg5CZTh": None,
    "HtwvDLMkQBJXsNzR": None,
    "RK6gLqSbyXp9VFDZ": None,
    "F7nVdZBRpqXLjYYs": None,
    "gXQs6FwPhYNLKzb4": None,
    "3pZCQ9XvVkmBtYsY": None,
    "8Fx5VdNJpycLKRsQ": None,
    "WqanRbGx9MYHZFsL": None
}

@app.route("/")
def home():
    return "Key auth backend running."

@app.route("/auth", methods=["POST"])
def auth():
    data = request.get_json()
    if not data or "key" not in data:
        return jsonify({"success": False, "message": "Key required"}), 400

    user_key = data["key"]
    user_ip = request.remote_addr

    # Reject if key not valid
    if user_key not in keys:
        return jsonify({"success": False, "message": "Invalid key"}), 401

    # Check if this IP already has a key bound
    ip_bound_keys = [k for k, ip in keys.items() if ip == user_ip]

    # If IP already has a different key bound, reject
    if ip_bound_keys and user_key not in ip_bound_keys:
        return jsonify({"success": False, "message": "You already have a different key bound to your IP"}), 403

    bound_ip = keys[user_key]

    if bound_ip is None:
        # Key is free, bind to this IP
        keys[user_key] = user_ip
        return jsonify({"success": True, "message": "Key accepted and bound to your IP"})

    if bound_ip == user_ip:
        # Same IP, accept
        return jsonify({"success": True, "message": "Key accepted"})

    # Key bound to different IP
    return jsonify({"success": False, "message": "Key is bound to another IP"}), 403

@app.route("/flush", methods=["POST"])
def flush():
    # This resets all keys to unbound (use only when needed)
    for k in keys:
        keys[k] = None
    return jsonify({"success": True, "message": "All keys flushed (unbound)."})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
