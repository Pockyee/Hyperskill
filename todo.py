import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a database engine (using SQLite as the database)
engine = create_engine('sqlite:///todo.db')
Base = declarative_base()


# Define the 'Tasks' table schema
class Tasks(Base):
    __tablename__ = "task"  # Table name in the database
    id = Column(Integer, primary_key=True)  # Unique ID for each task (auto-increment)
    task = Column(String)  # Task description
    deadline = Column(Date, default=datetime.date.today())  # Deadline with default as today's date

    def __repr__(self):
        return f"Task(id={self.id}, task={self.task}, deadline={self.deadline})"


# Create the 'task' table in the database (if it doesn't exist)
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Menu options for the user
menu = """1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add a task
6) Delete a task
0) Exit
"""


# Function to display today's tasks
def display_todays_tasks():
    today = datetime.date.today()  # Get today's date
    tasks = session.query(Tasks).filter(Tasks.deadline == today).all()  # Retrieve tasks with today's deadline
    if tasks:
        print(f"Today {today.strftime('%B %d')}:")
        for i, task in enumerate(tasks):
            print(f"{i+1}. {task.task}")  # Display each task
    else:
        print("Nothing to do!")  # No tasks for today


# Function to display the tasks for the next 7 days (week)
def display_weeks_tasks():
    for i in range(7):  # Loop through the next 7 days
        day = datetime.date.today() + datetime.timedelta(days=i)  # Calculate each day's date
        print(day.strftime("%A %B %d:"))  # Print the day (e.g., Monday, October 10)
        tasks = session.query(Tasks).filter(Tasks.deadline == day).all()  # Query tasks for that specific day
        if tasks:
            for j, task in enumerate(tasks):
                print(f"{j+1}. {task.task}")  # Display each task
        else:
            print("Nothing to do!")  # No tasks for that day
        print("\n")  # Add an extra line for better readability


# Function to display all tasks in the database ordered by deadline
def display_all_tasks():
    tasks = session.query(Tasks).order_by(Tasks.deadline).all()  # Retrieve all tasks sorted by deadline
    for i, task in enumerate(tasks):
        print(f"{i+1}. {task.task}. {task.deadline.strftime('%d %b')}")  # Display task with deadline


# Function to display tasks with deadlines that have passed
def missed_tasks():
    tasks = session.query(Tasks).filter(Tasks.deadline < datetime.date.today()).all()  # Query missed tasks
    if tasks:
        for i, task in enumerate(tasks):
            print(f"{i+1}. {task.task}. {task.deadline.strftime('%d %b')}")  # Display missed tasks
    else:
        print("All tasks have been completed!")  # No missed tasks
    print("\n")


# Function to add a new task
def add_task():
    my_task = input("Enter a task: \n")  # Input for the task description
    my_deadline = input("Enter a deadline (YYYY-MM-DD): \n")  # Input for the deadline
    deadline_date = datetime.datetime.strptime(my_deadline, "%Y-%m-%d").date()  # Convert input to date format
    new_task = Tasks(task=my_task, deadline=deadline_date)  # Create a new task instance
    session.add(new_task)  # Add task to session (staging it to be saved)
    session.commit()  # Commit to save the task to the database
    print("The task has been added!\n")


# Function to delete a task from the database
def delete_task():
    print("Choose the number of the task you want to delete:")
    tasks = session.query(Tasks).order_by(Tasks.deadline).all()  # Retrieve all tasks sorted by deadline
    for i, task in enumerate(tasks):
        print(f"{i+1}. {task.task}. {task.deadline.strftime('%d %b')}")  # Display tasks with their index
    x = int(input())  # Get the user's choice (task index)
    session.delete(tasks[x-1])  # Delete the selected task (account for 0-indexing)
    session.commit()  # Commit the deletion
    print("The task has been deleted!\n")


# Main loop to continuously show the menu and handle user inputs
while True:
    choice = input(menu)  # Show menu and get user input

    if choice == "1":
        display_todays_tasks()  # Display today's tasks

    elif choice == "2":
        display_weeks_tasks()  # Display tasks for the upcoming week

    elif choice == "3":
        display_all_tasks()  # Display all tasks

    elif choice == "4":
        missed_tasks()  # Display missed tasks

    elif choice == "5":
        add_task()  # Add a new task

    elif choice == "6":
        delete_task()  # Delete an existing task

    elif choice == "0":
        print("Goodbye!")  # Exit the program
        break

    else:
        print("Invalid choice, please try again.")  # Handle invalid input