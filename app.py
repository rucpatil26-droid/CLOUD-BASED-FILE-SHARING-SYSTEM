from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import mysql.connector

app = Flask(__name__)
UPLOAD_FOLDER = 'backend/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Rushi2626",
    database="cloud_file_sharing"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("SELECT * FROM files")
    files = cursor.fetchall()
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        cursor.execute("INSERT INTO files (filename) VALUES (%s)", (file.filename,))
        db.commit()
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<int:file_id>')
def delete_file(file_id):
    cursor.execute("SELECT filename FROM files WHERE id=%s", (file_id,))
    file = cursor.fetchone()
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file['filename'])
        if os.path.exists(file_path):
            os.remove(file_path)
        cursor.execute("DELETE FROM files WHERE id=%s", (file_id,))
        db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)