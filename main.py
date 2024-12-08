import sqlite3

conn = sqlite3.connect("pawsome_pets.db")
cursor = conn.cursor()

# Drop schema 
def drop_schema():
    cursor.executescript("""
    DROP TABLE IF EXISTS Examination;
    DROP TABLE IF EXISTS Pet;
    DROP TABLE IF EXISTS Owner;
    DROP TABLE IF EXISTS Staff;
    DROP TABLE IF EXISTS Clinic;
    """)
    conn.commit()
    print("Database schema dropped successfully!")

#Database schema
def create_schema():
    cursor.executescript("""
    -- Clinic Table
    CREATE TABLE IF NOT EXISTS Clinic (
        clinicNo INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address_street TEXT NOT NULL,
        address_city TEXT NOT NULL,
        address_zip TEXT NOT NULL,
        telephone TEXT UNIQUE NOT NULL CHECK (LENGTH(telephone) = 10 AND telephone GLOB '[0-9]*'),
        managerNo INTEGER UNIQUE,
        FOREIGN KEY (managerNo) REFERENCES Staff(staffNo) ON DELETE SET NULL
    );

    -- Staff Table
    CREATE TABLE IF NOT EXISTS Staff (
        staffNo INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address_street TEXT NOT NULL,
        address_city TEXT NOT NULL,
        address_zip TEXT NOT NULL,
        telephone TEXT UNIQUE NOT NULL CHECK (LENGTH(telephone) = 10 AND telephone GLOB '[0-9]*'),
        dob TEXT NOT NULL,
        position TEXT NOT NULL,
        salary REAL NOT NULL CHECK (salary >= 0),
        clinicNo INTEGER,
        FOREIGN KEY (clinicNo) REFERENCES Clinic(clinicNo) ON DELETE CASCADE
    );

    -- Owner Table
    CREATE TABLE IF NOT EXISTS Owner (
        ownerNo INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address_street TEXT NOT NULL,
        address_city TEXT NOT NULL,
        address_zip TEXT NOT NULL,
        telephone TEXT UNIQUE NOT NULL CHECK (LENGTH(telephone) = 10 AND telephone GLOB '[0-9]*')
    );

    -- Pet Table
    CREATE TABLE IF NOT EXISTS Pet (
        petNo INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        dob TEXT NOT NULL,
        species TEXT CHECK(species IN ('Dog', 'Cat', 'Bird')) NOT NULL,
        breed TEXT NOT NULL,
        color TEXT NOT NULL,
        ownerNo INTEGER NOT NULL,
        clinicNo INTEGER NOT NULL,
        FOREIGN KEY (ownerNo) REFERENCES Owner(ownerNo) ON DELETE CASCADE,
        FOREIGN KEY (clinicNo) REFERENCES Clinic(clinicNo) ON DELETE CASCADE
    );

    -- Examination Table
    CREATE TABLE IF NOT EXISTS Examination (
        examNo INTEGER PRIMARY KEY AUTOINCREMENT,
        chiefComplaint TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        actionsTaken TEXT,
        petNo INTEGER NOT NULL,
        staffNo INTEGER NOT NULL,
        FOREIGN KEY (petNo) REFERENCES Pet(petNo) ON DELETE CASCADE,
        FOREIGN KEY (staffNo) REFERENCES Staff(staffNo) ON DELETE SET NULL
    );
    """)
    conn.commit()
    print("Database schema created successfully!")

#Sample data
def insert_sample_data():
    try:
        
        clinic_data = [
            ("Downtown Vet", "123 Main St", "Metropolis", "12345", "5551234567", 1),
            ("Uptown Vet", "456 Maple Ave", "Gotham", "67890", "5552345678", 2),
            ("Suburb Vet", "789 Elm Dr", "Smallville", "54321", "5553456789", 3),
            ("Eastside Vet", "321 Oak Blvd", "Star City", "98765", "5554567890", 4),
            ("Westside Vet", "654 Pine Ln", "Central City", "87654", "5555678901", None)
        ]
        cursor.executemany("INSERT INTO Clinic (name, address_street, address_city, address_zip, telephone, managerNo) VALUES (?, ?, ?, ?, ?, ?)", clinic_data)
        print("Clinic data inserted successfully.")

        staff_data = [
            ("Dr. Smith", "456 Elm St", "Metropolis", "12345", "5559876543", "1980-05-12", "Veterinarian", 85000, 1),
            ("Dr. Jones", "789 Oak St", "Gotham", "67890", "5556549876", "1975-10-22", "Veterinarian", 90000, 2),
            ("Nurse Mary", "123 Pine St", "Metropolis", "12345", "5553216549", "1990-03-15", "Nurse", 50000, 1),
            ("Nurse Luke", "567 Birch Rd", "Smallville", "54321", "5554561230", "1985-06-18", "Nurse", 55000, 3),
            ("Dr. Lee", "234 Aspen St", "Star City", "98765", "5557891234", "1982-11-30", "Veterinarian", 87000, 4)
        ]
        cursor.executemany("INSERT INTO Staff (name, address_street, address_city, address_zip, telephone, dob, position, salary, clinicNo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", staff_data)
        print("Staff data inserted successfully.")

        owner_data = [
            ("John Doe", "789 Oak St", "Metropolis", "12345", "5554567890"),
            ("Jane Smith", "234 Pine St", "Gotham", "67890", "5556781234"),
            ("Clark Kent", "567 Birch Rd", "Smallville", "54321", "5559873210"),
            ("Bruce Wayne", "123 Wayne Manor", "Gotham", "67890", "5556543210"),
            ("Diana Prince", "456 Amazon St", "Themyscira", "12345", "5558765432")
        ]
        cursor.executemany("INSERT INTO Owner (name, address_street, address_city, address_zip, telephone) VALUES (?, ?, ?, ?, ?)", owner_data)
        print("Owner data inserted successfully.")

        pet_data = [
            ("Buddy", "2020-03-01", "Dog", "Labrador", "Yellow", 1, 1),
            ("Mittens", "2021-07-15", "Cat", "Siamese", "Gray", 2, 2),
            ("Max", "2018-11-23", "Dog", "Beagle", "Brown", 3, 3),
            ("Bella", "2019-08-09", "Dog", "Poodle", "White", 4, 4),
            ("Whiskers", "2022-02-14", "Cat", "Tabby", "Orange", 5, 5)
        ]
        cursor.executemany("INSERT INTO Pet (name, dob, species, breed, color, ownerNo, clinicNo) VALUES (?, ?, ?, ?, ?, ?, ?)", pet_data)
        print("Pet data inserted successfully.")

        examination_data = [
            ("Limping", "Examined leg, X-rays taken", "2024-12-06", "Prescribed rest", 1, 1),
            ("Coughing", "Checked lungs, prescribed antibiotics", "2024-12-06", "Antibiotics", 2, 2),
            ("Itchy skin", "Skin scrape test performed", "2024-12-05", "Special shampoo", 3, 3),
            ("Diarrhea", "Prescribed probiotics", "2024-12-04", "Probiotics", 4, 4),
            ("Ear infection", "Cleaned ears, prescribed drops", "2024-12-03", "Ear drops", 5, 5)
        ]
        cursor.executemany("INSERT INTO Examination (chiefComplaint, description, date, actionsTaken, petNo, staffNo) VALUES (?, ?, ?, ?, ?, ?)", examination_data)
        print("Examination data inserted successfully.")

        conn.commit()
    except sqlite3.IntegrityError as e:
        print("Error during data insertion:", e)

def main():
    drop_schema()
    create_schema()
    insert_sample_data()

if __name__ == "__main__":
    main()
