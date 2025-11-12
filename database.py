import os
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD')
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def init_db():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                phone VARCHAR(15),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                name VARCHAR(50) NOT NULL,
                species VARCHAR(50) NOT NULL,
                breed VARCHAR(50),
                age INT,
                weight DECIMAL(5,2),
                medical_history TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                specialization VARCHAR(100) NOT NULL,
                experience INT,
                bio TEXT,
                image VARCHAR(255),
                availability VARCHAR(100)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                price DECIMAL(10,2),
                duration INT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                doctor_id INT,
                pet_id INT,
                service_id INT,
                date DATE NOT NULL,
                time TIME NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(id),
                FOREIGN KEY (pet_id) REFERENCES pets(id),
                FOREIGN KEY (service_id) REFERENCES services(id)
            )
        ''')
        connection.commit()
        cursor.close()
        connection.close()
        print("Database initialized successfully")
