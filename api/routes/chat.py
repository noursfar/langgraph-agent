# api/routes/chat.py
from flask import request, jsonify
from flask_smorest import Blueprint

from agent_core.agent.executor import run_agent
from agent_core.utils.logger import log
from api.schemas.requests import ChatRequest
from api.schemas.responses import ChatResponse
from api.utils.agent_store import get_agent

chat_bp = Blueprint('chat', __name__, url_prefix='/api')


@chat_bp.route('/v1/pds/chat/<session_id>', methods=['POST'])
def chat(session_id):
    try:
        # Parse and validate request
        data = request.get_json()
        chat_request = ChatRequest(**data)

        log.info(f"Chat request for session: {session_id}")

        # Retrieve agent from store
        agent = get_agent(session_id)
        if not agent:
            log.error(f"Agent not found for session: {session_id}")
            response = ChatResponse(success=False, response=None, session_id=session_id, error="Session not found. Please initialize first.")
            return jsonify(response.model_dump()), 404

        # Run the agent with the user's message
        result = run_agent(agent, chat_request.message, session_id)

        if "error" in result:
            response = ChatResponse(success=False, response=None, session_id=session_id, error=result["error"])
            return jsonify(response.model_dump()), 500

        # Build success response
        response = ChatResponse(success=True, response=result["response"], session_id=session_id, error=None)

        return jsonify(response.model_dump()), 200

    except Exception as e:
        log.exception(f"Chat failed for session {session_id}: {e}")
        response = ChatResponse(success=False, response=None, session_id=session_id, error=str(e))
        return jsonify(response.model_dump()), 500


@chat_bp.route('/v1/pds/chat/<session_id>', methods=['GET'])
def chat_get():
    return jsonify({"error": "Method not allowed, use POST"}), 405