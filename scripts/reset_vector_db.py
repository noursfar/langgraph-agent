# scripts/reset_vector_db.py
import click
from agent_core.rag.vector_store import VectorStore
from agent_core.utils.exceptions import VectorStoreError

@click.command()
def reset_vector_db():
    try:
        vector_store = VectorStore()
        vector_store.reset()
        click.echo("Vector store successfully reset")
    except VectorStoreError as e:
        click.echo(f"Error: {str(e)}")

if __name__ == "__main__":
    reset_vector_db()
