from flask import Flask, render_template, request
from edi_viewer import parse_edi_837

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view', methods=['POST'])
def view():
    edi_text = request.form.get('edi_transaction')
    parsed = parse_edi_837(edi_text)
    return render_template('index.html', edi_data=parsed)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
