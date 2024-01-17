from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
import random
from datetime import datetime

app = Flask(__name__)

# 파일 업로드를 위한 설정
UPLOAD_FOLDER = '/Users/gzonelee/git/python-utils/uploads'  # 파일을 저장할 경로
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


@app.route('/eofp/v1/ofp/<legIdentifier>/message', methods=['GET'])
def get_messages(legIdentifier):
    category = request.args.get('category', default=None, type=str)
    app.logger.info(f'Received category: {category}')
    data = ""
    if category == "REQUEST STAFF":
        data = load_json_data('RequestStaff.json')
    elif category == "Load Sheet INQUIRY":
        data = load_json_data('WBInquiry.json')
    elif category == "ETD REPORT":
        data = load_json_data('EtdReport.json')
    elif category == "EMERGENCY":
        data = load_json_data('Emergency.json')
    elif category == "Load Sheet REQUEST":
        data = load_json_data('WBRequest.json')
    elif category == "FUEL REQUEST":
        data = load_json_data('FuelRequest.json')
    elif category == "DE/ANTI ICING":
        data = load_json_data('DeAntiIcing.json')
    response = {
        'status': 0,
        'message': 'success',
        'data': data
    }
    return jsonify(response)


@app.route('/eofp/v1/ofp/<legIdentifier>/message', methods=['POST'])
def send_message(legIdentifier):
    data = request.json
    app.logger.info(f'Received data: {data}')
    min_val = 1
    max_val = 2 ** 63 - 1
    # 무작위 64비트 정수 생성
    random_64bit_int = random.randint(min_val, max_val)
    # 현재 날짜와 시간을 가져옵니다.
    current_datetime = datetime.now()
    # datetime을 타임스탬프(정수)로 변환합니다.
    timestamp = int(datetime.timestamp(current_datetime))
    response = {
        'status': 0,
        'message': 'success',
        'data': {
            'messageId': random_64bit_int,
            'createdDate': timestamp * 1000
        }
    }
    return jsonify(response)


@app.route('/eofp/v1/ofp/<legIdentifier>/messageattaches', methods=['POST'])
def send_message_with_files(legIdentifier):
    # JSON 데이터 접근
    json_data = request.form.get('json')
    if json_data:
        # 로그 기록
        app.logger.info(f'Received JSON data: {json_data}')
        # JSON 문자열을 파이썬 딕셔너리로 변환 (예시)
        # data = json.loads(json_data)

    # 여러 파일 데이터 접근
    files = request.files.getlist('file')  # 'file'은 여기서 클라이언트가 파일을 보내는 필드명입니다.

    if not files or files[0].filename == '':
        return jsonify({
            'status': 1,
            'message': 'no file error'
        })

    min_val = 1
    max_val = 2 ** 63 - 1

    messageFiles = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            app.logger.info(f'file: {file.filename}')
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # 무작위 64비트 정수 생성
            random_64bit_int = random.randint(min_val, max_val)
            # 현재 날짜와 시간을 가져옵니다.
            current_datetime = datetime.now()
            # datetime을 타임스탬프(정수)로 변환합니다.
            timestamp = int(datetime.timestamp(current_datetime))
            messageFiles.append({
                'fileNo': random_64bit_int,
                'createdDate': timestamp,
                'fileName': filename
            })

    # 무작위 64비트 정수 생성
    random_64bit_int = random.randint(min_val, max_val)
    # 현재 날짜와 시간을 가져옵니다.
    current_datetime = datetime.now()
    # datetime을 타임스탬프(정수)로 변환합니다.
    timestamp = int(datetime.timestamp(current_datetime))
    response = {
        'status': 0,
        'message': 'success',
        'data': {
            'messageId': random_64bit_int,
            'createdDate': timestamp,
            'messageFiles': messageFiles
        }
    }
    return jsonify(response)


