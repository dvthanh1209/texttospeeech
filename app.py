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
    text = request.form.get('text')  # Lấy văn bản từ form
    voice = request.form.get('voice', 'banmai')  # Lấy giọng từ form, mặc định là 'banmai'
    speed = request.form.get('speed', 0)  # Lấy tốc độ từ form, mặc định là 0

    # Kiểm tra nếu API key chưa được cấu hình
    if not api_key:
        return jsonify({"error": "API key chưa được cấu hình."}), 500

    # In ra văn bản được gửi đi để kiểm tra
    print(f"Văn bản gửi đi: {text.strip()}")

    url = "https://api.fpt.ai/hmi/tts/v5"
    headers = {
        "api_key": api_key,
        "voice": voice,
        "speed": str(speed),
        "Content-Type": "application/json",
    }
    data = {
        "text": text.strip()  # Đảm bảo chỉ gửi văn bản đã loại bỏ khoảng trắng thừa
    }
    data = {
        "text": "xin chào bạn, tên tôi là nguyên văn A"
    }

    response = requests.post(url, headers=headers, json=data)

    # Kiểm tra trạng thái phản hồi từ API
    if response.status_code == 200:
        result = response.json()
        if result.get("async"):
            return jsonify({"audio_url": result["async"]})
        else:
            return jsonify({"error": "Không có liên kết âm thanh trả về."}), 400
    else:
        return jsonify({"error": "Lỗi khi gửi yêu cầu."}), response.status_code

# Route để kiểm tra Flask có hoạt động hay không
@app.route('/test')
def test():
    return "Hello, Flask is working!"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
