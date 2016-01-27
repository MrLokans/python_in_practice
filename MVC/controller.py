from flask import Flask, redirect, render_template, request
from werkzeug.exceptions import BadRequest, NotFound

from models import Url

app = Flask(__name__, template_folder='views')


@app.route("/")
def index():
    """main page presentation"""
    return render_template('main_page.html')


@app.route("/shorten/")
def shorten():
    long_url = request.args.get('url')
    if not long_url:
        raise BadRequest()

    url_model = Url.shorten(long_url)

    short_url = "/".join([request.host, url_model.short_url])
    return render_template('success.html', short_url=short_url)


@app.route('/<path:path>')
def redirect_to_long(path=''):
    url_model = Url.get_by_short_url(path)

    if not url_model:
        raise NotFound()

    return redirect(url_model.long_url)


if __name__ == '__main__':
    app.run(debug=True)
