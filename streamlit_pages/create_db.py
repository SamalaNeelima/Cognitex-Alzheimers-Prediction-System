import mysql.connector

# ✅ Connect to MySQL Server (Change credentials if needed)
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",       # 👉 Replace with your MySQL username
        password="root"    # 👉 Replace with your MySQL password
    )
    mycursor = mydb.cursor()

    # ✅ Create Database if it doesn't exist
    mycursor.execute("CREATE DATABASE IF NOT EXISTS Alzheimers_1")
    print("✅ Database 'Alzheimers_1' created successfully (if not already existing).")

    # ✅ Connect to the new database
    mydb.database = "Alzheimers_1"

    # ✅ Create 'patients' table
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS predicts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            gender VARCHAR(10) NOT NULL,
            contact VARCHAR(20) NOT NULL UNIQUE,
            condition VARCHAR(255) NOT NULL,
            image LONGBLOB
        )
    """)
    print("✅ Table 'patients' created successfully.")

    # ✅ Commit and close connection
    mydb.commit()
    mycursor.close()
    mydb.close()
    print("✅ Database setup complete!")

except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
