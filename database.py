import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="sys"
    )

# insert data into the customer table
def insert_customer_data(cur, username, password, phone_number):
    cur.execute("""
        INSERT INTO customer (username, password, phone_number)
        VALUES (%s, %s, %s)
    """, (username, password, phone_number)) 

    print("Customer data inserted successfully.")
    
def update_customer_data(cur, username, field, new_value):
    if field == "username":
        cur.execute("""
            UPDATE customer
            SET username = %s
            WHERE username = %s
        """, (new_value, username))
    elif field == "password":
        cur.execute("""
            UPDATE customer
            SET password = %s
            WHERE username = %s
        """, (new_value, username))
    elif field == "phone_number":
        cur.execute("""
            UPDATE customer
            SET phone_number = %s
            WHERE username = %s
        """, (new_value, username))
    else:
        print("Invalid field!")
        return
    
    print(f"{field.capitalize()} updated successfully!")

# to show the account info
def display_account_info(cur, username):
    cur.execute("""
        SELECT username, password, phone_number
        FROM customer
        WHERE username = %s
    """, (username,))
    
    result = cur.fetchone()
    
    # If the user is found, display their account details
    if result:
        print("\nAccount Information:")
        print(f"Username: {result[0]}")
        print(f"Password: {result[1]}")
        print(f"Phone Number: {result[2]}")
    else:
        print(f"No account found for username: {username}")

# Main function to run the program
def main():
    # Connect to the database
    conn = connect_to_db()
    cur = conn.cursor()

    while True:
        print("\n--- Home Screen ---")
        choice = input("Do you want to (1) insert new data, (2) update existing data, (3) view your account, or (4) exit? Enter 1, 2, 3, or 4: ")

        if choice == "1":
            # Get user input for new customer data
            username = input("Enter username: ")
            password = input("Enter password: ")
            phone_number = input("Enter phone number: ")

            insert_customer_data(cur, username, password, phone_number)

            conn.commit()
            print("Customer data inserted successfully.")

        elif choice == "2":
            # Get the username to identify which customer to update
            username = input("Enter your username to update your details: ")

            field = input("Which field would you like to update? (username, password, phone_number): ").strip().lower()
            
            new_value = input(f"Enter new value for {field}: ")

            # Update the customer data
            update_customer_data(cur, username, field, new_value)
            conn.commit()

        elif choice == "3":
            username = input("Enter your username to view your account: ")
            display_account_info(cur, username)

        elif choice == "4":
            print("Exiting the program.")
            break  

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()