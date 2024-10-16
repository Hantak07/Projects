from flask import Flask
from matplotlib import pyplot as plt
app = Flask(__name__, template_folder='templates')

@app.route("/index", methods=['POST'])
def index():
    page = ""
    pass


if __name__ == '__main__':
    app.run(debug=True)