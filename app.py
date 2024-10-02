from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Lấy API key từ biến môi trường
api_key = os.environ.get('API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    # Lấy văn bản từ form
    text = request.form.get('text')
    voice = request.form.get('voice', 'banmai')  # Giọng mặc định là 'banmai'
    speed = request.form.get('speed', 0)  # Tốc độ mặc định là 0

    if not api_key:
        return jsonify({"error": "API key chưa được cấu hình."}), 500

    # Kiểm tra và in văn bản trước khi xử lý
    print(f"Văn bản gốc từ form: {text}")

    # Đảm bảo văn bản được mã hóa bằng UTF-8
    if text:
        try:
            text = text.strip().encode('utf-8').decode('utf-8')
            print(f"Văn bản sau khi mã hóa UTF-8: {text}")
        except UnicodeEncodeError as e:
            print(f"Lỗi mã hóa UTF-8: {e}")
            return jsonify({"error": "Lỗi mã hóa UTF-8."}), 400

    url = "https://api.fpt.ai/hmi/tts/v5"
    headers = {
        "api_key": api_key,
        "voice": voice,
        "speed": str(speed),
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "text": text  # Đảm bảo văn bản đã loại bỏ khoảng trắng thừa
    }

    # In ra dữ liệu trước khi gửi đến API
    print(f"Dữ liệu gửi đến API: {data}")

    # Gửi yêu cầu tới API
    response = requests.post(url, headers=headers, json=data)

    # Kiểm tra phản hồi từ API
    if response.status_code == 200:
        result = response.json()
        print(f"Phản hồi từ API: {result}")

        # In ra phần URL của âm thanh nếu có
        if result.get("async"):
            print(f"URL âm thanh: {result['async']}")
            return jsonify({"audio_url": result["async"]})
        else:
            return jsonify({"error": "Không có liên kết âm thanh trả về."}), 400
    else:
        print(f"Lỗi khi gửi yêu cầu: {response.status_code}")
        return jsonify({"error": "Lỗi khi gửi yêu cầu."}), response.status_code

# Route để kiểm tra Flask có hoạt động hay không
@app.route('/test')
def test():
    return "Hello, Flask is working!"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
