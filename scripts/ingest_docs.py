# scripts/ingest_docs.py
import click
from agent_core.rag.ingest import ingest_document
from agent_core.utils.exceptions import IngestionError

@click.command()
@click.argument("file_path")
def ingest_docs(file_path):
    try:
        ingest_document(file_path)
        click.echo(f"Successfully ingested {file_path}")
    except IngestionError as e:
        click.echo(f"Error: {str(e)}")


# python -m scripts.ingest_docs data/documents/livretaccueilpatient.pdf
if __name__ == "__main__":
    ingest_docs()