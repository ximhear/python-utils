from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    # JSON 데이터 추출
    json_data = request.form.get('json')
    if json_data:
        json_data = json.loads(json_data)
    else:
        return jsonify({'error': 'No JSON data found'}), 400

    # 파일 추출
    file = request.files.get('file')
    if file:
        # 파일 저장 또는 처리
        file.save('path_to_save/' + file.filename)
    else:
        return jsonify({'error': 'No file found'}), 400

    # 성공 응답
    return jsonify({'message': 'File and JSON data received', 'json_data': json_data})

if __name__ == '__main__':
    app.run(debug=True)
