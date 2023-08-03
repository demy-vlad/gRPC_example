import secrets
import sqlite3
import string
import grpc
import pytest
import auth_pb2_grpc
from sqlite3 import Error



DATABASE_FILE = "app/users.db"

def create_connection():
    """Function to create a connection to a SQLite database"""
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        return connection
    except Error as e:
        print(e)
        return None


@pytest.fixture(scope='session', autouse=True)
def grpc_channel():
    channel = grpc.insecure_channel('localhost:50051')
    yield channel
    channel.close()


@pytest.fixture(scope='session')
def stub(grpc_channel):
    return auth_pb2_grpc.AuthServiceStub(grpc_channel)


@pytest.fixture(scope='session')
def connection():
    """Create connection database"""
    connection = create_connection()
    yield connection
    connection.close()


@pytest.fixture(scope='session')
def cleanup_users(connection):
    """Delete all users after each test"""
    yield
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users")
    connection.commit()


def random_string(number):
    """Generate random string"""
    return ''.join(secrets.choice(
        string.ascii_lowercase
        ) for _ in range(number))