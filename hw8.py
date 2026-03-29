#CONFIG.PY
DB_CONFIG =  {
    "host": "localhost",
    "database": "phonebook_db",
    "user": "aneli",
    "password": "password"
}

#CONNECT.PY
import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="aneli",
        password="password",
        port=5432
    )

#FUNCTIONS.SQL
CREATE OR REPLACE FUNCTION search_contacts(p TEXT)
RETURNS TABLE(name TEXT, phone TEXT)
AS $$
BEGIN
    RETURN QUERY
    SELECT pbook.name, pbook.phone
    FROM phonebook pbook
    WHERE pbook.name ILIKE '%' || p || '%'
       OR pbook.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, offs INT)
RETURNS TABLE(id INT, name TEXT, phone TEXT)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    ORDER BY id
    LIMIT lim OFFSET offs;
END;
$$ LANGUAGE plpgsql;

#PHONEBOOK.PY
from connect import get_connection

def show_menu():
    print("""
1. Add / Update contact
2. Bulk insert
3. Search contacts
4. Show paginated contacts
5. Delete contact
0. Exit
""")

def add_update():
    conn = get_connection()
    cur = conn.cursor()

    name = input("Name: ")
    phone = input("Phone: ")

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))

    conn.commit()
    cur.close()
    conn.close()

    print("Saved!")

def bulk_insert():
    conn = get_connection()
    cur = conn.cursor()

    names = input("Names (comma): ").split(",")
    phones = input("Phones (comma): ").split(",")

    cur.execute(
        "CALL bulk_insert_contacts(%s, %s)",
        (names, phones)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Bulk insert done!")

def search():
    conn = get_connection()
    cur = conn.cursor()

    text = input("Search: ")

    cur.execute("SELECT * FROM search_contacts(%s)", (text,))
    rows = cur.fetchall()

    for r in rows:
        print(r)

    cur.close()
    conn.close()

def paginate():
    conn = get_connection()
    cur = conn.cursor()

    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    cur.execute(
        "SELECT * FROM get_contacts_paginated(%s, %s)",
        (limit, offset)
    )

    for r in cur.fetchall():
        print(r)

    cur.close()
    conn.close()

def delete():
    conn = get_connection()
    cur = conn.cursor()

    value = input("Name or phone to delete: ")

    cur.execute("CALL delete_contact(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()

    print("Deleted!")

def main():
    while True:
        show_menu()
        choice = input("Choice: ")

        if choice == "1":
            add_update()
        elif choice == "2":
            bulk_insert()
        elif choice == "3":
            search()
        elif choice == "4":
            paginate()
        elif choice == "5":
            delete()
        elif choice == "0":
            break
        else:
            print("Wrong choice")

if __name__ == "__main__":
    main()

#PROCCEDURES
CREATE OR REPLACE PROCEDURE upsert_contact(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE phone = p_phone) THEN
        UPDATE phonebook
        SET name = p_name
        WHERE phone = p_phone;
    ELSE
        INSERT INTO phonebook(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(names TEXT[], phones TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP

        IF phones[i] ~ '^[0-9]+$' THEN
            INSERT INTO phonebook(name, phone)
            VALUES (names[i], phones[i]);
        END IF;

    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(p TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p OR phone = p;
END;
$$;
