"""Unit tests for summarization engine."""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from backend.app.summarizer.engine import SummarizationEngine
from backend.app.errors import SummarizationError
from backend.app.config import settings


class TestSummarizationEngine:
    """Tests for the summarization engine."""

    @pytest.fixture
    def engine(self):
        """Create engine instance for testing."""
        return SummarizationEngine()

    def test_get_summary_length_instruction_short(self, engine):
        """Test short summary instruction."""
        word_count, instruction = engine._get_summary_length_instruction("short")
        assert word_count == settings.SUMMARY_LENGTH_SHORT
        assert "short" in instruction.lower() or str(settings.SUMMARY_LENGTH_SHORT) in instruction

    def test_get_summary_length_instruction_medium(self, engine):
        """Test medium summary instruction."""
        word_count, instruction = engine._get_summary_length_instruction("medium")
        assert word_count == settings.SUMMARY_LENGTH_MEDIUM
        assert "moderate" in instruction.lower() or str(settings.SUMMARY_LENGTH_MEDIUM) in instruction

    def test_get_summary_length_instruction_long(self, engine):
        """Test long summary instruction."""
        word_count, instruction = engine._get_summary_length_instruction("long")
        assert word_count == settings.SUMMARY_LENGTH_LONG
        assert "comprehensive" in instruction.lower() or str(settings.SUMMARY_LENGTH_LONG) in instruction

    @pytest.mark.asyncio
    async def test_generate_summary_empty_text(self, engine):
        """Test summarization with empty text."""
        with pytest.raises(SummarizationError):
            await engine.generate_summary("", "medium")

    @pytest.mark.asyncio
    async def test_generate_summary_no_client(self):
        """Test summarization when Azure OpenAI client is not configured."""
        engine = SummarizationEngine()
        engine.client = None

        with pytest.raises(SummarizationError) as exc_info:
            await engine.generate_summary("Some text", "medium")

        assert "not configured" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_generate_summary_api_error(self, engine):
        """Test summarization when API call fails."""
        engine.client = MagicMock()
        engine.client.chat.completions.create.side_effect = Exception("API Error")

        with pytest.raises(SummarizationError):
            await engine.generate_summary("Some text to summarize", "medium")

    def test_engine_initialization(self):
        """Test engine initialization."""
        engine = SummarizationEngine()
        assert engine is not None
