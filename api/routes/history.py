# api/routes/history.py
from flask import jsonify
from flask_smorest import Blueprint
from langchain_community.chat_message_histories import SQLChatMessageHistory
from typing import Any, Dict


from agent_core.config.settings import settings
from agent_core.utils.logger import log
from api.schemas.responses import HistoryResponse

history_bp = Blueprint('history', __name__, url_prefix='/api')


@history_bp.route('/v1/pds/history/<session_id>', methods=['GET'])
def get_history(session_id):
    """Retrieve conversation history for a session"""
    try:
        log.info(f"Fetching history for session: {session_id}")

        # Initialize chat history from database
        chat_history = SQLChatMessageHistory(session_id=session_id, connection=settings.local_db_url, table_name="history")

        # Get all messages
        messages = chat_history.messages

        # Convert messages to dict format
        messages_dict = []
        for msg in messages:
            message_data : Dict[str, Any] = {
                "type": msg.type,
                "content": msg.content
            }

            # If content is empty and there are tool calls, show tool calls instead
            if not msg.content and hasattr(msg, 'tool_calls') and msg.tool_calls:
                message_data["tool_call"] = {
                    "name": msg.tool_calls[0].get("name"),
                    "args": msg.tool_calls[0].get("args")
                }

            messages_dict.append(message_data)

        log.info(f"Retrieved {len(messages_dict)} messages for session: {session_id}")

        response = HistoryResponse(success=True, session_id=session_id, messages=messages_dict, error=None)

        return jsonify(response.model_dump()), 200

    except Exception as e:
        log.exception(f"Failed to fetch history for session {session_id}: {e}")
        response = HistoryResponse(success=False, session_id=session_id, messages=None, error=str(e))
        return jsonify(response.model_dump()), 500


@history_bp.route('/v1/pds/history/<session_id>', methods=['POST'])
def post_history():
    return jsonify({"error": "Method not allowed, use GET"}), 405
