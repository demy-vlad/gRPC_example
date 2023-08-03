import auth_pb2
import pytest
from conftest import random_string


@pytest.mark.parametrize(
    "expected_email",
    [
        "john.doe@example.com",
        "john.doe+tag@example.com",
        "john.doe@sub.example.com",
        "email@example.com",
        "firstname.lastname@example.com",
        "firstname+lastname@example.com",
        "_______@example.com",
        "1234567890@example.com",
    ], 
)
@pytest.mark.usefixtures("connection", "cleanup_users")
def test_register_new_user(stub, expected_email):
    """Registration of a new user"""
    register_response = stub.RegisterUser(
        auth_pb2.RegisterRequest(
        email=expected_email,
        password=random_string(8),
        ))
    assert "User successfully registered!" == register_response.message


@pytest.mark.parametrize(
        "email, password",
        [
            ("test@example.com", "123456")
        ],
)
def test_authorization(stub, email, password):
    """Authorization testing"""
    # Add test user if not already added
    stub.RegisterUser(
        auth_pb2.RegisterRequest(
        email=email,
        password=password,
        ))
    # login
    login_response = stub.LoginUser(
        auth_pb2.LoginRequest(
        email=email,
        password=password,
        ))
    assert "User logged in successfully!" == login_response.message
    assert login_response.access_token != None


@pytest.mark.parametrize(
        "email, password",
        [
            ("test@example.com", "123456")
        ],
)
def test_register_existing_user(stub, email, password):
    """Attempt to register an existing user"""
    response = stub.RegisterUser(auth_pb2.RegisterRequest(
        email=email,
        password=password,
        ))
    assert "already registered" in response.message.lower()


def test_login_nonexistent_user(stub):
    """Attempt to authorize a non-existent user"""
    response = stub.LoginUser(auth_pb2.LoginRequest(
        email="nonexistent@example.com",
        password="password"
        ))
    assert "user not found" in response.message.lower()

 
def test_login_with_incorrect_password(stub):
    """Attempt to login with wrong password"""
    response = stub.LoginUser(auth_pb2.RegisterRequest(
        email="test@example.com",
        password=random_string(8)
        ))
    assert "incorrect password" in response.message.lower()