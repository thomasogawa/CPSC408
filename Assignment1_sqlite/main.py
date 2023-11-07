# Thomas Ogawa
# 2370770
# togawa@chapman.edu
# CPSC 408-01
# Assignment #1

import sqlite3
import csv
import random

# Establish connection to the database
conn = sqlite3.connect(
    '/Users/thomasogawa/PycharmProjects/Assignment1_sqlite/StudentDB.sqlite')  # establish connection to db
mycursor = conn.cursor()


# #Write a python function to import the students.csv file (provided to you) into
# your newly created Students table.
def import_students():
    # list of 5 advisors to randomly assign to students
    advisors = ["Dr. Stevens", "Dr. Linstead", "Sir German", "Dr. Jones", "Dr. Who?"]

    # a try catch block to try and add in data from csv file
    try:
        # open the file
        with open("./students.csv", 'r') as csvfile:
            # Read the file
            csvreader = csv.DictReader(csvfile)
            print("Opened File")

            # Loop through the file
            for row in csvreader:
                # Insert the data into the table
                sql = (
                    "INSERT INTO Students (FirstName, LastName, Address, City, State, ZipCode, MobilePhoneNumber, Major, GPA, FacultyAdvisor, isDeleted) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
                val = (row['FirstName'],
                       row['LastName'],
                       row['Address'],
                       row['City'],
                       row['State'],
                       row['ZipCode'],
                       row['MobilePhoneNumber'],
                       row['Major'],
                       float(row['GPA']),  # Assuming GPA is a float
                       random.choice(advisors),  # Randomly choose an advisor from advisors list
                       0  # isDeleted flag
                       )
                mycursor.execute(sql, val)

        conn.commit()

        print("Successfully Loaded Data")
    # catch any errors
    except:
        print("Error Loading Data")


# Display All Students and all of their attributes.
# Create the necessary SELECT statement to produce this result to
# standard output
def display_students():
    # a try catch block to catch any errors
    try:
        # Select all students from the table (not including soft deleted students)
        sql = "SELECT * FROM Students WHERE isDeleted = 0"
        mycursor.execute(sql)

        # Print the results
        for row in mycursor:
            print(row)
    # catch any errors
    except:
        # print an error message
        print("Error Loading Data")


# Function to check if a string is a float, used to validate GPA
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


# Add New Students
# All attributes are required when creating a new student.
# Please make sure to validate user input appropriately.
# for example, a GPA can’t have a value of ‘foobar’ etc.
def add_student():
    # a try catch block to catch any errors
    try:
        # Get the user input
        # While loop to validate firstname
        while True:
            first_name = input("Please enter the student's first name: ")
            if first_name == "":
                print("Please enter a first name")
            else:
                break
        # While loop to validate lastname
        while True:
            last_name = input("Please enter the student's last name: ")
            if last_name == "":
                print("Please enter a last name")
            else:
                break
        # While loop to validate address
        while True:
            address = input("Please enter the student's address: ")
            if address == "":
                print("Please enter an address")
            else:
                break
        # While loop to validate city
        while True:
            city = input("Please enter the student's city: ")
            if city == "":
                print("Please enter a city")
            else:
                break

        # While loop to validate address
        while True:
            state = input("Please enter the student's state: ")
            if state == "":
                print("Please enter a state")
            else:
                break

        # While loop to validate zip code, zip code must be numbers only
        while True:
            zip_code = input("Please enter the student's zip code: ")
            if zip_code.isdigit():
                break
            else:
                print("Please enter a valid zip code")

        # While loop to validate mobile phone number, mobile phone cannot be letters only
        while True:
            mobile_phone_number = input("Please enter the student's mobile phone number: ")
            if not mobile_phone_number.isalpha():
                break
            else:
                print("Please enter a valid mobile phone number")

        # While loop to validate major, major must be a string possibly with spaces
        while True:
            major = input("Please enter the student's major: ")
            if all(char.isalpha() or char.isspace() for char in major):
                break
            else:
                print("Please enter a valid major")

        # While loop to validate gpa, gpa must be a float
        while True:
            gpa = input("Please enter student's GPA:")
            if gpa.isdigit() or is_float(gpa):  # Using is_float function to validate GPA
                break
            else:
                print("Please enter a valid GPA")

        # While loop to validate faculty advisor, faculty advisor must be a string possibly with spaces or periods
        while True:
            faculty_advisor = input("Please enter the student's faculty advisor: ")
            if all(char.isalpha() or char.isspace() or char == '.' for char in faculty_advisor):
                break
            else:
                print("Please enter a valid faculty advisor")

        print("Adding Student")
        # Insert the data into the table
        sql = (
            "INSERT INTO Students (FirstName, LastName, Address, City, State, ZipCode, MobilePhoneNumber, Major, GPA, FacultyAdvisor, isDeleted) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        val = (first_name,
               last_name,
               address,
               city,
               state,
               zip_code,
               mobile_phone_number,
               major,
               gpa,
               faculty_advisor,
               0
               )
        mycursor.execute(sql, val)

        conn.commit()

        print("Successfully Added Student")
    except:
        print("Error Loading Data")


# Update Students Method
#  Only the following fields can be updated
#  Major, Advisor, MobilePhoneNumber
#  Make sure that your UPDATE statement makes use of the correct key
#  so that you don’t update every record in the database.
def update_student():
    valid_student = False  # Boolean to check if the student exists
    while not valid_student:

        student_id = input("Please enter the student's ID: ")

        try:
            # Convert the input to an integer
            student_id = int(student_id)

            mycursor.execute("SELECT * FROM Students WHERE StudentId = ?", (student_id,))

            query_result = mycursor.fetchall()  # Store results for to verify in next step
            # Print the results, check query_result is not empty (student exists)
            if query_result:
                print("Student Found:" + str(query_result))
                valid_student = True
            else:
                print("Student Not Found please enter a valid ID")

        except:
            print("Sorry this ID is does not exist or is invalid please enter a valid ID (numeric value).")

    # After verifying studentID is valid, update the student
    finished_update = False  # Boolean to check if the user is finished updating the student

    while not finished_update:
        print("Choose an option to update for the student below:")
        # Print the student's current information, useful for seeing students info after being updated
        mycursor.execute("SELECT * FROM Students WHERE StudentId = ?", (student_id,))
        print(mycursor.fetchall())

        print("1. Major")
        print("2. Faculty Advisor")
        print("3. Mobile Phone Number")
        print("4. Quit")

        user_input = input("Please enter a choice(number): ")

        if user_input == "1":
            while True:
                major = input("Please enter the student's major: ")
                if all(char.isalpha() or char.isspace() or char == '.' for char in major):
                    break
                else:
                    print("Please enter a valid major")
            mycursor.execute("UPDATE Students SET Major = ? WHERE StudentId = ?", (major, student_id,)
                             )  # Update the student's major
            conn.commit()
        elif user_input == "2":
            while True:
                faculty_advisor = input("Please enter the student's faculty advisor: ")
                if all(char.isalpha() or char.isspace() or char == '.' for char in faculty_advisor):
                    break
                else:
                    print("Please enter a valid faculty advisor")
            mycursor.execute("UPDATE Students SET FacultyAdvisor = ? WHERE StudentId = ?",
                             (faculty_advisor, student_id,)) # Update the student's faculty advisor
            conn.commit()
        elif user_input == "3":
            while True:
                mobile_phone_number = input("Please enter the student's mobile phone number: ")
                if not mobile_phone_number.isalpha():
                    break
                else:
                    print("Please enter a valid mobile phone number")
            mycursor.execute("UPDATE Students SET MobilePhoneNumber = ? WHERE StudentId = ?",
                             (mobile_phone_number, student_id,)) # Update the student's mobile phone number
            conn.commit()
        elif user_input == "4":
            finished_update = True
        else:
            print("Invalid Input, please enter a number between 1 and 4")


# Function to delete a student
# Performs a soft delete taking in a studentID and setting isDeleted to 1
def delete_student():
    while True:
        student_id = input("Please enter the student's ID: ")

        try:
            # Convert the input to an integer
            student_id = int(student_id)

            # SQL statement to update the student's isDeleted flag
            mycursor.execute("UPDATE Students SET isDeleted = 1 WHERE StudentId = ?", (student_id,))
            conn.commit()
            break
        except:
            print("Sorry this ID is does not exist or is invalid please enter a valid ID (numeric value).")


# Function that Searches and Displays students by Major, GPA, City, State and Advisor.
# User should be able to query by the 5 aforementioned fields
def search_students():
    is_searching = True
    while is_searching:
        print("Choose an option to search for the student(s) below:")
        print("1. Major")
        print("2. GPA")
        print("3. City")
        print("4. State")
        print("5. Advisor")
        print("6. Quit")
        user_input = input("Please enter a choice(number): ")
        if user_input == "1":
            while True:
                major = input("Please enter the student's major: ")
                if all(char.isalpha() or char.isspace() or char == '.' for char in major):
                    break
                else:
                    print("Please enter a valid major")
            mycursor.execute("SELECT * FROM Students WHERE Major = ?", (major,))
            for row in mycursor:
                print(row)
        elif user_input == "2":
            while True:
                gpa = input("Please enter student's GPA:")
                if gpa.isdigit() or is_float(gpa):
                    break
                else:
                    print("Please enter a valid GPA")
            mycursor.execute("SELECT * FROM Students WHERE GPA = ?", (gpa,))
            for row in mycursor:
                print(row)
        elif user_input == "3":
            while True:
                city = input("Please enter the student's city: ")
                if city == "":
                    print("Please enter a city")
                else:
                    break
            mycursor.execute("SELECT * FROM Students WHERE City = ?", (city,))
            for row in mycursor:
                print(row)
        elif user_input == "4":
            while True:
                state = input("Please enter the student's state: ")
                if state == "":
                    print("Please enter a state")
                else:
                    break
            mycursor.execute("SELECT * FROM Students WHERE State = ?", (state,))
            for row in mycursor:
                print(row)
        elif user_input == "5":
            while True:
                faculty_advisor = input("Please enter the student's faculty advisor: ")
                if all(char.isalpha() or char.isspace() or char == '.' for char in
                       faculty_advisor):  # Need to have a space in the name
                    break
                else:
                    print("Please enter a valid faculty advisor")
            mycursor.execute("SELECT * FROM Students WHERE FacultyAdvisor = ?", (faculty_advisor,))
            for row in mycursor:
                print(row)
        elif user_input == "6":
            print("Leaving Search")
            is_searching = False  # Break out of the while loop
        else:
            print("Invalid Input, please enter a number between 1 and 6")


# main function to run the program
def main():
    # While loop to keep the program running until the user quits
    while True:
        # Print out the main menu and ask the user for inout
        print("Welcome to the Student Database")
        print("Please select an option from the menu below")
        print("1. Initialize Database")
        print("2. Display All Students")
        print("3. Add A New Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Search/Display Students")
        print("7. Quit")

        # Get the user input
        user_input = input("Please enter a choice(number): ")

        # If the user enters 1, call the import_students function
        if user_input == "1":
            print("Calling Import Students Function")
            import_students()
            print("Finished Importing Students")
        # If the user enters 2, call the display_students function
        elif user_input == "2":
            display_students()
        # If the user enters 3, call the add_student function
        elif user_input == "3":
            print("Calling Add Student Function")
            add_student()
            print("Finished Adding Student")
        # If the user enters 4, call the update_student function
        elif user_input == "4":
            print("Calling Update Student")
            update_student()
            print("Finished Updating Student")
        # If the user enters 5, call the delete_student function
        elif user_input == "5":
            print("Calling Delete Student Function")
            delete_student()
            print("Finished Deleting Student")
        # If the user enters 6, call the search_students function
        elif user_input == "6":
            print("Searching/Displaying Students")
            search_students()
            print("Finished Searching/Displaying Students")
        # If the user enters 7, quit the program
        elif user_input == "7":
            print("Quitting Program")
            conn.close()  # quit program
            break
        # If the user enters anything else, print an error message
        else:
            print("Invalid Input, please enter a number between 1 and 7")


# Call the main function
main()
