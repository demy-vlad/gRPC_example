import auth_pb2
import pytest
from conftest import random_string


@pytest.mark.xfail
@pytest.mark.parametrize(
    "email",
    [
        "example.com",
        "john.doe@example",
        "@example.com",
        "john.doe@example..com",
        "john.doe@example_com",
        "john.doe@example#com",
        "john.doe@.com",
        "john.doe@examplecom",
        "john.doe@examplecom.",
        "john.doe@ex#ample.com",
        None,
        1111,
        "1111"
    ], 
)
@pytest.mark.usefixtures("connection", "cleanup_users")
def test_register_new_user(stub, email):
    """Registration of a new user"""
    stub.RegisterUser(
        auth_pb2.RegisterRequest(
        email=email,
        password=random_string(8),
        ))
    

@pytest.mark.xfail
@pytest.mark.parametrize(
    "password",
    [
        random_string(1),
        random_string(100),
        None,
        1111
    ], 
)
def test_password(stub, password):
    """Registration of a new user"""
    stub.RegisterUser(
        auth_pb2.RegisterRequest(
        email="john.doe@example.com",
        password=password,
        ))