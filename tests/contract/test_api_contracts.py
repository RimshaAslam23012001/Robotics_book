import pytest
from src.config.settings import Settings


class TestAPIContracts:
    """Contract tests for API compatibility."""

    def test_settings_have_required_fields(self):
        """Test that settings class has all required configuration fields."""
        settings = Settings()

        # Check that required attributes exist
        assert hasattr(settings, 'COHERE_API_KEY')
        assert hasattr(settings, 'QDRANT_URL')
        assert hasattr(settings, 'QDRANT_API_KEY')
        assert hasattr(settings, 'QDRANT_COLLECTION_NAME')
        assert hasattr(settings, 'DEFAULT_TOP_K')
        assert hasattr(settings, 'MIN_SCORE_THRESHOLD')

    def test_settings_validation_method_exists(self):
        """Test that settings validation method exists and is callable."""
        settings = Settings()

        assert hasattr(settings, 'validate')
        assert callable(getattr(settings, 'validate'))

    def test_settings_required_settings_method_exists(self):
        """Test that required settings method exists and is callable."""
        settings = Settings()

        assert hasattr(settings, 'get_required_settings')
        assert callable(getattr(settings, 'get_required_settings'))

    def test_settings_required_settings_list(self):
        """Test that required settings list contains expected values."""
        settings = Settings()
        required_settings = settings.get_required_settings()

        expected_settings = ["COHERE_API_KEY", "QDRANT_URL", "QDRANT_COLLECTION_NAME"]
        for expected in expected_settings:
            assert expected in required_settings