# api/routes/documents.py
from flask import request, jsonify
from flask_smorest import Blueprint
from werkzeug.utils import secure_filename

from agent_core.rag.config import DOCUMENTS_DIR
from agent_core.rag.ingest import ingest_document
from agent_core.rag.vector_store import VectorStore
from agent_core.utils.logger import log
from api.schemas.requests import DocumentDeleteRequest
from api.schemas.responses import DocumentUploadResponse, DocumentDeleteResponse, DocumentListResponse


documents_bp = Blueprint('documents', __name__, url_prefix='/api')

# Configuration
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@documents_bp.route('/v1/pds/documents', methods=['POST'])
def upload_document():
    """ Upload and ingest a document into a clinic's collection """
    # Check if file is in request
    if 'file' not in request.files:
        response = DocumentUploadResponse(success=False, filename=None, hr_id=None, chunks_count=None,
                                          error="No file provided")
        return jsonify(response.model_dump()), 400

    file = request.files['file']
    hr_id = request.form.get('hrId')

    if not hr_id:
        response = DocumentUploadResponse(success=False, filename=None, hr_id=None, chunks_count=None,
                                          error="hr_id is required")
        return jsonify(response.model_dump()), 400

    # Validate file type
    if not allowed_file(file.filename):
        response = DocumentUploadResponse(success=False, filename=file.filename, hr_id=hr_id, chunks_count=None,
                                          error=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}")
        return jsonify(response.model_dump()), 400
    # Secure the filename
    filename = secure_filename(file.filename)

    try:
        # Create upload folder if it doesn't exist
        DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

        # Save file
        file_path = DOCUMENTS_DIR / filename
        file.save(str(file_path))

        log.info(f"File saved to: {file_path}")

        # Ingest document into ChromaDB with hr_id as collection name
        collection_name = f"clinic_{hr_id}"
        ingest_document(str(file_path), collection_name)

        # Get chunks count
        vector_store = VectorStore(collection_name)
        chunks_count = vector_store.count()

        log.info(f"Document ingested: {filename} into collection {collection_name}")

        response = DocumentUploadResponse(success=True, filename=filename, hr_id=hr_id, chunks_count=chunks_count,
                                          error=None)

        return jsonify(response.model_dump()), 201

    except Exception as e:
        log.exception(f"Upload failed: {e}")
        response = DocumentUploadResponse(success=False, filename=filename if 'filename' in locals() else None,
                                          hr_id=hr_id if 'hr_id' in locals() else None, chunks_count=None, error=str(e))
        return jsonify(response.model_dump()), 500


@documents_bp.route('/v1/pds/documents', methods=['DELETE'])
def delete_document():
    """ Delete a document from a clinic's collection """
    data = request.get_json()
    delete_request = DocumentDeleteRequest(**data)

    log.info(f"Deleting document: {delete_request.filename} from hr_id: {delete_request.hrId}")

    try:
        # Initialize vector store for the clinic's collection
        collection_name = f"clinic_{delete_request.hrId}"
        vector_store = VectorStore(collection_name)

        # Delete document from vector store
        vector_store.delete_by_source(delete_request.filename)

        # delete physical file
        file_path = DOCUMENTS_DIR / delete_request.filename
        if file_path.exists():
            file_path.unlink()
            log.info(f"Physical file deleted: {file_path}")

        response = DocumentDeleteResponse(success=True, filename=delete_request.filename, hr_id=delete_request.hrId,
                                          error=None)
        return jsonify(response.model_dump()), 200

    except Exception as e:
        log.exception(f"Delete failed: {e}")
        response = DocumentDeleteResponse(success=False,
                                          filename=delete_request.filename if 'delete_request' in locals() else None,
                                          hr_id=delete_request.hrId if 'delete_request' in locals() else None,
                                          error=str(e))
        return jsonify(response.model_dump()), 500


@documents_bp.route('/v1/pds/documents/<hr_id>', methods=['GET'])
def list_documents(hr_id):
    """ List all documents in a clinic's collection """
    try:
        log.info(f"Listing documents for hr_id: {hr_id}")

        # Initialize vector store for the clinic's collection
        collection_name = f"clinic_{hr_id}"
        vector_store = VectorStore(collection_name)

        # Get list of sources
        documents = vector_store.list_sources()
        total_chunks = vector_store.count()

        response = DocumentListResponse(success=True, hr_id=hr_id, documents=documents, total_chunks=total_chunks,
                                        error=None)
        return jsonify(response.model_dump()), 200

    except Exception as e:
        log.exception(f"List documents failed: {e}")
        response = DocumentListResponse(success=False, hr_id=hr_id, documents=None, total_chunks=None, error=str(e))
        return jsonify(response.model_dump()), 500