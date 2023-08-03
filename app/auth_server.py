import time
import grpc
import auth_pb2
import auth_pb2_grpc
import sqlite3
from sqlite3 import Error
import concurrent.futures
import jwt
import datetime

DATABASE_FILE = "users.db"
SECRET_KEY = "your-secret-key"
_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def create_connection():
    """Function to create a connection to a SQLite database"""
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        return connection
    except Error as e:
        print(e)
        return None


def create_tables(connection):
    """Creating the users table if it doesn't exist"""
    create_users_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    '''
    try:
        cursor = connection.cursor()
        cursor.execute(create_users_table_query)
        connection.commit()
    except Error as e:
        print(e)


def register_user(email, password):
    """Registering a user in the database"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            connection.commit()
            connection.close()
            return True
        except Error as e:
            print(e)
    return False


def login_user(email, password):
    """User verification during authorization"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = cursor.fetchone()
            connection.close()
            if user is not None:
                return True
        except Error as e:
            print(e)
    return False


def generate_access_token():
    """Generate access token using JWT"""
    payload = {"exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
    access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return access_token


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def RegisterUser(self, request, context):
        """Implementing a gRPC service"""
        email = request.email
        password = request.password

        if register_user(email, password):
            response = auth_pb2.RegisterResponse(message="User successfully registered!")
        else:
            response = auth_pb2.RegisterResponse(message="User with this email already registered!")

        return response

    def LoginUser(self, request, context):
        email = request.email
        password = request.password

        if login_user(email, password):
            access_token = generate_access_token()
            response = auth_pb2.LoginResponse(message="User logged in successfully!", access_token=access_token)
        else:
            response = auth_pb2.LoginResponse(message="User not found or incorrect password.")

        return response


def serve():
    """Starting the gRPC server"""
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started. Listening on port 50051.")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    create_tables(create_connection())
    serve()