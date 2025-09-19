import sqlite3
from icecream import ic as print


# Step1: setup/ initialize database
def get_connection(db_name):
     try:
          return sqlite3.connect(db_name)
     except Exception as e:
          print(f"Eroor: {e}")
          raise
          
          
# Step2: create table in the database
def create_table(connection):
     query= """
     CREATE TABLE IF NOT EXISTS USERS(
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          age INTEGER,
          email TEXT UNIQUE
     )
     """
     try:
          with connection:
               connection.execute(query)
          print("Table created ssuccessfully")
     except Exception as e:
          print(e)
            
          
# Step3: add user to the database
def insert_user(connection, name:str, age:int, email:str):
     query="""
     INSERT INTO users(name, age, email) VALUES(?, ?, ?)
     """
     try:
          with connection:
               connection.execute(query, (name, age, email))
     except Exception as e:
          print(f"Erorr: {e}")
          
          
# Step4: query all users in the database
def fetch_user(connection, condition:str=None):
     query="SELECT * FROM users"
     if condition:
          query+=f" WHERE name='{condition}'"
     try: 
          with connection:         
               rows= connection.execute(query).fetchall()
          return rows
     except Exception as e:
          print(f"Error: {e}")
          return []
          
          
# Step5: delete user from the database
def delete_user(connection, user_id):
     query= "DELETE FROM users WHERE id = ?"
     with connection:
          connection.execute(query, (user_id,))
     print(f"User ID= {user_id} was deleted.")
     
     
     
# Step6: update an existing user
def update_email(connection, user_id:int, email:str):
     query= "UPDATE users SET email= ? WHERE id= ?"
     try:
          with connection:
               connection.execute(query, (user_id, email))
          print(f"User ID= {user_id}  has a new email of {email}")
     except Exception as e:
          print(e)
          
          
# 💡Bonus: ability to add multiple users
def insert_users(connection, users:list[tuple[str, int, str]]):
     query= "INSERT INTO users (name, age, email) VALUES (?, ?, ?)"
     try:
          with connection:
               connection= connection.executemany(query, users)
          print(f"{len(users)}, added to the database!.")
     except Exception as e:
          print(e)
          
          
          
# Final step: main as a wrapper function
def main():
     try:
          connection = get_connection('utility.db')
          # create table
          create_table(connection)
          # Add users
          while True:
               start= option=input("Enter an option (Add, Delete, Search, Add many): ").lower()
               
               if start =='add':
                    name=input("Enter the user name: ").title().strip()
                    age= int(input("Enter the user age: ").strip())
                    email=input("Enter the user email: ").strip()
                    insert_user(connection,name, age, email)
                    
               elif start == 'search':
                    name=input("Enter the user name to search: ").title().strip()
                    for user in fetch_user(connection, condition=name):
                         print(f"The user data is:\n{user}")
                         
               elif start == 'delete':
                    user_id= int(input("Enter the user ID to delete: "))
                    delete_user(connection, user_id)
                    
               elif start == "update":
                    user_id= int(input("Enter the user ID to update: "))
                    email= input("Enter a new email of the user: ").strip()
                    update_email(connection, user_id, email)
                    
               elif start == "add many":
                    users= []
                    while True:
                         name=input("Enter the user name or (type 'done' to exit): ").title().strip()
                         if name.lower() == 'done':
                              break
                         age_input=input("Enter the user age: ").strip()
                         if not age_input.isdigit():
                              print("Invalide age, try again!.")
                         age= int(age_input)
                         email=input("Enter the user email: ").strip()
                         users.append((name, age, email))
                         if users:
                              insert_users(connection, users)
                         else:
                              print("No user to add!.")
     finally:
          connection.close()
     
if __name__=="__main__":
     main()