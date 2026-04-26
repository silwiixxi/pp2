import psycopg2
import json
import csv
from connect import get_connection

# ---------- FILTER BY GROUP ----------
def filter_by_group(conn):
    group = input("Enter group name: ")
    cur = conn.cursor()
    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group,))
    
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found")

    cur.close()


# ---------- SEARCH BY EMAIL ----------
def search_by_email(conn):
    email = input("Enter email part: ")
    cur = conn.cursor()
    cur.execute("""
        SELECT name, email FROM contacts
        WHERE email ILIKE %s
    """, ('%' + email + '%',))

    rows = cur.fetchall()
    print(rows if rows else "No results")
    cur.close()


# ---------- SORT ----------
def sort_contacts(conn):
    field = input("Sort by (name/birthday): ")

    allowed = ["name", "birthday"]
    if field not in allowed:
        print("Invalid field")
        return

    cur = conn.cursor()
    cur.execute(f"""
        SELECT name, email, birthday
        FROM contacts
        ORDER BY {field}
    """)

    for row in cur.fetchall():
        print(row)

    cur.close()


# ---------- PAGINATION ----------
def paginate(conn):
    page = 0
    limit = 5

    while True:
        cur = conn.cursor()
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, page * limit))
        rows = cur.fetchall()

        print("\n--- PAGE ---")
        for r in rows:
            print(r)

        cur.close()

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            page += 1
        elif cmd == "prev" and page > 0:
            page -= 1
        elif cmd == "quit":
            break


# ---------- EXPORT JSON ----------
def export_json(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
    """)

    rows = cur.fetchall()

    data = []
    for r in rows:
        data.append({
            "name": r[0],
            "email": r[1],
            "birthday": str(r[2]) if r[2] else None,
            "group": r[3],
            "phone": r[4],
            "type": r[5]
        })

    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Exported to contacts.json")
    cur.close()


# ---------- IMPORT JSON ----------
def import_json(conn):
    with open("contacts.json") as f:
        data = json.load(f)

    cur = conn.cursor()

    for row in data:
        name = row["name"]
        email = row["email"]
        birthday = row["birthday"]
        group = row["group"]
        phone = row["phone"]
        ptype = row["type"]

        # check contact
        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists. skip/overwrite: ")
            if choice == "skip":
                continue
            elif choice == "overwrite":
                cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        # group
        cur.execute("""
            INSERT INTO groups(name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
        """, (group,))

        cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
        gid = cur.fetchone()[0]

        # contact
        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (name, email, birthday, gid))

        cid = cur.fetchone()[0]

        # phone
        if phone:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (cid, phone, ptype))

    conn.commit()
    print("Import complete")
    cur.close()


# ---------- IMPORT CSV ----------
def import_csv(conn):
    with open("contacts.csv") as f:
        reader = csv.DictReader(f)
        cur = conn.cursor()

        for row in reader:
            # group
            cur.execute("""
                INSERT INTO groups(name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
            """, (row['group'],))

            cur.execute("SELECT id FROM groups WHERE name=%s", (row['group'],))
            gid = cur.fetchone()[0]

            # contact
            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (row['name'], row['email'], row['birthday'], gid))

            cid = cur.fetchone()[0]

            # phone
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (cid, row['phone'], row['type']))

    conn.commit()
    print("CSV import complete")
    cur.close()

# ---------- MENU ----------
def main():
    conn = get_connection()

    while True:
        print("\n1.Filter by group")
        print("2.Search by email")
        print("3.Sort")
        print("4.Pagination")
        print("5.Export JSON")
        print("6.Import JSON")
        print("7.Import CSV")
        print("0.Exit")

        choice = input("Choose: ")

        if choice == "1":
            filter_by_group(conn)
        elif choice == "2":
            search_by_email(conn)
        elif choice == "3":
            sort_contacts(conn)
        elif choice == "4":
            paginate(conn)
        elif choice == "5":
            export_json(conn)
        elif choice == "6":
            import_json(conn)
        elif choice == "7":
            import_csv(conn)
        elif choice == "0":
            break

    conn.close()


if __name__ == "__main__":
    main()