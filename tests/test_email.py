import pytest
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
@patch("smtplib.SMTP")
async def test_send_markdown_email(mock_smtp, email_service):
    # Mock the context manager behavior
    mock_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_instance

    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }

    await email_service.send_user_email(user_data, 'email_verification')

    # Optional assertion
    mock_instance.sendmail.assert_called()