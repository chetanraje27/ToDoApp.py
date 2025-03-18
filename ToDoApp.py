import mysql.connector as mysql

# Connect to MySQL
con = mysql.connect(host="localhost", user="root", passwd="pass@1234")

cursor = con.cursor()

# Create database if not exists
cursor.execute("CREATE DATABASE IF NOT EXISTS TODOAPP")
cursor.execute("USE TODOAPP")

# Create task table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tb_todo (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task VARCHAR(50) NOT NULL,
        status ENUM('pending', 'completed') DEFAULT 'pending'
    )
""")

# Show tables
cursor.execute("SHOW TABLES")
for i in cursor:
    print(i)

# Task management loop
while True:
    print("\nTask Management")
    print("1. Add Task")
    print("2. View Task")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        task = input("Enter task: ")
        cursor.execute("INSERT INTO tb_todo (task) VALUES (%s)", (task,))
        con.commit()
        print("Task added successfully!")

    elif choice == "2":
        cursor.execute("SELECT * FROM tb_todo")
        tasks = cursor.fetchall()
        if not tasks:
            print("No tasks available!")
        else:
            for task in tasks:
                print(f"{task[0]}. {task[1]} - {task[2]}")

    elif choice == "3":
        task_id = input("Enter task ID to update: ")
        new_status = input("Enter new status (pending/completed): ").lower()
        if new_status in ["pending", "completed"]:
            cursor.execute("UPDATE tb_todo SET status = %s WHERE id = %s", (new_status, task_id))
            con.commit()
            if cursor.rowcount > 0:
                print("Task updated successfully!")
            else:
                print("Task not found!")
        else:
            print("Invalid status. Use 'pending' or 'completed'.")

    elif choice == "4":
        task_id = input("Enter task ID to delete: ")
        cursor.execute("DELETE FROM tb_todo WHERE id = %s", (task_id,))
        con.commit()
        if cursor.rowcount > 0:
            print("Task deleted successfully!")
        else:
            print("Task not found!")

    elif choice == "5":
        print("Exiting Task Management...")
        break

    else:
        print("Invalid choice. Please try again.")

# Close connection
con.close()
