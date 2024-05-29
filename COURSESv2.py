from tkinter import *
from tkinter import ttk
import tkinter.ttk as ttk
from tkinter import messagebox
import mysql.connector


class SecondPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Information System")
        self.root.geometry("1600x900")
        self.create_course_widgets()
        self.current_frame = None  # To keep track of the current frame
        

        # Database connection setup
        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            port="3306",
            password="",
            database="students"
        )
        self.cursor = self.conn.cursor()

        self.create_second_page()

    def create_course_widgets(self):
        self.fields = ["Course_Code", "Course_Name"]

    def create_second_page(self):
        self.second_page_frame = Frame(self.root, bd=5, relief=RIDGE, bg="#408181")
        self.second_page_frame.pack(fill=BOTH, expand=True)

        title = Label(self.second_page_frame, text="COURSE PAGE", bd=4, relief=RIDGE, font=("Source code", 40, "bold"),
                      bg="#142b39", fg="White")
        title.pack(side=TOP)

        self.detail_frame = Frame(self.second_page_frame, bd=4, relief=RIDGE, bg="Sky Blue")
        self.detail_frame.place(x=20, y=150, width=780, height=420)

        # Add widgets for the second page
        lblInfo = Button(self.second_page_frame, text="LIST OF COURSES", font=("Source code", 20, "bold"), bg="#142b39", fg="White")
        lblInfo.place(x=275, y=90)

        # Frame for course entry and search
        CourseFrame = Frame(self.second_page_frame, bd=4, bg="Sky Blue", relief=RIDGE)
        CourseFrame.place(x=870, y=150, width=630, height=250)

        self.coursecode_label = Label(CourseFrame, text="Course Code:", font=("Arial", 14, "bold"), bg="#142b39", fg="White")
        self.coursecode_label.place(x=20, y=20)
        self.coursecode_entries = Entry(CourseFrame, font=("Arial", 14), bg="white", fg="black")
        self.coursecode_entries.place(x=170, y=20, width=180)

        self.coursetitle_label = Label(CourseFrame, text="Course Title:", font=("Arial", 14, "bold"), bg="#142b39", fg="White")
        self.coursetitle_label.place(x=20, y=70)
        self.coursetitle_entries = Entry(CourseFrame, font=("Arial", 14), bg="white", fg="black")
        self.coursetitle_entries.place(x=170, y=70, width=400)

        # Search frame within the CourseFrame
        SearchFrame = Frame(CourseFrame, bd=4, bg="Sky Blue", relief=RIDGE)
        SearchFrame.place(x=20, y=120, width=590, height=100)

        self.search_entry = Entry(SearchFrame, font=("Arial", 14), bg="white", fg="black")
        self.search_entry.place(x=150, y=20, width=300)

        self.btnSearchData = Button(SearchFrame, text="SEARCH", font=("Source code", 13, "bold"), bg="#142b39", fg="white", height=1, width=12, bd=5, command=self.search_course)
        self.btnSearchData.place(x=20, y=15, width=100)

        # BUTTONS FOR CRUDL
        ButtonFrame = Frame(self.second_page_frame, bd=4, bg="Sky Blue", relief=RIDGE)
        ButtonFrame.place(x=870, y=420, width=630, height=140)

        # Add buttons to ButtonFrame
        self.add_button = Button(ButtonFrame, text="ADD", font=("Source code", 10, "bold"), bg="#142b39", fg="White", command=self.add_course)
        self.add_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        btn2 = Button(ButtonFrame, text="UPDATE", font=("Source code", 10, "bold"), bg="#142b39", fg="White", command=self.edit_course)
        btn2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        btn3 = Button(ButtonFrame, text="DELETE", font=("Source code", 10, "bold"), bg="#142b39", fg="White", command=self.delete_course)
        btn3.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        btn4 = Button(ButtonFrame, text="SEARCH", font=("Source code", 10, "bold"), bg="#142b39", fg="White", command=self.search_course)
        btn4.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Add SAVE and GO BACK buttons
        btn5 = Button(ButtonFrame, text="SAVE", font=("Source code", 10, "bold"), bg="#142b39", fg="White", command=self.save_changes)
        btn5.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        btn6 = Button(ButtonFrame, text="GO BACK", font=("Source code", 10, "bold"), bg="#142b39", fg="White", command=self.return_to_main_page)
        btn6.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # Configure grid options to make buttons fill the frame
        ButtonFrame.grid_columnconfigure(0, weight=1)
        ButtonFrame.grid_columnconfigure(1, weight=1)
        ButtonFrame.grid_columnconfigure(2, weight=1)
        ButtonFrame.grid_rowconfigure(0, weight=1)
        ButtonFrame.grid_rowconfigure(1, weight=1)

        # Create Treeview for course display
        self.tree = ttk.Treeview(self.detail_frame, columns=("Course Code", "Course Name"), show="headings")
        self.tree.heading("Course Code", text="Course Code")
        self.tree.heading("Course Name", text="Course Name")
        self.tree.column("Course Code", width=200)
        self.tree.column("Course Name", width=400)

        # Add vertical scrollbar
        vsb = ttk.Scrollbar(self.detail_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        self.tree.pack(fill="both", expand=True)

        # Load courses into the Treeview
        self.load_courses()
        self.selected_item = None

    def return_to_main_page(self):
        # Destroy the current frame (second page)
        self.second_page_frame.pack_forget()
        self.root

    def edit_course(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a course to edit.")
            return

        # Store the selected item for later use
        self.selected_item = selected_item

        # Extract course information from the selected item
        course_values = self.tree.item(selected_item, "values")
        if not course_values:
            messagebox.showwarning("Warning", "Selected item does not contain course information.")
            return

        # Display course information in entry fields for editing
        self.coursecode_entries.delete(0, END)
        self.coursecode_entries.insert(0, course_values[0])

        self.coursetitle_entries.delete(0, END)
        self.coursetitle_entries.insert(0, course_values[1])

    def clear_entry_fields(self):
        self.coursecode_entries.delete(0, "end")
        self.coursetitle_entries.delete(0, "end")

    def cancel_edit(self):
        self.selected_item = None
        self.clear_entry_fields()

    def save_changes(self):
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select a course to edit.")
            return

        # Retrieve edited values from entry fields
        edited_course_code = self.coursecode_entries.get()
        edited_course_title = self.coursetitle_entries.get()

        # Check if any field is empty
        if edited_course_code == '' or edited_course_title == '':
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        selected_course_code = self.tree.item(self.selected_item, "values")[0]

        # Update Treeview with the edited values
        self.tree.item(self.selected_item, values=(edited_course_code, edited_course_title))

        # Update database with the edited values
        self.update_db(selected_course_code, edited_course_code, edited_course_title)

        self.selected_item = None
        self.clear_entry_fields()

        messagebox.showinfo("Success", "Changes saved successfully!")

    def update_db(self, selected_course_code, edited_course_code, edited_course_title):
        query = "UPDATE course SET Course_Code = %s, Course_Name = %s WHERE Course_Code = %s"
        self.cursor.execute(query, (edited_course_code, edited_course_title, selected_course_code))
        self.conn.commit()

    def load_courses(self):
        # Clear existing rows in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load courses from the database
        query = "SELECT Course_Code, Course_Name FROM course"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def add_course(self):
        course_code = self.coursecode_entries.get()
        course_title = self.coursetitle_entries.get()
        

        # Check if any field is empty
        if course_code == '' or course_title == '':
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        # Check if course code already exists
        if self.check_course(course_code):
            messagebox.showerror("Error", f"Course {course_code} already exists.")
            return

        # Insert into the database
        query = "INSERT INTO course (Course_Code, Course_Name) VALUES (%s, %s)"
        self.cursor.execute(query, (course_code, course_title))
        self.conn.commit()

        # Update Treeview
        self.tree.insert("", "end", values=(course_code, course_title))

        # Clear entry fields
        self.coursecode_entries.delete(0, "end")
        self.coursetitle_entries.delete(0, "end")

        messagebox.showinfo("Success", "Course added successfully!")

    def delete_course(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a course to delete.")
            return

        course_values = self.tree.item(selected_item, "values")
        if not course_values:
            messagebox.showwarning("Warning", "Selected item does not contain course information.")
            return

        course_code = course_values[0]
        self.tree.delete(selected_item)

        self.delete_course_from_db(course_code)

        messagebox.showinfo("Success", f"Course {course_code} deleted successfully!")

    def check_course(self, course_code):
        query = "SELECT COUNT(*) FROM course WHERE Course_Code = %s"
        self.cursor.execute(query, (course_code,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def delete_course_from_db(self, course_code):
        query = "DELETE FROM course WHERE Course_Code = %s"
        self.cursor.execute(query, (course_code,))
        self.conn.commit()

        # Update corresponding course code to "N/A" in the student database
        update_query = "UPDATE students SET Course_Code = 'N/A' WHERE Course_Code = %s"
        self.cursor.execute(update_query, (course_code,))
        self.conn.commit()

    def search_course(self, event=None):
        keyword = self.search_entry.get().lower()

        if not keyword.strip():
            messagebox.showwarning("Warning", "Please enter a keyword to search.")
            return

        # Clear previous selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)

        # Highlight rows matching the search keyword
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if values and any(keyword in value.lower() for value in values):
                self.tree.selection_add(item)


if __name__ == "__main__":
    root = Tk()
    app = SecondPage(root)
    root.mainloop()
