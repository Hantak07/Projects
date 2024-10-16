from matplotlib import pyplot as plt
from flask import Flask, request, render_template, render_template_string

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=["POST"])
def output():
    data = None
    id_value = None
    if request.method == "POST":
        data = request.form.get("ID")
        id_value = request.form.get("id_value")
    if id_value is None or data is None:
        return render_template("error.html")
    else:
        
        return render_template_string(f"{data}, {id_value}")

@app.route("/index")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)