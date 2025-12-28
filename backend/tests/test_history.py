"""Unit tests for history tracking."""
import pytest
from datetime import datetime

from backend.app.api import summaries_db, users_db


class TestHistory:
    """Tests for summary history tracking."""

    def setup_method(self):
        """Clear databases before each test."""
        summaries_db.clear()
        users_db.clear()

    def test_add_summary_to_history(self):
        """Test adding a summary to user history."""
        user_id = "test_user"
        summary_id = "summary_1"

        summary_record = {
            "id": summary_id,
            "text": "Original text",
            "summary": "Summary text",
            "length": "medium",
            "created_at": datetime.utcnow().isoformat(),
            "user_id": user_id,
        }

        summaries_db[summary_id] = summary_record

        if user_id not in users_db:
            users_db[user_id] = []
        users_db[user_id].append(summary_id)

        assert summary_id in summaries_db
        assert summary_id in users_db[user_id]

    def test_multiple_summaries_per_user(self):
        """Test storing multiple summaries per user."""
        user_id = "test_user"

        for i in range(5):
            summary_id = f"summary_{i}"
            summary_record = {
                "id": summary_id,
                "text": f"Text {i}",
                "summary": f"Summary {i}",
                "length": "medium",
                "created_at": datetime.utcnow().isoformat(),
                "user_id": user_id,
            }
            summaries_db[summary_id] = summary_record

            if user_id not in users_db:
                users_db[user_id] = []
            users_db[user_id].append(summary_id)

        assert len(users_db[user_id]) == 5

    def test_retrieve_user_summaries(self):
        """Test retrieving all summaries for a user."""
        user_id = "test_user"
        summary_ids = ["summary_1", "summary_2", "summary_3"]

        for summary_id in summary_ids:
            summary_record = {
                "id": summary_id,
                "text": f"Text",
                "summary": f"Summary",
                "length": "medium",
                "created_at": datetime.utcnow().isoformat(),
                "user_id": user_id,
            }
            summaries_db[summary_id] = summary_record

            if user_id not in users_db:
                users_db[user_id] = []
            users_db[user_id].append(summary_id)

        user_summaries = users_db.get(user_id, [])
        retrieved = [summaries_db[sid] for sid in user_summaries if sid in summaries_db]

        assert len(retrieved) == 3
        assert all(s["user_id"] == user_id for s in retrieved)

    def test_delete_summary_from_history(self):
        """Test removing a summary from history."""
        user_id = "test_user"
        summary_id = "summary_1"

        summary_record = {
            "id": summary_id,
            "text": "Text",
            "summary": "Summary",
            "length": "medium",
            "created_at": datetime.utcnow().isoformat(),
            "user_id": user_id,
        }

        summaries_db[summary_id] = summary_record
        users_db[user_id] = [summary_id]

        # Delete
        del summaries_db[summary_id]
        users_db[user_id].remove(summary_id)

        assert summary_id not in summaries_db
        assert summary_id not in users_db[user_id]
