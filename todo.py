import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a database engine
engine = create_engine('sqlite:///todo.db')
Base = declarative_base()


# Define the tasks table
class Tasks(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)  # Automatically generated ID
    task = Column(String)
    deadline = Column(Date, default=datetime.date.today())  # Default value is today's date

    def __repr__(self):
        return f"Task(id={self.id}, task={self.task}, deadline={self.deadline})"


# Create the table in the database
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Menu options
menu = """1) Today's tasks
2) Week's tasks
3) All tasks
4) Add a task
0) Exit
"""


# Function to add a task
def add_task():
    my_task = input("Enter a task: \n")
    my_deadline = input("Enter a deadline : \n")
    deadline_date = datetime.datetime.strptime(my_deadline, "%Y-%m-%d").date()
    new_task = Tasks(task=my_task,deadline=deadline_date)
    session.add(new_task)
    session.commit()  # Commit to save the task to the database
    print("The task has been added!")


# Function to display today's tasks
def display_todays_tasks():
    today = datetime.date.today()  # Get today's date
    tasks = session.query(Tasks).filter(Tasks.deadline == today).all()  # Query tasks due today
    if tasks:
        print(f"Today {today.strftime('%B %d')}:")
        i = 0
        for task in tasks:
             print(f"{i+1}. {task.task}")
             i+=1
    else:
        print("Nothing to do!")


# Function to display week's tasks
def display_weeks_tasks():
    for i in range(7):
        day = datetime.date.today()+datetime.timedelta(days=i)
        print(day.strftime("%A %B %d:"))
        tasks = session.query(Tasks).filter(Tasks.deadline == day).all()
        if tasks:
            j=0
            for task in tasks:
                print(f"{j+1}. {task.task}")
                j+=1
        else:
            print("Noting to do!")
        print("\n")

def display_all_tasks():
    tasks = session.query(Tasks).order_by(Tasks.deadline).all()
    i=0
    for task in tasks:
        print(f"{i+1}. {task.task}. {task.deadline.strftime('%d %b')}")
        i+=1



# Main loop to display the menu and handle user input
while True:
    choice = input(menu).strip()  # Get user input and remove any extra spaces

    if choice == "1":
        display_todays_tasks()  # Display today's tasks

    elif choice == "2":
        display_weeks_tasks()

    elif choice == "3":
        display_all_tasks()

    elif choice == "4":
        add_task()

    elif choice == "0":  # Exit the program
        print("Goodbye!")
        break  # Exit the loop

    else:
        print("Invalid choice, please try again.")