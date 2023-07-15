from flask import Flask, jsonify, request, send_file
import visualization

app = Flask(__name__)

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    # Parse connections from request data
    # connections = request.json.get('connections', [])
    before = request.json.get('Before')
    after = request.json.get('After')
    step_num = request.json.get('StepNum')


    # Create a Step instance
    step = visualization.Step()

    # Run simulation steps
    step.exec([before, after], step_num)

    return jsonify({'message': 'Simulation run successfully.'})

@app.route('/get_gif', methods=['GET'])
def get_gif():
    # Convert images to GIF
    visualization.convertToGif()

    return send_file('agents.gif', mimetype='image/gif')

if __name__ == '__main__':
    app.run(debug=True)
