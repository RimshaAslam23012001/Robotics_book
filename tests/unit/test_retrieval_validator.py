import pytest
from src.rag_retrieval.retrieval_validator import RetrievalValidator, ValidationResult


class TestRetrievalValidator:
    """Unit tests for RetrievalValidator."""

    @pytest.fixture
    def validator(self):
        """Create a RetrievalValidator instance for testing."""
        return RetrievalValidator()

    def test_validate_content_fidelity_matching(self, validator):
        """Test content validation when content matches exactly."""
        # Arrange
        retrieved_content = "This is the exact same content."
        original_content = "This is the exact same content."

        # Act
        result = validator.validate_content_fidelity(retrieved_content, original_content)

        # Assert
        assert result is True

    def test_validate_content_fidelity_not_matching(self, validator):
        """Test content validation when content does not match."""
        # Arrange
        retrieved_content = "This is different content."
        original_content = "This is the original content."

        # Act
        result = validator.validate_content_fidelity(retrieved_content, original_content)

        # Assert
        assert result is False

    def test_validate_content_fidelity_different_case(self, validator):
        """Test content validation when content differs by case."""
        # Arrange
        retrieved_content = "This is the same content."
        original_content = "THIS IS THE SAME CONTENT."

        # Act
        result = validator.validate_content_fidelity(retrieved_content, original_content)

        # Assert
        assert result is False

    def test_validate_metadata_integrity_matching(self, validator):
        """Test metadata validation when metadata matches."""
        # Arrange
        retrieved_metadata = {"url": "http://example.com", "chunk_id": "123"}
        expected_metadata = {"url": "http://example.com", "chunk_id": "123"}

        # Act
        result = validator.validate_metadata_integrity(retrieved_metadata, expected_metadata)

        # Assert
        assert result is True

    def test_validate_metadata_integrity_extra_retrieved(self, validator):
        """Test metadata validation when retrieved has extra fields."""
        # Arrange
        retrieved_metadata = {"url": "http://example.com", "chunk_id": "123", "extra": "value"}
        expected_metadata = {"url": "http://example.com", "chunk_id": "123"}

        # Act
        result = validator.validate_metadata_integrity(retrieved_metadata, expected_metadata)

        # Assert
        assert result is True

    def test_validate_metadata_integrity_missing_retrieved(self, validator):
        """Test metadata validation when retrieved is missing expected field."""
        # Arrange
        retrieved_metadata = {"url": "http://example.com"}  # Missing chunk_id
        expected_metadata = {"url": "http://example.com", "chunk_id": "123"}

        # Act
        result = validator.validate_metadata_integrity(retrieved_metadata, expected_metadata)

        # Assert
        assert result is False

    def test_validate_metadata_integrity_different_value(self, validator):
        """Test metadata validation when metadata has different values."""
        # Arrange
        retrieved_metadata = {"url": "http://example.com", "chunk_id": "123"}
        expected_metadata = {"url": "http://example.com", "chunk_id": "456"}

        # Act
        result = validator.validate_metadata_integrity(retrieved_metadata, expected_metadata)

        # Assert
        assert result is False

    def test_validate_url_format_valid_http(self, validator):
        """Test URL validation with valid HTTP URL."""
        # Arrange
        url = "http://example.com"

        # Act
        result = validator.validate_url_format(url)

        # Assert
        assert result is True

    def test_validate_url_format_valid_https(self, validator):
        """Test URL validation with valid HTTPS URL."""
        # Arrange
        url = "https://example.com/path/to/resource"

        # Act
        result = validator.validate_url_format(url)

        # Assert
        assert result is True

    def test_validate_url_format_invalid(self, validator):
        """Test URL validation with invalid URL."""
        # Arrange
        url = "not-a-url"

        # Act
        result = validator.validate_url_format(url)

        # Assert
        assert result is False

    def test_validate_url_format_empty(self, validator):
        """Test URL validation with empty string."""
        # Arrange
        url = ""

        # Act
        result = validator.validate_url_format(url)

        # Assert
        assert result is False

    def test_validate_chunk_id_matching(self, validator):
        """Test chunk ID validation when IDs match."""
        # Arrange
        chunk_id = "test_chunk_123"
        expected_chunk_id = "test_chunk_123"

        # Act
        result = validator.validate_chunk_id(chunk_id, expected_chunk_id)

        # Assert
        assert result is True

    def test_validate_chunk_id_not_matching(self, validator):
        """Test chunk ID validation when IDs don't match."""
        # Arrange
        chunk_id = "test_chunk_123"
        expected_chunk_id = "different_chunk_456"

        # Act
        result = validator.validate_chunk_id(chunk_id, expected_chunk_id)

        # Assert
        assert result is False

    def test_validate_retrieved_chunk_valid(self, validator):
        """Test validation of a correctly retrieved chunk."""
        # Arrange
        retrieved_chunk = {
            "content": "This is the content",
            "url": "https://example.com",
            "chunk_id": "123"
        }
        expected_chunk = {
            "content": "This is the content",
            "url": "https://example.com",
            "chunk_id": "123"
        }

        # Act
        result = validator.validate_retrieved_chunk(retrieved_chunk, expected_chunk)

        # Assert
        assert result.is_content_valid is True
        assert result.is_metadata_valid is True
        assert result.content_diff is None
        assert result.metadata_diff is None

    def test_validate_retrieved_chunk_invalid_content(self, validator):
        """Test validation of a chunk with invalid content."""
        # Arrange
        retrieved_chunk = {
            "content": "Different content",
            "url": "https://example.com",
            "chunk_id": "123"
        }
        expected_chunk = {
            "content": "Expected content",
            "url": "https://example.com",
            "chunk_id": "123"
        }

        # Act
        result = validator.validate_retrieved_chunk(retrieved_chunk, expected_chunk)

        # Assert
        assert result.is_content_valid is False
        assert result.is_metadata_valid is True  # URL and chunk_id are valid
        assert result.content_diff is not None
        assert result.metadata_diff is None

    def test_validate_retrieved_chunk_invalid_metadata(self, validator):
        """Test validation of a chunk with invalid metadata."""
        # Arrange
        retrieved_chunk = {
            "content": "Expected content",
            "url": "invalid-url",
            "chunk_id": "123"
        }
        expected_chunk = {
            "content": "Expected content",
            "url": "https://example.com",  # Different URL
            "chunk_id": "123"
        }

        # Act
        result = validator.validate_retrieved_chunk(retrieved_chunk, expected_chunk)

        # Assert
        assert result.is_content_valid is True
        assert result.is_metadata_valid is False
        assert result.content_diff is None
        assert result.metadata_diff is not None