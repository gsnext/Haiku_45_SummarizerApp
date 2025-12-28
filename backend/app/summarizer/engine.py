"""Summarization engine using Azure OpenAI."""
from typing import Literal
from openai import AzureOpenAI
from ..errors import SummarizationError
from ..logger import logger
from ..config import settings


class SummarizationEngine:
    """Engine for generating summaries using Azure OpenAI."""

    def __init__(self):
        """Initialize the summarization engine with Azure OpenAI client."""
        if not settings.AZURE_OPENAI_API_KEY or not settings.AZURE_OPENAI_ENDPOINT:
            logger.warning("Azure OpenAI credentials not configured")
            self.client = None
        else:
            self.client = AzureOpenAI(
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version="2024-02-15-preview",
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            )

    def _get_summary_length_instruction(
        self, length: Literal["short", "medium", "long"]
    ) -> tuple[int, str]:
        """Get word count target and instruction for the summary length."""
        length_config = {
            "short": (settings.SUMMARY_LENGTH_SHORT, f"Create a very brief summary of approximately {settings.SUMMARY_LENGTH_SHORT} words."),
            "medium": (settings.SUMMARY_LENGTH_MEDIUM, f"Create a moderate summary of approximately {settings.SUMMARY_LENGTH_MEDIUM} words."),
            "long": (settings.SUMMARY_LENGTH_LONG, f"Create a comprehensive summary of approximately {settings.SUMMARY_LENGTH_LONG} words."),
        }
        return length_config.get(length, length_config["medium"])

    async def generate_summary(
        self,
        text: str,
        length: Literal["short", "medium", "long"] = "medium",
    ) -> str:
        """
        Generate a summary of the provided text.

        Args:
            text: Text to summarize
            length: Desired summary length (short, medium, long)

        Returns:
            Generated summary

        Raises:
            SummarizationError: If summarization fails
        """
        if not self.client:
            raise SummarizationError(
                "Azure OpenAI is not configured. Please set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT."
            )

        if not text or not text.strip():
            raise SummarizationError("Cannot summarize empty text")

        try:
            word_count, instruction = self._get_summary_length_instruction(length)

            message = f"""{instruction}

Text to summarize:
{text}

Summary:"""

            logger.info(f"Generating {length} summary for text of length {len(text)}")

            response = self.client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a concise and helpful assistant that creates accurate summaries of documents.",
                    },
                    {"role": "user", "content": message},
                ],
                temperature=0.5,
                max_tokens=500,
            )

            summary = response.choices[0].message.content.strip()
            logger.info(f"Successfully generated summary ({len(summary)} chars)")
            return summary

        except Exception as e:
            logger.error(f"Summarization failed: {str(e)}")
            raise SummarizationError(f"Failed to generate summary: {str(e)}")


# Global instance
engine = SummarizationEngine()
