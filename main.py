# import modules
from sqlalchemy import create_engine, String, Integer, ForeignKey, Column
from sqlalchemy.ext.declarative import declarative_base # Define base claas for models
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError


# create your database
engine = create_engine("sqlite:///database.db", echo=False)
base = declarative_base()
Session = sessionmaker(bind=engine)# bind=engine this makes all sessions know where to send their queries
session = Session()


# Create Models (Users/Tasks)
class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # nullable:refer to NULL or NOT NULL
    email = Column(String, nullable=False, unique=True)
    tasks = relationship("Task", back_populates="user", cascade="all,delete-orphan")


class Task(base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks")

base.metadata.create_all(engine)

# Utility functions
def get_user_by_email(email):
    return session.query(User).filter_by(email=email).first()

def confirm_operation(prompt):
    return input(f"{prompt} yes/no: ")== 'yes'



# CRUD operations
def add_user():
    name, email= input("Enter name: ").title().strip(), input("Enter email: ").strip()
    if get_user_by_email(email):
        print(f"User {name} is already exist: {email}")
        return
    
    try:
        session.add(User(name=name, email=email))
        session.commit()
        print(f"User: {name} added!.")
    except IntegrityError:
        session.rollback()
        print("Error")
        
        
def add_task():
    email=input("Enter the user email to add a task: ").strip()
    user= get_user_by_email(email)
    if not user:
        print("No user foud with that email!")
        return
    
    title, description= input("Enter the task title: "), input("Enter the description of the task: ")
    session.add(Task(title= title, description= description, user=user))
    session.commit()
    print(f"{title}: {description} added to database.")
    
# query to find something
def query_user():
    for user in session.query(User).all():
        print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")


def query_task():
    email= input("Enter the email of the user for tasks: ").strip()
    user= get_user_by_email(email=email)
    if not user:
        print("There was no user with that email.")
        return
    
    if not user.tasks:
        print(f"User '{user.name}' exists, but has no tasks assigned.")
        return

    for task in user.tasks:
        print(f"ID: {task.id}, Title: {task.title}, Description: {task.description}")


def delete_user():
    email=input("Enter the email of the user to delete: ").strip()
    user= get_user_by_email(email)
    if not user:
        print('No user found with that email.')
        return
    if confirm_operation(f"Are you sure you want to delete`{user.name}`"):
        session.delete(user)
        session.commit()
        print("User has been deleted!")


def delete_task(): 
    task_id=input("Enter the ID of the task to delete")
    task= session.query(Task).get(task_id)
    if not task:
        print(f"There is no task with ID={task_id}!")
        return
    session.delete(task)
    session.commit()
    print("Task has deleted!")


def update_user():
    email= input("Enter the email of user you want to update: ").strip()
    user= get_user_by_email(email)
    if not user:
        print("There is no user with that email.")
        return
    
    user.name=input("Enter the new name of the user (leave blanck to say the same): ") or user.name
    user.email=input("Enter the new email of the user (leave blank to stay the same): ") or user.email
    session.commit()
    print("The user has been updated!.")
    

# Main operations
def main():
    options={
        '1': add_user,
        '2': add_task,
        "3": query_user,
        '4': query_task,
        '5': update_user,
        '6': delete_user,
        '7': delete_task,
        '8': exit,

    } 
    while True:
        print("Options\n====================\n1- Add user.\n2- Add task.\n3- Query user.\n4- Query task.\n5- Update user.\n6- Delete user.\n7- Delete task.\n8- Exit.")
        choice= input("Pick one of these options, please: ")
        if choice in options:
            if choice =='8':
                print("exiting the programme....")
                break
            action= options.get(choice)# Give the value associated with what we shosen
            if action:
                action()
            else:
                print("That's not an option")
            # options[choice]()   #Call the selected function
        else:
            print(f"{choice}: Invalide command, try again!")
            
            
            
if __name__=="__main__":
    main()