@app.route('/eofp/v1/ofp/<legIdentifier>/comment', methods=['GET'])
def get_comments(legIdentifier):
    messageId = request.args.get('messageId', default=None, type=str)
    app.logger.info(f'Received category: {messageId}')
    data = load_json_data('comments.json')
    response = {
        'status': 0,
        'message': 'success',
        'data': data
    }
    return jsonify(response)


@app.route('/eofp/v1/ofp/<legIdentifier>/message/<messageId>/file', methods=['POST'])
def upload_message_file(legIdentifier, messageId):
    # 텍스트 필드 데이터 접근
    # file_name = request.form.get('file-url')  # 파일 이름 필드
    # creation_date = request.form.get('date')  # 생성일 필드

    # 로그 기록
    # app.logger.info(f'Received file_name: {file_name}, creation_date: {creation_date}')

    # 파일 데이터 접근
    if 'file' not in request.files:
        return jsonify({"message": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        min_val = 1
        max_val = 2 ** 63 - 1
        # 무작위 64비트 정수 생성
        random_64bit_int = random.randint(min_val, max_val)
        # 현재 날짜와 시간을 가져옵니다.
        current_datetime = datetime.now()
        # datetime을 타임스탬프(정수)로 변환합니다.
        timestamp = int(datetime.timestamp(current_datetime))
        response = {
            'status': 0,
            'message': 'success',
            'data': {
                'fileNo': random_64bit_int,
                'createdDate': timestamp
            }
        }
        return jsonify(response)


@app.route('/eofp/v1/ofp/<legIdentifier>/message/<messageId>/<fileNo>', methods=['GET'])
def download_message_file(legIdentifier, messageId, fileNo):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], "aaa.pdf")
    return send_file(file_path, as_attachment=True)


@app.route('/eofp/v1/ofp/<legIdentifier>/message/<messageId>/comment', methods=['POST'])
def send_comment(legIdentifier, messageId):
    data = request.json
    app.logger.info(f'Received data: {data}')
    min_val = 1
    max_val = 2 ** 63 - 1
    # 무작위 64비트 정수 생성
    random_64bit_int = random.randint(min_val, max_val)
    # 현재 날짜와 시간을 가져옵니다.
    current_datetime = datetime.now()
    # datetime을 타임스탬프(정수)로 변환합니다.
    timestamp = int(datetime.timestamp(current_datetime))
    response = {
        'status': 0,
        'message': 'success',
        'data': {
            'commentId': random_64bit_int,
            'createdDate': timestamp
        }
    }
    return jsonify(response)


@app.route('/eofp/v1/ofp/<legIdentifier>/message/<messageId>/commentattaches', methods=['POST'])
def send_comment_with_file(legIdentifier, messageId):
    # JSON 데이터 접근
    json_data = request.form.get('json')
    if json_data:
        # 로그 기록
        app.logger.info(f'Received JSON data: {json_data}')
        # JSON 문자열을 파이썬 딕셔너리로 변환 (예시)
        # data = json.loads(json_data)

    # 여러 파일 데이터 접근
    files = request.files.getlist('file')  # 'file'은 여기서 클라이언트가 파일을 보내는 필드명입니다.

    if not files or files[0].filename == '':
        return jsonify({
            'status': 1,
            'message': 'no file error'
        })

    min_val = 1
    max_val = 2 ** 63 - 1

    commentFiles = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            app.logger.info(f'file: {file.filename}')
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # 무작위 64비트 정수 생성
            random_64bit_int = random.randint(min_val, max_val)
            # 현재 날짜와 시간을 가져옵니다.
            current_datetime = datetime.now()
            # datetime을 타임스탬프(정수)로 변환합니다.
            timestamp = int(datetime.timestamp(current_datetime))
            commentFiles.append({
                'fileNo': random_64bit_int,
                'createdDate': timestamp,
                'fileName': filename
            })

    # 무작위 64비트 정수 생성
    random_64bit_int = random.randint(min_val, max_val)
    # 현재 날짜와 시간을 가져옵니다.
    current_datetime = datetime.now()
    # datetime을 타임스탬프(정수)로 변환합니다.
    timestamp = int(datetime.timestamp(current_datetime))
    response = {
        'status': 0,
        'message': 'success',
        'data': {
            'commentId': random_64bit_int,
            'createdDate': timestamp,
            'commentFiles': commentFiles
        }
    }
    return jsonify(response)


