from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of content and metadata verification."""
    is_content_valid: bool
    is_metadata_valid: bool
    content_diff: Optional[str] = None
    metadata_diff: Optional[str] = None


class RetrievalValidator:
    """Validator for checking content accuracy and metadata integrity."""

    def validate_content_fidelity(self, retrieved_content: str, original_content: str) -> bool:
        """
        Validate that retrieved content matches original content exactly.

        Args:
            retrieved_content: Content retrieved from Qdrant
            original_content: Original content for comparison

        Returns:
            True if content matches exactly, False otherwise
        """
        return retrieved_content == original_content

    def validate_metadata_integrity(self, retrieved_metadata: Dict[str, Any], expected_metadata: Dict[str, Any]) -> bool:
        """
        Validate that retrieved metadata matches expected metadata.

        Args:
            retrieved_metadata: Metadata retrieved from Qdrant
            expected_metadata: Expected metadata for comparison

        Returns:
            True if metadata matches, False otherwise
        """
        # Check if all expected keys exist in retrieved metadata
        for key, expected_value in expected_metadata.items():
            if key not in retrieved_metadata:
                return False
            if retrieved_metadata[key] != expected_value:
                return False

        return True

    def validate_url_format(self, url: str) -> bool:
        """
        Validate URL format.

        Args:
            url: URL to validate

        Returns:
            True if URL format is valid, False otherwise
        """
        if not url:
            return False

        # Simple URL format validation
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None

    def validate_chunk_id(self, chunk_id: str, expected_chunk_id: str) -> bool:
        """
        Validate chunk ID consistency.

        Args:
            chunk_id: Chunk ID retrieved from Qdrant
            expected_chunk_id: Expected chunk ID for comparison

        Returns:
            True if chunk ID matches expected value, False otherwise
        """
        return chunk_id == expected_chunk_id

    def validate_retrieved_chunk(
        self,
        retrieved_chunk: Dict[str, Any],
        expected_chunk: Dict[str, Any]
    ) -> ValidationResult:
        """
        Validate a single retrieved chunk against expected values.

        Args:
            retrieved_chunk: Chunk retrieved from Qdrant
            expected_chunk: Expected chunk values for comparison

        Returns:
            ValidationResult with validation status and details
        """
        # Validate content
        content_valid = self.validate_content_fidelity(
            retrieved_chunk.get("content", ""),
            expected_chunk.get("content", "")
        )

        # Validate metadata
        retrieved_metadata = {
            "url": retrieved_chunk.get("url", ""),
            "chunk_id": retrieved_chunk.get("chunk_id", "")
        }
        expected_metadata = {
            "url": expected_chunk.get("url", ""),
            "chunk_id": expected_chunk.get("chunk_id", "")
        }

        metadata_valid = self.validate_metadata_integrity(retrieved_metadata, expected_metadata)

        # Additional specific validations
        url_valid = self.validate_url_format(retrieved_chunk.get("url", ""))
        chunk_id_valid = self.validate_chunk_id(
            retrieved_chunk.get("chunk_id", ""),
            expected_chunk.get("chunk_id", "")
        )

        metadata_valid = metadata_valid and url_valid and chunk_id_valid

        # Prepare diff information if validation fails
        content_diff = None
        if not content_valid:
            content_diff = f"Content mismatch: retrieved='{retrieved_chunk.get('content', '')[:50]}...', expected='{expected_chunk.get('content', '')[:50]}...'"

        metadata_diff = None
        if not metadata_valid:
            metadata_diff = f"Metadata mismatch: retrieved={retrieved_metadata}, expected={expected_metadata}"

        return ValidationResult(
            is_content_valid=content_valid,
            is_metadata_valid=metadata_valid,
            content_diff=content_diff if not content_valid else None,
            metadata_diff=metadata_diff if not metadata_valid else None
        )

    def validate_retrieved_chunks(
        self,
        retrieved_chunks: List[Dict[str, Any]],
        expected_chunks: List[Dict[str, Any]]
    ) -> List[ValidationResult]:
        """
        Validate multiple retrieved chunks against expected values.

        Args:
            retrieved_chunks: List of chunks retrieved from Qdrant
            expected_chunks: List of expected chunk values for comparison

        Returns:
            List of ValidationResult objects for each chunk
        """
        results = []
        for i, retrieved_chunk in enumerate(retrieved_chunks):
            if i < len(expected_chunks):
                expected_chunk = expected_chunks[i]
                result = self.validate_retrieved_chunk(retrieved_chunk, expected_chunk)
                results.append(result)
            else:
                # No expected chunk for this retrieved chunk
                results.append(ValidationResult(
                    is_content_valid=False,
                    is_metadata_valid=False,
                    content_diff="No expected chunk for this retrieved chunk",
                    metadata_diff="No expected chunk for this retrieved chunk"
                ))

        return results