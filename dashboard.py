import streamlit as st
import mysql.connector

# Database Connection Configuration
db_config = {
    'host': '38.242.131.49:182',  # Replace with the IP address or hostname of the server where database2 is running
    'user': 'shlink2',              # Replace with your MariaDB username for database2
    'password': 'dizi@123',         # Replace with your MariaDB password for database2
    'database': 'shlink2'           # Replace with the name of the database in database2
}

# Connect to the MariaDB database
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    st.success("Connected to the database")
except Exception as e:
    st.error(f"Error connecting to the database: {e}")

# Streamlit App
st.title("MariaDB Streamlit Dashboard")

# Execute SQL query and display results
if 'conn' in locals():
    cursor.execute("SELECT * FROM your_table_name")  # Replace with your table name
    results = cursor.fetchall()

    st.subheader("Query Results:")
    st.write(results)

# Close the database connection
if 'conn' in locals():
    conn.close()
    st.info("Database connection closed")