@app.route('/eofp/v1/ofp/<legIdentifier>/message/<messageId>/comment/<commentId>/file', methods=['POST'])
def upload_comment_file(legIdentifier, messageId, commentId):
    # 텍스트 필드 데이터 접근
    # file_name = request.form.get('file-url')  # 파일 이름 필드
    # creation_date = request.form.get('date')  # 생성일 필드

    # 로그 기록
    # app.logger.info(f'Received file_name: {file_name}, creation_date: {creation_date}')

    # 파일 데이터 접근
    if 'file' not in request.files:
        return jsonify({"message": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        min_val = 1
        max_val = 2 ** 63 - 1
        # 무작위 64비트 정수 생성
        random_64bit_int = random.randint(min_val, max_val)
        # 현재 날짜와 시간을 가져옵니다.
        current_datetime = datetime.now()
        # datetime을 타임스탬프(정수)로 변환합니다.
        timestamp = int(datetime.timestamp(current_datetime))
        response = {
            'status': 0,
            'message': 'success',
            'data': {
                'fileNo': random_64bit_int,
                'createdDate': timestamp
            }
        }
        return jsonify(response)


@app.route('/eofp/v1/ofp/<legIdentifier>/message/<messageId>/comment/<commentId>/<fileNo>', methods=['GET'])
def download_comment_file(legIdentifier, messageId, commentId, fileNo):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], "aaa.jpg")
    return send_file(file_path, as_attachment=True)


@app.route('/uploadfiles', methods=['POST'])
def upload_files():
    # JSON 데이터 접근
    json_data = request.form.get('json_data')
    if json_data:
        # 로그 기록
        app.logger.info(f'Received JSON data: {json_data}')
        # JSON 문자열을 파이썬 딕셔너리로 변환 (예시)
        # data = json.loads(json_data)

    # 여러 파일 데이터 접근
    files = request.files.getlist('file')  # 'file'은 여기서 클라이언트가 파일을 보내는 필드명입니다.

    if not files or files[0].filename == '':
        return jsonify({
        'status': 1,
        'message': 'error'
        })

    file_urls = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            app.logger.info(f'file: {file.filename}')
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_urls.append(file_path)

    min_val = 1
    max_val = 2 ** 63 - 1
    # 무작위 64비트 정수 생성
    random_64bit_int = random.randint(min_val, max_val)
    # 현재 날짜와 시간을 가져옵니다.
    current_datetime = datetime.now()
    # datetime을 타임스탬프(정수)로 변환합니다.
    timestamp = int(datetime.timestamp(current_datetime))
    response = {
        'status': 0,
        'message': 'success',
        'data': {
            'fileNo': random_64bit_int,
            'createdDate': timestamp,
        }
    }
    return jsonify(response)


@app.route('/eofp/v1/ofp/search', methods=['GET'])
def search_ofp():
    data = load_json_data('search-plan.json')
    response = {
        'status': 0,
        'message': 'success',
        'data': data
    }
    return jsonify(response)


@app.route('/eofp/v1/ofp/add', methods=['POST'])
def add_flight_plan():
    response = {
        'status': 0,
        'message': 'success',
    }
    return jsonify(response)


@app.route('/eofp/v1/code/actype', methods=['GET'])
def get_aircraft_types():
    response = {
        'status': 0,
        'message': 'success',
        'data': {
            'code': ["320", "321", "32Q", "333", "359", "388", "744", "74Y", "763", "76Y", "77L"]
        }
    }
    return jsonify(response)


def load_json_data(filename):
    with open(filename) as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    app.run(debug=True)
