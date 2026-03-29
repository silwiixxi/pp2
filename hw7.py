#CONFIG.PY
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

#CONNECT.PY
import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user="aneli",
        password=DB_PASSWORD,
        port=DB_PORT
    )

#CONTACTS.CSV
Name,Phone
Aneli,87011234501
Asema,87011234503
Askhat,87011234504

#PHONEBOOK.PY
import csv
from connect import get_connection


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name TEXT,
            phone TEXT UNIQUE
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


def add_contact(name, phone):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


def add_from_console():
    name = input("Name: ")
    phone = input("Phone: ")
    add_contact(name, phone)


def add_from_csv():
    filename = input("CSV filename: ")

    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            cur.execute("""
                INSERT INTO phonebook (name, phone)
                VALUES (%s, %s)
                ON CONFLICT (phone) DO NOTHING
            """, (row[0], row[1]))

    conn.commit()
    cur.close()
    conn.close()


def get_all_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def search_by_name():
    name = input("Name: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE name ILIKE %s",
        (f"%{name}%",)
    )

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def search_by_phone():
    phone = input("Phone prefix: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s",
        (f"{phone}%",)
    )

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def update_contact():
    choice = input("1. Update name | 2. Update phone: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        old_name = input("Old name: ")
        new_name = input("New name: ")

        cur.execute(
            "UPDATE phonebook SET name=%s WHERE name=%s",
            (new_name, old_name)
        )

    elif choice == "2":
        name = input("Name: ")
        new_phone = input("New phone: ")

        cur.execute(
            "UPDATE phonebook SET phone=%s WHERE name=%s",
            (new_phone, name)
        )

    conn.commit()
    cur.close()
    conn.close()


def delete_contact():
    choice = input("1. By name | 2. By phone: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Name: ")
        cur.execute("DELETE FROM phonebook WHERE name=%s", (name,))

    elif choice == "2":
        phone = input("Phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))

    conn.commit()
    cur.close()
    conn.close()


def menu():
    create_table()

    while True:
        print("""
1. Add contact
2. Import CSV
3. Show all
4. Search by name
5. Search by phone
6. Update contact
7. Delete contact
0. Exit
""")

        choice = input("Choice: ")

        if choice == "1":
            add_from_console()
        elif choice == "2":
            add_from_csv()
        elif choice == "3":
            get_all_contacts()
        elif choice == "4":
            search_by_name()
        elif choice == "5":
            search_by_phone()
        elif choice == "6":
            update_contact()
        elif choice == "7":
            delete_contact()
        elif choice == "0":
            break


if __name__ == "__main__":
    menu()
