
from flask import Flask, jsonify, request, send_from_directory
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import uuid

# Import the agents
from DataGenerator.agent import root_agent as DataGeneratorAgent
from MultiToolAgent.agent import root_agent as MultiToolAgent

app = Flask(__name__, static_folder='frontend')

# Create a session service
session_service = InMemorySessionService()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route("/api/<agent_name>", methods=['POST'])
def interact(agent_name):
    if agent_name == "DataGeneratorAgent":
        agent = DataGeneratorAgent
    elif agent_name == "MultiToolAgent":
        agent = MultiToolAgent
    else:
        return jsonify({"error": "Agent not found"}), 404

    data = request.get_json()
    prompt = data.get('prompt')
    session_id = data.get('session_id')

    if not session_id:
        session_id = str(uuid.uuid4())

    runner = Runner(agent=agent, session_service=session_service)
    response = runner.run(session_id=session_id, prompt=prompt)

    return jsonify({"response": response.top_response, "session_id": session_id})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

