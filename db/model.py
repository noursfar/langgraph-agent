# db/model.py
from sqlalchemy.ext.mutable import MutableList
from db import db
from datetime import datetime, timezone


class Conversation(db.Model):
    """Represents a conversation session with the PDS assistant."""
    __tablename__ = "conversations"
    __table_args__ = {'schema': 'agent'}

    id = db.Column(db.Integer, primary_key=True)

    hr_id = db.Column(db.String(100), nullable=False)
    pds_id = db.Column(db.String(100), nullable=False)

    full_history = db.Column(MutableList.as_mutable(db.JSON), nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Conversation id={self.id} pds_id={self.pds_id} hr_id={self.hr_id}>"
