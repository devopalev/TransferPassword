from flask import Flask, request, render_template
import storage

storage_data = storage.Storage()
app = Flask(__name__)


@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')


@app.route("/generate_link", methods=['POST'])
def generate_link():
    text = request.form.get("secret_text")
    if text:
        public_key, private_key = storage_data.save(text, 86400)
        url = f"{request.url_root}show/{public_key}"
        return render_template('generate_link.html', link=url, private_key=private_key)


@app.route("/show/<public_key>", methods=['GET'])
def pre_show(public_key):
    if storage_data.check_public_key(public_key):
        return render_template('pre_show.html', public_key=public_key)
    else:
        return render_template('not_found.html')


@app.route("/show/<public_key>", methods=['POST'])
def show(public_key):
    try:
        data = storage_data.get(public_key, request.form.get("private_key"))
        if data:
            return render_template('show.html', data=data)
        else:
            return render_template('not_found.html')
    except KeyError:
        return render_template('not_found.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=46001, debug=True)
