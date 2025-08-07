from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Flask on Render!"

@app.route("/data")
def data():
    return jsonify(message="Here is some backend data")

# Required to run on Render
if __name__ == "__main__":
    app.run()
