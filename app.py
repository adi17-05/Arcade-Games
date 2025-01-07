from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('arcade.html')

@app.route('/run-game', methods=['POST'])
def run_game():
    game = request.json.get('game')
    try:
        result = subprocess.run(['python', f'{game}.py'], capture_output=True, text=True)
        return jsonify({"output": result.stdout})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
