import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='project2',
            user='root',
            password='123456'
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
        
        # Create Users table
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
        
        # Create Pets table
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
        
        # Create Doctors table
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
        
        # Create Services table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                price DECIMAL(10,2),
                duration INT
            )
        ''')
        
        # Create Appointments table
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
        
        # Insert sample data
        insert_sample_data(cursor)
        
        connection.commit()
        cursor.close()
        connection.close()
        print("Database initialized successfully")

def insert_sample_data(cursor):
    # Insert sample doctors
    cursor.execute('''
        INSERT IGNORE INTO doctors (name, specialization, experience, bio, availability) VALUES
        ('Dr. Sarah Johnson', 'Veterinary Surgeon', 8, 'Specialized in orthopedic surgery and emergency care.', 'Mon, Wed, Fri'),
        ('Dr. Mike Chen', 'Dermatology', 6, 'Expert in skin conditions and allergies in pets.', 'Tue, Thu, Sat'),
        ('Dr. Emily Davis', 'Dentistry', 10, 'Focused on dental health and oral surgery for pets.', 'Mon-Fri'),
        ('Dr. Robert Wilson', 'Internal Medicine', 12, 'Specialist in chronic diseases and diagnostics.', 'Tue-Sat')
    ''')
    
    # Insert sample services
    cursor.execute('''
        INSERT IGNORE INTO services (name, description, price, duration) VALUES
        ('General Checkup', 'Comprehensive health examination', 50.00, 30),
        ('Vaccination', 'Essential vaccines for your pet', 35.00, 20),
        ('Dental Cleaning', 'Professional teeth cleaning', 120.00, 60),
        ('Surgery Consultation', 'Pre-surgical assessment', 80.00, 45),
        ('Emergency Care', 'Urgent medical attention', 150.00, 90),
        ('Grooming Service', 'Full grooming and hygiene care', 45.00, 60)
    ''')

if __name__ == "__main__":
    init_db()