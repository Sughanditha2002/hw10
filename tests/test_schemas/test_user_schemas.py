import pytest
from pydantic import ValidationError
from uuid import uuid4
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, LoginRequest, UserListResponse
from app.schemas.user_schemas import UserRole

# ✅ Base valid data for reuse
base_valid_data = {
    "email": "test@example.com",
    "nickname": "valid_user",
    "first_name": "Test",
    "last_name": "User",
    "bio": "Just testing.",
    "profile_picture_url": "https://example.com/pic.jpg",
    "linkedin_profile_url": "https://linkedin.com/in/testuser",
    "github_profile_url": "https://github.com/testuser"
}

def test_user_base_valid():
    user = UserBase(**base_valid_data)
    assert user.email == base_valid_data["email"]
    assert user.nickname == base_valid_data["nickname"]

def test_user_base_invalid_email():
    data = base_valid_data.copy()
    data["email"] = "invalid-email"
    with pytest.raises(ValidationError):
        UserBase(**data)

@pytest.mark.parametrize("nickname", ["valid_user", "user123", "u_nder-score"])
def test_nickname_valid(nickname):
    data = base_valid_data.copy()
    data["nickname"] = nickname
    user = UserBase(**data)
    assert user.nickname == nickname

@pytest.mark.parametrize("nickname", ["invalid user", "no$", "", "12"])
def test_nickname_invalid(nickname):
    data = base_valid_data.copy()
    data["nickname"] = nickname
    with pytest.raises(ValidationError):
        UserBase(**data)

@pytest.mark.parametrize("url", ["http://valid.com", "https://site.org", None])
def test_url_valid(url):
    data = base_valid_data.copy()
    data["profile_picture_url"] = url
    user = UserBase(**data)
    assert user.profile_picture_url == url

@pytest.mark.parametrize("url", ["ftp://bad.com", "https//missingcolon.com", "invalid"])
def test_url_invalid(url):
    data = base_valid_data.copy()
    data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**data)

def test_user_create_valid():
    data = base_valid_data.copy()
    data["password"] = "StrongP@ss123"
    user = UserCreate(**data)
    assert user.password == data["password"]

def test_user_update_requires_one_field():
    with pytest.raises(ValidationError):
        UserUpdate()

def test_login_request_valid():
    login = LoginRequest(email="user@example.com", password="123456")
    assert login.email == "user@example.com"
    assert login.password == "123456"

def test_user_response_valid():
    data = base_valid_data.copy()
    data.update({
        "id": uuid4(),
        "role": UserRole.AUTHENTICATED,
        "is_professional": True
    })
    user = UserResponse(**data)
    assert user.email == data["email"]
    assert user.role == UserRole.AUTHENTICATED

def test_user_list_response_valid():
    item = {
        **base_valid_data,
        "id": uuid4(),
        "role": UserRole.AUTHENTICATED,
        "is_professional": False
    }
    response = UserListResponse(
        items=[UserResponse(**item)],
        total=1,
        page=1,
        size=10
    )
    assert response.total == 1
    assert isinstance(response.items[0], UserResponse)