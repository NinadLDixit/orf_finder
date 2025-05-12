from flask import Flask, request, jsonify
from orf_finder import find_orfs

app = Flask(__name__)

@app.route('/api/find_orfs', methods=['POST'])
def find_orfs_api():
    data = request.json
    sequence = data.get("sequence", "")
    min_length = data.get("min_length", 100)

    if not sequence:
        return jsonify({"error": "No DNA sequence provided"}), 400

    try:
        orfs = find_orfs(sequence, min_length)
        return jsonify({"orfs": orfs, "count": len(orfs)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
