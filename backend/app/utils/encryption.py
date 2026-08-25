"""Encryption utilities for secure token storage."""

from cryptography.fernet import Fernet
from app.config import get_settings
import base64
import logging

logger = logging.getLogger(__name__)

settings = get_settings()

# Initialize cipher
try:
    # Ensure encryption key is 32 bytes for Fernet
    key = settings.encryption_key
    if isinstance(key, str):
        # Pad or truncate to 32 bytes
        key = key.ljust(32)[:32]
        key = base64.urlsafe_b64encode(key.encode())
    cipher = Fernet(key)
except Exception as e:
    logger.warning(f"Failed to initialize encryption: {e}. Using fallback.")
    cipher = None


def encrypt_token(token: str) -> str:
    """Encrypt a token."""
    if not cipher:
        return token
    try:
        encrypted = cipher.encrypt(token.encode())
        return encrypted.decode()
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        return token


def decrypt_token(encrypted_token: str) -> str:
    """Decrypt a token."""
    if not cipher:
        return encrypted_token
    try:
        decrypted = cipher.decrypt(encrypted_token.encode())
        return decrypted.decode()
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        return encrypted_token
