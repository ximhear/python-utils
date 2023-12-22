from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# 파일 업로드를 위한 설정
UPLOAD_FOLDER = '/Users/gzonelee/PycharmProjects/pythonProject1/uploads'  # 파일을 저장할 경로
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'heic'}  # 허용할 파일 확장자
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api', methods=['GET', 'POST'])
def api_endpoint():
    if request.method == 'POST':
        data = request.json
        return jsonify({"message": "POST request received", "data": data})
    else:
        return jsonify({"message": "GET request received"})


@app.route('/api/send/<guestNo>/image/<imageNo>', methods=['GET', 'POST'])
def handle_request(guestNo, imageNo):
    # guestNo와 imageNo를 사용하여 필요한 작업 수행
    # 예를 들어, 데이터베이스 조회, 로직 처리 등

    # 응답 반환
    return jsonify({"guestNo": guestNo, "imageNo": imageNo})


@app.route('/upload', methods=['POST'])
def upload_file():
    # 텍스트 필드 데이터 접근
    file_name = request.form.get('file-url')  # 파일 이름 필드
    creation_date = request.form.get('date')  # 생성일 필드

    # 로그 기록
    app.logger.info(f'Received file_name: {file_name}, creation_date: {creation_date}')

    # 파일 데이터 접근
    if 'file' not in request.files:
        return jsonify({"message": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({
            "message": "File uploaded successfully",
            "file_name": file_name,
            "creation_date": creation_date,
            "saved_file": filename
        })


@app.route('/download/<fileNo>')
def download_file(fileNo):
    if fileNo == '1':
        file_path = '/Users/gzonelee/PycharmProjects/pythonProject1/uploads/About_Threads_and_Threadgroups_Apple_Developer_Documentation.pdf'
    elif fileNo == '2':
        file_path = '/Users/gzonelee/PycharmProjects/pythonProject1/uploads/colored_image_10.png'
    else:
        file_path = '/Users/gzonelee/PycharmProjects/pythonProject1/uploads/image.jpg'
    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
