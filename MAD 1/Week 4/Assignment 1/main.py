from matplotlib import pyplot as plt
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == "GET":
        pass
