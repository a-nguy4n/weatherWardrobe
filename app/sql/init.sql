-- Create users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100)
);

-- CREATE sensorData table
CREATE TABLE IF NOT EXISTS sensorData (
    data_id INT PRIMARY KEY,
    user_id INT,
    sensor_type VARCHAR(50) NOT NULL,
    data_value float,
    curr_time timestamp,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

-- CREATE devices table 
CREATE TABLE IF NOT EXISTS devices (
    device_id INT PRIMARY KEY,
    user_id INT,
    topic VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

-- CREATE sessions table
CREATE TABLE IF NOT EXISTS sessions (
    session_id INT PRIMARY KEY,
    user_id INT,
    device_id INT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
    FOREIGN KEY(device_id) REFERENCES devices(device_id)
);