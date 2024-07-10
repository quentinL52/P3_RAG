from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = file.filename
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        # Vous pouvez maintenant utiliser pdf_loader.py pour traiter le fichier PDF
        return 'File uploaded successfully'
    return 'File upload failed'

if __name__ == '__main__':
    app.run(debug=True)
