# api/routes/initialize.py
import uuid
from flask import request, jsonify, session
from flask_smorest import Blueprint

from agent_core.agent.base_agent import create_agent
from agent_core.utils.logger import log
from api.schemas.requests import InitializeRequest
from api.schemas.responses import InitializeResponse
from api.utils.agent_store import set_agent

initialize_bp = Blueprint('initialize', __name__, url_prefix='/api')


@initialize_bp.route('/v1/pds/initialize', methods=['POST'])
def initialize_session():
    try:
        data = request.get_json()
        init_request = InitializeRequest(**data)
        log.info(f"Initializing session for userId: {init_request.userId}")

        session['user_type'] = "PDS"

        session_id = str(uuid.uuid4())
        session['session_id'] = session_id

        agent = create_agent(init_request.userId, init_request.token)
        set_agent(session_id, agent)
        log.info("Agent initialized for session: %s", session_id)

        response = InitializeResponse(success=True, session_id=session_id, error=None)
        return jsonify(response.model_dump()), 200

    except Exception as e:
        log.exception(f"Failed to initialize session: {e}")
        response = InitializeResponse(success=False, session_id=None, error=str(e))
        return jsonify(response.model_dump()), 500


@initialize_bp.route('/v1/pds/initialize', methods=['GET'])
def initialize_get():
    return jsonify({"error": "Method not allowed, use POST"}), 405
