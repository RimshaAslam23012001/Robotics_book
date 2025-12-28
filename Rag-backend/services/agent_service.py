import openai
from typing import Dict, Any, Optional
from datetime import datetime
from config import OPENAI_API_KEY
import logging
import asyncio
import time
import re

logger = logging.getLogger(__name__)

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY


class AgentService:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        self.model = "gpt-4-turbo"  # Using GPT-4 Turbo for better performance and cost
        self.timeout = 30  # seconds

    def translate_to_urdu(
        self,
        chapter_content: str,
        preserve_code_blocks: bool = True
    ) -> Optional[str]:
        """
        Translate chapter content to Urdu while preserving markdown structure.

        Args:
            chapter_content: The original chapter content in markdown format
            preserve_code_blocks: Whether to preserve code blocks without translation

        Returns:
            Translated content in Urdu or None if failed
        """
        try:
            start_time = time.time()

            # Create the system prompt with Urdu translation instructions
            system_prompt = self._create_urdu_translation_prompt(preserve_code_blocks)

            # Create the user message with chapter content
            user_message = f"""
            Here is the chapter content to translate to Urdu:

            {chapter_content}

            Please translate this content to clear, simple Urdu while maintaining the original markdown structure and technical accuracy.
            """

            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,  # Lower temperature for more consistent translation
                max_tokens=4000,  # Adjust based on content length
                timeout=self.timeout
            )

            translated_content = response.choices[0].message.content.strip()
            processing_time = time.time() - start_time

            logger.info(f"Content translation to Urdu completed in {processing_time:.2f}s")

            return translated_content

        except openai.error.Timeout as e:
            logger.error(f"OpenAI API timeout: {e}")
            return None
        except openai.error.RateLimitError as e:
            logger.error(f"OpenAI rate limit error: {e}")
            return None
        except openai.error.AuthenticationError as e:
            logger.error(f"OpenAI authentication error: {e}")
            return None
        except openai.error.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in Urdu translation: {e}")
            return None

    async def translate_to_urdu_async(
        self,
        chapter_content: str,
        preserve_code_blocks: bool = True
    ) -> Optional[str]:
        """
        Async version of translate_to_urdu for better performance.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.translate_to_urdu,
            chapter_content,
            preserve_code_blocks
        )

    def _create_urdu_translation_prompt(self, preserve_code_blocks: bool) -> str:
        """
        Create a system prompt for Urdu translation with markdown preservation.
        """
        instructions = [
            "You are a professional translator specializing in technical content translation to Urdu.",
            "Your task is to translate the provided content to clear, simple Urdu suitable for learners while preserving:",
            "- The original markdown structure (headings, lists, emphasis)",
            "- Code blocks, formulas, and technical syntax (do not translate these)",
            "- Links, references, and citations",
            "- Mathematical expressions and scientific notation",
            "",
            "Translation guidelines:",
            "- Translate explanations, descriptions, and narrative text to Urdu",
            "- Keep technical terms in English where appropriate, with Urdu explanations if needed",
            "- Maintain the logical flow and meaning of the content",
            "- Use simple, readable Urdu that is accessible to learners",
            "- Preserve all markdown formatting and structure exactly",
        ]

        if preserve_code_blocks:
            instructions.extend([
                "",
                "Special handling for code blocks:",
                "- Do NOT translate any content inside code blocks (``` ... ``` or indented code)",
                "- Do NOT translate programming language keywords (if, else, for, function, etc.)",
                "- Do NOT translate variable names, function names, or class names",
                "- Do NOT translate comments inside code blocks",
                "- Keep all code syntax exactly as is",
            ])

        instructions.append("\nReturn only the translated markdown content without any additional commentary.")

        return "\n".join(instructions)

    def personalize_content(
        self,
        chapter_content: str,
        user_background: Dict[str, Any],
        learning_goal: Optional[str] = None
    ) -> Optional[str]:
        """
        Personalize chapter content based on user background and learning goals.
        """
        try:
            start_time = time.time()

            # Create the system prompt with personalization instructions
            system_prompt = self._create_personalization_prompt(user_background, learning_goal)

            # Create the user message with chapter content
            user_message = f"""
            Here is the chapter content to personalize:

            {chapter_content}

            Please personalize this content according to the user's background and preferences while maintaining the original markdown structure.
            """

            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.4,  # Slightly higher for more creative personalization
                max_tokens=4000,
                timeout=self.timeout
            )

            personalized_content = response.choices[0].message.content.strip()
            processing_time = time.time() - start_time

            logger.info(f"Content personalization completed in {processing_time:.2f}s")

            return personalized_content

        except openai.error.Timeout as e:
            logger.error(f"OpenAI API timeout: {e}")
            return None
        except openai.error.RateLimitError as e:
            logger.error(f"OpenAI rate limit error: {e}")
            return None
        except openai.error.AuthenticationError as e:
            logger.error(f"OpenAI authentication error: {e}")
            return None
        except openai.error.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in content personalization: {e}")
            return None

    def _create_personalization_prompt(self, user_background: Dict[str, Any], learning_goal: Optional[str]) -> str:
        """
        Create a system prompt for content personalization based on user background.
        """
        instructions = [
            "You are an expert educator and content personalization specialist.",
            "Your task is to adapt the provided educational content to match the user's background and learning preferences.",
            "",
            "User Background Information:",
            f"- Technical Depth: {user_background.get('technicalDepth', 'intermediate')}",
            f"- Terminology Complexity: {user_background.get('terminologyComplexity', 'moderate')}",
            f"- Example Focus: {user_background.get('exampleFocus', 'mixed')}",
            f"- AI/ML Concept Level: {user_background.get('aiConceptLevel', 'intermediate')}",
        ]

        if learning_goal:
            instructions.extend([
                "",
                f"Learning Goal: {learning_goal}",
                "Adapt the content to help achieve this specific learning goal."
            ])

        instructions.extend([
            "",
            "Personalization Guidelines:",
            "- Adjust the complexity of explanations based on the user's technical depth",
            "- Modify terminology usage based on the user's preferred complexity level",
            "- Include or emphasize examples according to the user's example focus preference",
            "- Adjust AI/ML concept explanations based on the user's experience level",
            "- Maintain the original markdown structure and formatting",
            "- Preserve code blocks, formulas, and technical syntax exactly as is",
            "- Add relevant explanations or simplify concepts as needed for the user's level",
            "- Keep all links, references, and citations intact",
        ])

        instructions.append("\nReturn only the personalized markdown content without any additional commentary.")

        return "\n".join(instructions)

    def extract_code_blocks(self, content: str) -> tuple:
        """
        Extract code blocks from content to preserve during translation.
        Returns the content with placeholders and a list of code blocks.
        """
        code_blocks = []
        # Pattern to match both inline and fenced code blocks
        pattern = r'(```.*?```|`.*?`|    .+?(?=\n\n|\Z))'

        def replace_code(match):
            code = match.group(0)
            index = len(code_blocks)
            code_blocks.append(code)
            return f"__CODE_BLOCK_{index}__"

        processed_content = re.sub(pattern, replace_code, content, flags=re.DOTALL)
        return processed_content, code_blocks

    def restore_code_blocks(self, content: str, code_blocks: list) -> str:
        """
        Restore code blocks back to translated content.
        """
        result = content
        for i, code_block in enumerate(code_blocks):
            placeholder = f"__CODE_BLOCK_{i}__"
            result = result.replace(placeholder, code_block)
        return result


# Global instance of AgentService
agent_service = AgentService()