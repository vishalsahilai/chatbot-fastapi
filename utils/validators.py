from fastapi import HTTPException

MAX_MESSAGE_LENGTH = 2000

def validate_message(message: str) -> str:
    """
    Validates and sanitizes the incoming user message.
 
    Raises:
        HTTPException 400 — if message is empty or too long.
 
    Returns:
        Stripped, validated message string.
    """
    if not message or not message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
 
    message = message.strip()
 
    if len(message) > MAX_MESSAGE_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Message too long. Maximum {MAX_MESSAGE_LENGTH} characters allowed.",
        )
 
    return message