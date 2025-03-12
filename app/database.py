import os
import time
import logging
import mysql.connector

from typing import Optional
from dotenv import load_dotenv
from mysql.connector import Error

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseConnectionError(Exception):
    """Custom exception for database connection failures"""

    pass


def get_db_connection(
    max_retries: int = 12,  # 12 retries = 1 minute total (12 * 5 seconds)
    retry_delay: int = 5,  # 5 seconds between retries
) -> mysql.connector.MySQLConnection:
    """Create database connection with retry mechanism."""
    connection: Optional[mysql.connector.MySQLConnection] = None
    attempt = 1
    last_error = None

    while attempt <= max_retries:
        try:
            connection = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DATABASE"),
            )

            # Test the connection
            connection.ping(reconnect=True, attempts=1, delay=0)
            logger.info("Database connection established successfully")
            return connection

        except Error as err:
            last_error = err
            logger.warning(
                f"Connection attempt {attempt}/{max_retries} failed: {err}. "
                f"Retrying in {retry_delay} seconds..."
            )

            if connection is not None:
                try:
                    connection.close()
                except Exception:
                    pass

            if attempt == max_retries:
                break

            time.sleep(retry_delay)
            attempt += 1

    raise DatabaseConnectionError(
        f"Failed to connect to database after {max_retries} attempts. "
        f"Last error: {last_error}"
    )


async def setup_database(initial_users: dict = None):
    """Creates user and session tables and populates initial user data if provided."""
    connection = None
    cursor = None

    # Define table schemas
    table_schemas = {
        "users": """
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                firstName VARCHAR(100),
                lastName VARCHAR(100),
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        "sessions": """
            CREATE TABLE sessions (
                id VARCHAR(36) PRIMARY KEY,
                user_id INT NOT NULL,
                device_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """,
        "devices": """
            CREATE TABLE devices (
                id VARCHAR(36) PRIMARY KEY,
                user_id INT NOT NULL,
                topic VARCHAR(50),
                status VARCHAR(50),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """,
        "wardrobe": """
            CREATE TABLE wardrobe (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                name VARCHAR(100),
                category VARCHAR(100),
                color VARCHAR(100),
                size VARCHAR(100),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
        """,
        "sensorData": """
            CREATE TABLE sensorData (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                device_id VARCHAR(36) NOT NULL,
                sensor_type VARCHAR(100),
                value FLOAT,
                curr_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
                )
        """,
    }

    try:
        # Get database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Drop and recreate tables one by one
        for table_name in ["sensorData", "wardrobe", "devices", "sessions", "users"]:
            # Drop table if exists
            logger.info(f"Dropping table {table_name} if exists...")
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            connection.commit()

        # Recreate tables one by one
        for table_name, create_query in table_schemas.items():

            try:
                # Create table
                logger.info(f"Creating table {table_name}...")
                cursor.execute(create_query)
                connection.commit()
                logger.info(f"Table {table_name} created successfully")

            except Error as e:
                logger.error(f"Error creating table {table_name}: {e}")
                raise

        # Insert initial users if provided
        if initial_users:
            try:
                insert_query = "INSERT INTO users (email, password) VALUES (%s, %s)"
                for username, password in initial_users.items():
                    cursor.execute(insert_query, (username, password))
                connection.commit()
                logger.info(f"Inserted {len(initial_users)} initial users")
            except Error as e:
                logger.error(f"Error inserting initial users: {e}")
                raise

    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        raise

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            logger.info("Database connection closed")

####### USERS ##########

# Database utility functions for user and session management
async def get_user_by_username(username: str) -> Optional[dict]:
    """Retrieve user from database by username."""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (username,))
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

async def get_all_users():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        return users
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


async def get_user_by_id(user_id: int) -> Optional[dict]:
    """
    Retrieve user from database by ID.

    Args:
        user_id: The ID of the user to retrieve

    Returns:
        Optional[dict]: User data if found, None otherwise
    """
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

async def get_id_by_user(username: str) -> Optional[dict]:
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (username,))
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


async def create_user(firstName: str, lastName: str, email: str, password: str):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (email, firstName, lastName, password) VALUES (%s, %s, %s, %s)", (email, firstName, lastName, password) 
        )
        connection.commit()
        return True
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

######## SESSIONS ########

async def create_session(user_id: int, session_id: str) -> bool:
    """Create a new session in the database."""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO sessions (id, user_id) VALUES (%s, %s)", (session_id, user_id)
        )
        connection.commit()
        return True
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


async def get_session(session_id: str) -> Optional[dict]:
    """Retrieve session from database."""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT *
            FROM sessions s
            WHERE s.id = %s
        """,
            (session_id,),
        )
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


async def delete_session(session_id: str) -> bool:
    """Delete a session from the database."""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM sessions WHERE id = %s", (session_id,))
        connection.commit()
        return True
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


####### DEVICES ############

async def get_user_devices(user_id: int):
    """Fetch all devices for a specific user from the database."""
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM devices WHERE user_id = %s", (user_id,))
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

async def get_device(id: str, user_id: int):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM devices WHERE id = %s AND user_id = %s", (id, user_id,))
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

async def add_user_device(id: str, user_id: int, topic: str, status: str):
    """Insert a new device into the database."""
    connection = None
    cursor = None

    unique_id = id + str(user_id)

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO devices (id, user_id, topic, status) VALUES (%s, %s, %s, %s)",
            (unique_id, user_id, topic, status)
        )
        connection.commit()
        return True
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

async def delete_user_device(id: str, user_id: int):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM devices WHERE id = %s AND user_id = %s", (id, user_id,))
        connection.commit()
        return True
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

async def get_devices():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM devices")
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

######## WARDROBE  ##############
async def get_wardrobe():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM wardrobe")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


async def get_user_wardrobe(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM wardrobe WHERE user_id = %s", (user_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

async def add_wardrobe_item(user_id: int, name: str, category: str, size: str):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO wardrobe (user_id, name, category, size) VALUES (%s, %s, %s, %s)", (user_id, name, category, size))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

async def remove_wardrobe_item(user_id: int, name: str):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM wardrobe WHERE user_id = %s AND LOWER(name) = LOWER(%s)", (user_id, name,))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

async def update_wardrobe_item(user_id: int, old_name: str, new_name: str):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE wardrobe SET name = %s WHERE user_id = %s AND name = %s", (new_name, user_id, old_name))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

###### DASHBOARD ##########



#### SENSOR DATA ######
async def get_all_data():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM sensorData")
        sensorData = cursor.fetchall()

        return sensorData
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


async def get_user_sensor_data(user_id: int):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM sensorData WHERE user_id = %s", (user_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

async def add_user_sensor_data(user_id: int, device_id: str, value: float):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO sensorData (device_id, value) VALUES (%s, %s)", (device_id, value))
        connection.commit()
    finally:
        cursor.close()
        connection.close()