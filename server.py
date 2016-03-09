from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/rude")
def rude_page():
    return "You're ugly and so is your mom"

if __name__ == "__main__":
    app.run()