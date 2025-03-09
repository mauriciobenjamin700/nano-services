from pydantic import field_validator
from re import match

from src.pydantic_helper.validators.base import ValidationError

ERROR_EMAIL_INVALID_FORMAT_TYPE = "Email must be a string"
ERROR_EMAIL_INVALID_FORMAT_MASK = "Email must have a valid format"

ERROR_PASSWORD_INVALID_FORMAT_TYPE = "Password must be a string"
ERROR_PASSWORD_INVALID_FORMAT_MIN_LENGTH = "Password must have at least 8 characters"
ERROR_PASSWORD_INVALID_FORMAT_MAX_LENGTH = "Password must have at most 255 characters"
ERROR_PASSWORD_INVALID_FORMAT_DIGIT = "Password must have at least one digit"
ERROR_PASSWORD_INVALID_FORMAT_LOWERCASE = "Password must have at least one lowercase letter"
ERROR_PASSWORD_INVALID_FORMAT_UPPERCASE = "Password must have at least one uppercase letter"
ERROR_PASSWORD_INVALID_FORMAT_SPECIAL_CHARACTER = "Password must have at least one special character"


ERROR_IS_ADMIN_INVALID_FORMAT_TYPE = "Is Admin must be a boolean"
ERROR_NAME_INVALID_FORMAT_TYPE = "Name must be a string"
ERROR_NAME_INVALID_FORMAT_MIN_LENGTH = "Name must be at least 2 characters"
ERROR_PHONE_INVALID_FORMAT_TYPE = "Phone must be a string"
ERROR_PHONE_INVALID_FORMAT_LENGTH = "Phone must be at least 11 characters"
ERROR_USERNAME_INVALID_FORMAT_TYPE = "Username must be a string"
ERROR_USERNAME_INVALID_FORMAT_MIN_LENGTH = "Username must be at least 2 characters with no spaces"

@field_validator("email", mode="before")
def validate_email(cls, value: str) -> str:
    """
    A function that validates the email field.

    - Args:
        - cls: The class instance.
        - value: The email value.
    - Returns:
        - str: The email value.
    """
    if not isinstance(value, str):
        raise ValidationError(field="email", detail=ERROR_EMAIL_INVALID_FORMAT_TYPE)
    
    value = value.strip()
    
    if not match(r"[^@]+@[^@]+\.[^@]+", value):
        raise ValidationError(field="email", detail=ERROR_EMAIL_INVALID_FORMAT_MASK)
    
    return value

@field_validator("is_admin", mode="before")
def validate_is_admin(cls, value: bool) -> bool:
    """
    A function that validates the is_admin field.

    - Args:
        - cls: The class instance.
        - value: The is_admin value.
    - Returns:
        - bool: The is_admin value.
    """
    if not isinstance(value, bool):
        raise ValidationError(field="is_admin", detail=ERROR_IS_ADMIN_INVALID_FORMAT_TYPE)
    return value

@field_validator("name", mode="before")
def validate_name(cls, value: str) -> str:
    """
    A function that validates the name field.

    - Args:
        - cls: The class instance.
        - value: The name value.
    - Returns:
        - str: The name value.
    """
    if not isinstance(value, str):
        raise ValidationError(field="name", detail=ERROR_NAME_INVALID_FORMAT_TYPE)
    
    value = value.strip()
    
    if len(value) <= 1:
        raise ValidationError(field="name", detail=ERROR_NAME_INVALID_FORMAT_MIN_LENGTH)
    
    value = value.upper()
    
    return value

@field_validator("password", mode="before")
def validate_password(cls, value: str) -> str:
    """
    A function that validates the password field.

    - Args:
        - cls: The class instance.
        - value: The password value.
    - Returns:
        - str: The password value.
    """
    if not isinstance(value, str):
        raise ValidationError(field="password", detail=ERROR_PASSWORD_INVALID_FORMAT_TYPE)
    
    value = value.strip()
    
    if len(value) < 8:
        raise ValidationError(field="password", detail=ERROR_PASSWORD_INVALID_FORMAT_MIN_LENGTH)
    
    if len(value) > 255:
        raise ValidationError(field="password", detail=ERROR_PASSWORD_INVALID_FORMAT_MAX_LENGTH)
    
    if not any(char.isdigit() for char in value):
        raise ValidationError(field="password", detail=ERROR_PASSWORD_INVALID_FORMAT_DIGIT)
    
    if not any(char.islower() for char in value):
        raise ValidationError(field="password", detail=ERROR_PASSWORD_INVALID_FORMAT_LOWERCASE)
    
    if not any(char.isupper() for char in value):
        raise ValidationError(field="password", detail=ERROR_PASSWORD_INVALID_FORMAT_UPPERCASE)
    
    if not any(char in "!@#$%&*()_+-=[]{};:,.<>?/" for char in value):
        raise ValidationError(field="password", detail=ERROR_PASSWORD_INVALID_FORMAT_SPECIAL_CHARACTER)
    
    return value

@field_validator("phone", mode="before")
def validate_phone(cls, value: str) -> str:
    """
    A function that validates the phone field.

    - Args:
        - cls: The class instance.
        - value: The phone value.
    - Returns:
        - str: The phone value.
    """
    if not isinstance(value, str):
        raise ValidationError(field="phone", detail=ERROR_PHONE_INVALID_FORMAT_TYPE)
    
    value = value.strip()
    
    value = "".join([char for char in value if char.isdigit()])
    
    if len(value) < 11:
        raise ValidationError(field="phone", detail=ERROR_PHONE_INVALID_FORMAT_LENGTH)
    
    return value


@field_validator("username", mode="before")
def validate_username(cls, value: str) -> str:
    """
    A function that validates the username field.

    - Args:
        - cls: The class instance.
        - value: The username value.
    - Returns:
        - str: The username value.
    """
    if not isinstance(value, str):
        raise ValidationError(field="username", detail=ERROR_USERNAME_INVALID_FORMAT_TYPE)
    
    value = value.strip()
    
    if len(value) <= 1:
        raise ValidationError(field="username", detail=ERROR_USERNAME_INVALID_FORMAT_MIN_LENGTH)
    
    return value