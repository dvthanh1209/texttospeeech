from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Khóa API
api_key = "3hlR0ZtgRGnHh2lK2RBM582L4VYOOfiy"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form.get('text')
    voice = request.form.get('voice', 'banmai')
    speed = request.form.get('speed', 0)

    url = "https://api.fpt.ai/hmi/tts/v5"
    headers = {
        "api_key": api_key,
        "voice": voice,
        "speed": str(speed),
        "Content-Type": "application/json",
    }
    data = {
        "text": text  # Gửi chỉ văn bản nhập vào
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        if result.get("async"):
            return jsonify({"audio_url": result["async"]})
        else:
            return jsonify({"error": "Không có liên kết âm thanh trả về."}), 400
    else:
        return jsonify({"error": "Lỗi khi gửi yêu cầu."}), response.status_code

if __name__ == "__main__":
    app.run(debug=True)
@app.route('/test')
def test():
    return "Hello, Flask is working!"
