import mysql.connector

# MySQL connection setup
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="face_recognition_db"
)
db_cursor = db_connection.cursor()

# Function to save detected face data to the MySQL database
def save_face_data(face_data):
    timestamp = face_data["time"]
    name = face_data["name"]
    student_id = face_data["student_id"]
    # Insert data into the MySQL database
    day = timestamp.split()[0].split('-')[2]
    select_query = "SELECT timestamp FROM face_data WHERE name = %s AND student_id = %s ORDER BY timestamp DESC LIMIT 1"
    db_cursor.execute(select_query, (name, student_id))

    result = db_cursor.fetchall()
    if len(result) != 0:
        last_entry = result[0][0]
        #last_enry is in datetime format, so we need to extract the day from it
        last_day = str(last_entry).split()[0].split('-')[2]
        if int(day) - int(last_day) > 1:
            print("Inserting data")
            insert_query = "INSERT INTO face_data (name, student_id, timestamp) VALUES (%s, %s, %s)"
            db_cursor.execute(insert_query, (name, student_id, timestamp))
            db_connection.commit()
            print(f"Face data saved to MySQL database")
            return True
        else:
            pass
    else:
        print("Inserting data")
        insert_query = "INSERT INTO face_data (name, student_id, timestamp) VALUES (%s, %s, %s)"
        db_cursor.execute(insert_query, (name, student_id, timestamp))
        db_connection.commit()
        print(f"Face data saved to MySQL database")
        return True
    

# Function to retrieve attendance data from the MySQL database
def get_attendance_data():
    select_query = "SELECT name, student_id, timestamp FROM face_data ORDER BY timestamp DESC"
    db_cursor.execute(select_query)
    result = db_cursor.fetchall()
    return result

# Close the MySQL connection
def close_db_connection():
    db_cursor.close()
    db_connection.close()
