from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import os
import csv
from COURSESv2 import SecondPage
from tkinter import messagebox
from tkinter import Tk, Button, Frame
import mysql.connector

class Student:
    
    def __init__(self, root):
        # Initialize MySQL connection
        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            port="3306",
            password="",
            database="students"
        )
        
        self.cursor = self.conn.cursor()
        self.root = root
        self.root.title("MSU-IIT STUDENT INFORMATION SYSTEM")
        self.root.geometry("1350x750+0+0")
        self.root.config(bg="#001F3F")

        self.Name = StringVar()
        self.StudID = StringVar()
        self.YearLevel = StringVar()
        self.Gender = StringVar()
        self.Course_Code = StringVar()
        self.Searchbar = StringVar()

        self.create_widgets()
        self.DisplayStd()

    def Quit(self):
        quit_confirmation = tkinter.messagebox.askyesno("MSU-IIT SIS", "Are you sure you want to QUIT?")
        if quit_confirmation > 0:
            self.root.destroy()

    def check_IDNo(self, idNo):
        # Check if student ID exists in MySQL database
        query = "SELECT * FROM student WHERE ID = %s"
        self.cursor.execute(query, (idNo,))
        return bool(self.cursor.fetchone())

    def add_student(self):
        if self.StudID.get() == "" or self.Name.get() == "" or self.YearLevel.get() == "" or self.Gender.get() == "" or self.Course_Code.get() == "":
            tkinter.messagebox.showinfo("MSU-IIT SIS", "Fill in the box.")
            return

        if self.check_IDNo(self.StudID.get()):
            messagebox.showerror("Error", f"Student {self.StudID.get()} already exists.")
            return
        else:
            query = "INSERT INTO student (ID, Name, Gender, Year, Course_Code) VALUES (%s, %s, %s, %s, %s)"
            values = (self.StudID.get(), self.Name.get(), self.Gender.get(), self.YearLevel.get(), self.Course_Code.get())
            self.cursor.execute(query, values)
            self.conn.commit()
            tkinter.messagebox.showinfo("MSU-IIT SIS", "Successfully added!")
            self.DisplayStd()
            self.ClearStd()

    def ClearStd(self):
        self.StudID.set("")
        self.Name.set("")
        self.YearLevel.set("")
        self.Gender.set("")
        self.Course_Code.set("")

    def DisplayStd(self):
        self.tree.delete(*self.tree.get_children())
        query = "SELECT ID, Name, Gender, Year, Course_Code FROM student"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            self.tree.insert("", END, values=row)

    def delete_student(self):
        if not self.tree.focus():
            tkinter.messagebox.showerror("MSU-IIT SIS", "Select a student")
            return
        id_no = self.tree.item(self.tree.focus(), "values")[0]
        query = "DELETE FROM student WHERE ID = %s"
        self.cursor.execute(query, (id_no,))
        self.conn.commit()
        self.tree.delete(self.tree.focus())
        tkinter.messagebox.showinfo("MSU-IIT SIS", "Record Deleted!")

    def edit_student(self):
        if not self.tree.focus():
            tkinter.messagebox.showerror("MSU-IIT SIS", "Select a student")
            return
        values = self.tree.item(self.tree.focus(), "values")
        self.StudID.set(values[0])
        self.Name.set(values[1])
        self.Gender.set(values[2])
        self.YearLevel.set(values[3])
        self.Course_Code.set(values[4])

    def update_student(self):
        if not self.tree.focus():
            tkinter.messagebox.showerror("MSU-IIT SIS", "Select a student")
            return
        edited_values = [
            self.StudID.get(),
            self.Name.get(),
            self.Gender.get(),
            self.YearLevel.get(),
            self.Course_Code.get()
        ]
        original_id = self.tree.item(self.tree.focus(), "values")[0]

        if edited_values[0] != original_id and self.check_IDNo(edited_values[0]):
            messagebox.showerror("Error", f"Student {edited_values[0]} already exists.")
            return

        query = "UPDATE student SET ID=%s, Name=%s, Gender=%s, Year=%s, Course_Code=%s WHERE ID=%s"
        self.cursor.execute(query, (edited_values[0], edited_values[1], edited_values[2], edited_values[3], edited_values[4], original_id))
        self.conn.commit()
        tkinter.messagebox.showinfo("MSU-IIT SIS", "Successfully Updated")
        self.DisplayStd()
        self.ClearStd()

        
    def refresh_courses(self):
        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            port="3306",
            password="",
            database="students"
        )
        self.cursor = self.conn.cursor()

        courses = self.fetch_courses()
        self.comboCourseCode['values'] = courses
        tkinter.messagebox.showinfo("MSU-IIT SIS", "Courses refreshed!")

    def fetch_courses(self):
        query = "SELECT Course_Code FROM course"
        self.cursor.execute(query)
        courses = [row[0] for row in self.cursor.fetchall()]
        return courses
    '''
    def fetch_courses(self):
        query = "SELECT course_code FROM course"
        self.cursor.execute(query)
        courses = [row[0] for row in self.cursor.fetchall()]
        print("Fetched courses:", courses)  # Debug print

        return courses
    
    def refresh_courses(self):
        courses = self.fetch_courses()
        self.comboCourseCode['values'] = courses
        tkinter.messagebox.showinfo("MSU-IIT SIS", "Courses refreshed!")

    def refresh_data(self):
        # Clear the existing course data
        self.course_data = {}

        # Fetch course data from the database
        query = "SELECT Course_Code, Course_Name FROM course"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Update course_data dictionary
        for course_row in rows:
            course_code, course_name = course_row
            self.course_data[course_code] = course_name
        
        # Refresh the combobox in the main application
        self.refresh_courses()
        '''
    def create_widgets(self):
        courses = self.fetch_courses()
        ManageFrame = Frame(self.root, bd=5, relief=RIDGE, bg="Sky Blue")
        ManageFrame.place(x=1080, y=260, width=660, height=400)

        title = Label(self.root, text="STUDENT INFORMATION SYSTEM", bd=4, relief=RIDGE, font=("Source code", 40, "bold"),
                      bg="Sky Blue", fg="#2B8180")
        title.pack(side=TOP)

        DetailFrame = Frame(self.root, bd=4, relief=RIDGE, bg="Sky Blue")
        DetailFrame.place(x=20, y=100, width=1030, height=560)

        ButtonFrame = Frame(self.root, bd=4, bg="Sky Blue", relief=RIDGE)
        ButtonFrame.place(x=1080, y=100, width=430, height=140)

        TableFrame = Frame(DetailFrame, bd=4, relief=RIDGE, bg='Sky Blue')
        TableFrame.place(x=10, y=10, width=1030, height=450)

        title = Label(ManageFrame, text="STUDENT INFORMATION", bg="#2B8180", fg="White", font=("Source code", 20, "bold"))
        title.grid(row=0, columnspan=2, pady=20)
        
        self.lblStdID = Label(ManageFrame, font=("Source code", 15, "bold"), text="ID Number:", padx=2, pady=2, bg="#2B8180", fg="black", height=1, width=11)
        self.lblStdID.grid(row=1, column=0, padx=5, pady=5)
        self.txtStdID = Entry(ManageFrame, font=("Source code", 15, "bold"), textvariable=self.StudID, relief=GROOVE, width=27, fg="#2B8180")
        self.txtStdID.grid(row=1, column=1)

        self.lblname = Label(ManageFrame, font=("Source code", 15, "bold"), text="Name:", padx=2, pady=2, bg="#2B8180", fg="black", height=1, width=11)
        self.lblname.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.txtname = Entry(ManageFrame, font=("Source code", 15, "bold"), textvariable=self.Name, relief=GROOVE, width=27, fg="#2B8180")
        self.txtname.grid(row=2, column=1)

        self.lblYearlevel = Label(ManageFrame, font=("Source code", 15, "bold"), text="Year Level:", padx=2, pady=2, bg="#2B8180", fg="black", height=1, width=11)
        self.lblYearlevel.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.comboYearlevel = ttk.Combobox(ManageFrame, font=("Source code", 15, "bold"), state="readonly", width=27, textvariable=self.YearLevel)
        self.comboYearlevel['values'] = ("First Year", "Second Year", "Third Year", "Fourth Year")
        self.comboYearlevel.grid(row=3, column=1, padx=5, pady=5)

        self.lblgender = Label(ManageFrame, font=("Source code", 15, "bold"), text="Gender:", padx=2, pady=2, bg="#2B8180", fg="black", height=1, width=11)
        self.lblgender.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.combogender = ttk.Combobox(ManageFrame, font=("Source code", 15, "bold"), state="readonly", width=27, textvariable=self.Gender)
        self.combogender['values'] = ("Male", "Female", "Others")
        self.combogender.grid(row=4, column=1, padx=5, pady=5)

        self.lblCourseCode = Label(ManageFrame, font=("Source code", 15, "bold"), text="Course Code:", padx=2, pady=2, bg="#2B8180", fg="black", height=1, width=11)
        self.lblCourseCode.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.comboCourseCode = ttk.Combobox(ManageFrame, font=("Source code", 15, "bold"), state="readonly", width=27, textvariable=self.Course_Code)
        self.comboCourseCode['values'] = courses
        self.comboCourseCode.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.btnAddnew = Button(ButtonFrame, text="Add New", font=("Source code", 15, "bold"), height=1, width=10, bd=4, command=self.add_student)
        self.btnAddnew.grid(row=0, column=0)

        self.btnDisplay = Button(ButtonFrame, text="Update", font=("Source code", 15, "bold"), height=1, width=10, bd=4, command=self.update_student)
        self.btnDisplay.grid(row=0, column=1)

        self.btnClear = Button(ButtonFrame, text="Clear", font=("Source code", 15, "bold"), height=1, width=10, bd=4, command=self.ClearStd)
        self.btnClear.grid(row=0, column=2)

        self.btnDelete = Button(ButtonFrame, text="Delete", font=("Source code", 15, "bold"), height=1, width=10, bd=4, command=self.delete_student)
        self.btnDelete.grid(row=1, column=0)

        self.btnEdit = Button(ButtonFrame, text="Edit", font=("Source code", 15, "bold"), height=1, width=10, bd=4, command=self.edit_student)
        self.btnEdit.grid(row=1, column=1)

        self.btnExit = Button(ButtonFrame, text="Exit", font=("Source code", 15, "bold"), height=1, width=10, bd=4, command=self.Quit)
        self.btnExit.grid(row=1, column=2)

        self.Searchbar = Entry(self.root, font=("Arial", 14), bg="white", fg="black")
        self.Searchbar.place(x=200, y=600, width=400)

        self.searchbtn = Button(self.root, text="Search", font=("Source code", 10, "bold"), bg="#2B8180", fg="black", height=2, width=12, bd=5, command=self.search_data)
        self.searchbtn.place(x=90, y=590, width=100)

        self.showallbtn = Button(self.root, text="Show All", width=10, pady=5, font=("Source code", 10, "bold"), bg="#2B8180", fg="black", command=self.DisplayStd)
        self.showallbtn.place(x=750, y=590, width=100)

        self.btnRefresh = Button(self.root, text="REFRESH", width=10, pady=5, font=("Source code", 10, "bold"), bg="#2B8180", fg="black",  command=self.refresh_courses)
        self.btnRefresh.place(x=850, y=590, width=100)


        scroll_x = Scrollbar(TableFrame, orient=HORIZONTAL)
        scroll_y = Scrollbar(TableFrame, orient=VERTICAL)
        self.tree = ttk.Treeview(TableFrame, columns=("ID", "Name", "Gender", "Year", "Course_Code"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.tree.xview)
        scroll_y.config(command=self.tree.yview)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Course_Code", text="Course_Code")
        self.tree['show'] = 'headings'
        
        self.tree.column("ID", width=100)
        self.tree.column("Name", width=200)
        self.tree.column("Gender", width=100)
        self.tree.column("Year", width=100)
        self.tree.column("Course_Code", width=100)
        
        self.tree.pack(fill=BOTH, expand=1)

        self.btnSecondPage = Button(self.root, text="Course Page", font=("Source code", 15, "bold"), height=1, width=10, bd=4, command=self.open_second_page)
        self.btnSecondPage.place(x=1300, y=20)  # Adjust the row and column as necessary


    def search_data(self):
        search = self.Searchbar.get()
        query = "SELECT * FROM student WHERE Name LIKE %s OR ID LIKE %s OR Gender LIKE %s OR Year LIKE %s OR Course_Code LIKE %s"
        search_term = f"%{search}%"
        self.cursor.execute(query, (search_term, search_term, search_term, search_term, search_term))
        rows = self.cursor.fetchall()
        if not rows:
            tkinter.messagebox.showinfo("Search Result", "No matching records found.")
        else:
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert("", END, values=row)

    def open_second_page(self):
        self.COURSESv2 = SecondPage(self.root)


if __name__ == "__main__":
    root = Tk()
    application = Student(root)
    root.mainloop()