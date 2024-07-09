"""
This below python code script defines a GUI application for managing CO attainment(Course Outcome) records using Python's Tkinter library. The main functionality includes creating and managing student records in a SQLite3 database which is not connected to web.

Key Components:-
1.  Libraries Used:- 
   - Tkinter for the GUI components.
   - SQLite3 for database management.
   - datetime for Year-related operations use in dynamic combobox options for Year.

2.   Attainment Class:- 
   - Initializes the main application window (master/root).
   - Sets the window title and dimensions, this is a scorallable window(main window).
   - Establishes a connection to a SQLite3 database named "Attainment_record.db",for all data read write operations.

3. Database Initialization:
   - Creates all required tables if it does not already exist. This table stores records with there fields.

4. GUI Components:
   - Various Tkinter widgets are used to interact with the user, including canvas, buttons, labels,treeview, and entry fields.

5. Additional Functionality:
   - The script likely includes methods for adding, updating, and displaying student's and exam's records.

This script is designed to be executed as a standalone application for managing course attainment records.

"""

# Note:-                                      <<< MAIN CODE STARTS HERE >>> 
from tkinter  import*
from tkinter  import ttk
from tkinter import Toplevel
import datetime
from tkinter import messagebox
import sqlite3

# Note:- <Main class Attainment>
class Attainment:
    def __init__(self,main_window):
        self.main_window=main_window
        self.main_window.title("Attainment Application")
        self.main_window.geometry("%dx%d+0+0" % (self.main_window.winfo_screenwidth(), self.main_window.winfo_screenheight()))
        defult ='#333333'

# Note:- **************Createing Tables in DataBase with SQLite3 Connection(open)****************
        self.db_connection = sqlite3.connect("Attainment_record.db")
        my_cursor = self.db_connection.cursor()

    # Note:-: TABLE FOR  Student:: Table no 1 
        my_cursor.execute('''
            CREATE TABLE IF NOT EXISTS STUDENT (
                Academic_year VARCHAR(10),
                Student_name TEXT,
                Student_Reg_No INTEGER,
                Semester INTEGER,
                PRIMARY KEY (Student_Reg_No,Academic_year,Semester))''')
                
    # Note:-: TABLE FOR COURSE EXAM:: Table no 2  
        my_cursor.execute('''
            CREATE TABLE IF NOT EXISTS QUESTION_MARK (
                Academic_year VARCHAR(10),
                Semester INTEGER,
                Course_code VARCHAR(50),
                Exam_Name VARCHAR(10), 
                QuCO1 INTEGER,
                QuCO2 INTEGER,
                QuCO3 INTEGER,
                QuCO4 INTEGER,
                QuCO5 INTEGER,
                QuCO6 INTEGER,
                Total_QuCOs INTEGER,
                PRIMARY KEY (Academic_year, Semester, Course_code, Exam_Name)
                FOREIGN KEY (Course_code) REFERENCES Course_Table(course_code)
            )''')

    # Note:-: TABLE FOR EXAM SCORE:: Table no 3 
        my_cursor.execute('''
            CREATE TABLE IF NOT EXISTS ANSWER_MARK  (
                Student_Reg_No INTEGER,
                Course_code VARCHAR(50),
                SCA_No VARCHAR(10),
                Score_CO1 INTEGER,
                Score_CO2 INTEGER,
                Score_CO3 INTEGER,
                Score_CO4 INTEGER,
                Score_CO5 INTEGER,
                Score_CO6 INTEGER,
                Total_ScoreCOs INTEGER,
                PRIMARY KEY (Student_Reg_No,Course_code, SCA_No),
                FOREIGN KEY (Student_Reg_No) REFERENCES STUDENT(Student_Reg_No),
                FOREIGN KEY (Course_code) REFERENCES  Course_Table(Course_code)
            )''')

        # Note:-: TABLE FOR COURSE REGISTER:: Table no 4 
        my_cursor.execute('''
            CREATE TABLE IF NOT EXISTS Course_Table (
                course_code TEXT PRIMARY KEY,
                semester_no INTEGER NOT NULL
            )''')

        # Note:-: TABLE FOR Set Target Levels:: Table no 5
        my_cursor.execute('''
            CREATE TABLE IF NOT EXISTS Target_Variable_Table (
                course_code TEXT PRIMARY KEY,
                internal_target INTEGER DEFAULT 60,
                final_target INTEGER DEFAULT 60,
                overall_target INTEGER DEFAULT 60,
                FOREIGN KEY (course_code) REFERENCES Course_Table(course_code)
                    ON DELETE CASCADE
            )''')

        # Note:-: TABLE FOR to Store Set levels to the Tergets :: Table no 6
        my_cursor.execute('''
            CREATE TABLE IF NOT EXISTS Level_Table (
                course_code TEXT NOT NULL,
                target_type VARCHAR(10) NOT NULL,
                level_0 INTEGER DEFAULT 40,
                level_1 INTEGER DEFAULT 50,
                level_2 INTEGER DEFAULT 60,
                PRIMARY KEY (course_code, target_type),
                CHECK(target_type IN ('internal', 'final', 'overall')),
                FOREIGN KEY (course_code) REFERENCES Course_Table(course_code) ON DELETE CASCADE
            )''')

        # Note:-: TABLE FOR to Store Set WEIGHTS For the Attainment :: Table no 7
        my_cursor.execute('''
            CREATE TABLE IF NOT EXISTS weight_table (
                id INTEGER PRIMARY KEY,
                internal_weight INTEGER  DEFAULT 30,
                external_weight INTEGER  DEFAULT 70
            )''')

        self.db_connection.commit()
        self.db_connection.close()      


# Note:- **************Createing Tables in DataBase with SQLite3 Connection(close)****************
     
# Note:- ************* Button variables for main frame(open)**********************
    # Note:- Variables for DataframeTop**********
        self.AcademicYear    =   StringVar()
        self.Semester        =   IntVar()
        self.CourseCode      =   StringVar()
        self.Exam_Name       =   StringVar()        # Note:- Question CA_no or QCANo 
        self.QuCO1           =   IntVar()
        self.QuCO2           =   IntVar()
        self.QuCO3           =   IntVar()
        self.QuCO4           =   IntVar()
        self.QuCO5           =   IntVar()
        self.QuCO6           =   IntVar()
        self.QuCO6           =   IntVar()
        self.Total_QuCOs     =   IntVar() 
        
    # Note:- DataframeDown**********
        self.StudentName     =   StringVar()
        self.CourseCodeDown  =   StringVar()
        self.StudentIDNO     =   IntVar()
        self.SCANo           =   StringVar()
        self.ScoreCO1        =   IntVar()
        self.ScoreCO2        =   IntVar()
        self.ScoreCO3        =   IntVar()
        self.ScoreCO4        =   IntVar()
        self.ScoreCO5        =   IntVar()
        self.ScoreCO6        =   IntVar()
        self.Total_ScoreCOs  =   IntVar()

# Note:- ***************** Button variables for main frame(close) ********************


# Note:- //////////////////////////// MAIN LABEL (Start) ////////////////////////////////////

    # Note:- Note:[Here a TK Canvas in Use](automaticaly looks for system screen's width and height)
        self.canvas = Canvas(main_window,background='#3D9970',scrollregion = (0,0,self.main_window.winfo_screenwidth(), self.main_window.winfo_screenheight())) # Note:- bg = Olive Green 
        self.canvas.pack(expand = True, fill ='both')

        self.main_frame = Frame(self.canvas,background =  'White')

        # Note:- Add a vertical scrollbar for the canvas
        scrollbar_y_main = Scrollbar(self.canvas, orient=VERTICAL, command=self.canvas.yview, width=20, bg='green', troughcolor='gray', highlightthickness=0)
        scrollbar_y_main.pack(side=RIGHT, fill=Y)

        # Note:- Add a horizontal scrollbar for the canvas
        scrollbar_x_main = Scrollbar(self.canvas, orient=HORIZONTAL, command=self.canvas.xview, width=20, bg='green', troughcolor='gray', highlightthickness=0)
        scrollbar_x_main.pack(side=BOTTOM, fill=X)

        # Note:- Configure the canvas to use the scrollbars
        self.canvas.configure(yscrollcommand=scrollbar_y_main.set, xscrollcommand=scrollbar_x_main.set)


        self.canvas.create_window((0,0),window = self.main_frame,anchor = NW,width = self.main_window.winfo_screenwidth()-18,height= self.main_window.winfo_screenheight()-18)

        self.main_window.bind("<Configure>", lambda event: self.canvas.config(scrollregion=self.canvas.bbox("all")))

# Note:- [[===================================== DATAFRAMES ====================================]]

        Dataframe=Frame(self.main_frame, bd=8, relief=RIDGE)
        Dataframe.place(x=0,y=-10,width=1525,height=365)

        Headtitel=Label(Dataframe,bd=8,relief=RIDGE,text="<<<< COURSE OUTCOME ATTAINMENT >>>>",fg="green", bg="white",font=("times new roman",18,"bold"))
        Headtitel.pack(side=TOP,fill=X)
        
    # Note:- ================= DataframeTop & DataframeDown(start)=====================

        DataframeTop=LabelFrame(Dataframe,bd=6,fg="Red",relief=RIDGE,padx=10,
                                    font=("times new roman",12, "bold"),text=" Course's Exam Details and Maximum Obtainable Marks ")
        DataframeTop.place(x=-8,y=36,width=1525,height=302)
        # Note:- DataframeTop.configure(bg="green")
       
        DataframeDown=LabelFrame(Dataframe,bd=8,fg="Green",relief=RIDGE,padx=10,
                                    font=("times new roman",13, "bold"),text=" Coursewise Student Score Details in Exam ")
        DataframeDown.place(x=-10,y=212,width=1525,height=140)
        # Note:- DataframeDown.configure(bg=defult)

    # Note:- ================== DataframeTop & DataframeDown(end)======================


# Note:- [[===================================== DATAFRAMEs ====================================]]

    # Note:- ****************************  Buttons Frame *********************************
        # Note:- /////////// Student Buttons Frame \\\\\\\\\\
        StudentButtonframe=Frame(self.main_frame, bd=5, relief=RIDGE) 
        StudentButtonframe.place(x=1,y=350,width=1520,height=50)
        # Note:- ********* Course Buttons Frame *********
        CourseButtonframe=Frame(self.main_frame, bd=5, relief=RIDGE) 
        CourseButtonframe.place(x=-1,y=161,width=1520,height=50)
    # Note:- ****************************  Buttons Frame *********************************
    

    # Note:- ****************************** Details frame(open) ******************************
        Detailsframe=Frame(self.main_frame, bd=5, relief=RIDGE,bg=defult) 
        Detailsframe.place(x=-1,y=435,width=1522,height=400)
        # Note:- Two frames for different Treeviews
        self.Frame1 =LabelFrame(Detailsframe, bg="White",text=" Maximum Obtainable Marks in Exams ")
        self.Frame1.place(x=0, y=0, width=1522, height=400)

        self.Frame2 =LabelFrame(Detailsframe, bg="White",text=" Student's Scores in Exams ")
        self.Frame2.place(x=0, y=0, width=1522, height=400)

        # Note:- *******************DataframeTop*****************
        # Note:- ****Academic Year/FIRST****
        lblYear=Label(DataframeTop,text="Academic Year",font=("times new roman",12,"bold"),padx=3,pady=0)
        lblYear.place(x=0,y=6,width=120,height=20)

        comboxYear=ttk.Combobox(DataframeTop,textvariable=self.AcademicYear, font=("times new roman",12,"bold"),width=8, state="readonly")
        # Note:- current_year = datetime.datetime.now().year   
        year_values = [f"{year}-{str(year + 1)[-2:]}" for year in range(datetime.datetime.now().year - 4, datetime.datetime.now().year + 1)]
        comboxYear["values"] = year_values
        comboxYear.place(x=125,y=5,width=80,height=25)

        # Note:- ****Semester/SECOND****
        lblsem=Label(DataframeTop,text="Semester",font=("times new roman",12,"bold"),padx=10,pady=1)
        lblsem.place(x=225,y=6,width=120,height=25)

        comboxSem=ttk.Combobox(DataframeTop,textvariable=self.Semester, font=("times new roman",12,"bold"),width=5,state="readonly")
        comboxSem["values"] = [str(i) for i in range(1, 9)]
        comboxSem.place(x=335,y=6,height=25)


        # Note:- ****Course Code/Third****
        lblCourseCode=Label(DataframeTop,text="Course Code",font=("times new roman",12,"bold"),padx=8,pady=0)
        lblCourseCode.place(x=450,y=6,height=25)

        # Note:- Below code is for a function under function (__init__)
        def update_courses_top():
            conn = sqlite3.connect("Attainment_record.db")
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT course_code FROM Course_Table ORDER BY course_code") 
            course_codes = [row[0] for row in cursor.fetchall()]
            conn.close()
            return course_codes

        # Note:- This variable holds the course codes 
        course_codes = update_courses_top()
        comboxCourseCode=ttk.Combobox(DataframeTop,textvariable=self.CourseCode,postcommand=self.fetch_exam_data,font=("times new roman",10,"bold"),width=25, state="readonly")
        comboxCourseCode["values"] = course_codes
        comboxCourseCode.place(x=560,y=5,height=25)

        # Note:- Binding the Selection Event of the Semester Combobox here
        comboxSem.bind("<<ComboboxSelected>>",update_courses_top)   
        # Note:- It's bind the ComboboxSelected event to the fetch_exam_data function
        comboxCourseCode.bind("<<ComboboxSelected>>", self.fetch_exam_data)

        # Note:- ****CA No/Fourth****
        lblExam_Name=Label(DataframeTop,text="Exam Name",font=("times new roman",12,"bold"),padx=10,pady=1)
        lblExam_Name.place(x=800,y=6,height=25)

        comboxExam_Name=ttk.Combobox(DataframeTop,textvariable=self.Exam_Name, font=("times new roman",12,"bold"),width=25, state="readonly")
        comboxExam_Name["values"] = (" CA 1 ", " CA 2 ", " CA 3 ", " CA 4 ", " Semester End Exam (SEE)")
        comboxExam_Name.place(x=910,y=5,height=25)

        # Note:- *****COs marks in CA************
        lblCAmarks=Label(DataframeTop,bd=2,text="CO-Full Marks in Exam",font=("times new roman",12),padx=0,pady=10)
        lblCAmarks.place(x=-9,y=40,width=1505,height=22)


        # Note:- *********CO 1,2,3,4,5,6**********
        lblCO1=Label(DataframeTop,text="CO 1",font=("times new roman",14,"bold"),padx=0,pady=2)
        lblCO1.place(x=10,y=70,width=50,height=25)
        txtentryCO1=Entry(DataframeTop,textvariable=self.QuCO1, font=("times new roman",12,"bold"),width=4)
        txtentryCO1.place(x=70,y=70,width=50,height=25)

        lblCO2=Label(DataframeTop,text="CO 2",font=("times new roman",14,"bold"),padx=6,pady=2)
        lblCO2.place(x=200,y=70,width=50,height=25)
        txtentryCO2=Entry(DataframeTop,textvariable=self.QuCO2,font=("times new roman",12,"bold"),width=4)
        txtentryCO2.place(x=260,y=70,width=50,height=25)

        lblCO3=Label(DataframeTop,text="CO 3",font=("times new roman",14,"bold"),padx=10,pady=2)
        lblCO3.place(x=390,y=70,width=50,height=25)
        txtentryCO3=Entry(DataframeTop,textvariable=self.QuCO3,font=("times new roman",12,"bold"),width=4)
        txtentryCO3.place(x=450,y=70,width=60,height=25)

        lblCO4=Label(DataframeTop,text="CO 4",font=("times new roman",14,"bold"),padx=20,pady=2)
        lblCO4.place(x=580,y=70,width=50,height=25)
        txtentryCO4=Entry(DataframeTop,textvariable=self.QuCO4,font=("times new roman",12,"bold"),width=4)
        txtentryCO4.place(x=640,y=70,width=60,height=25)

        lblCO5=Label(DataframeTop,text="CO 5",font=("times new roman",14,"bold"),padx=8,pady=2)
        lblCO5.place(x=735,y=70,width=50,height=25)
        txtentryCO5=Entry(DataframeTop,textvariable=self.QuCO5,font=("times new roman",12,"bold"),width=4)
        txtentryCO5.place(x=795,y=70,width=60,height=25)

        lblCO6=Label(DataframeTop,text="CO 6",font=("times new roman",14,"bold"),padx=0,pady=2)
        lblCO6.place(x=920,y=70,width=50,height=25)
        txtentryCO6=Entry(DataframeTop,textvariable=self.QuCO6,font=("times new roman",12,"bold"),width=4)
        txtentryCO6.place(x=980,y=70,width=50,height=25)


        # Note:- It helps user to count the number's Total
        lblTotalQuCOs=Label(DataframeTop,text="Total Marks\nin COs",font=("times new roman",12,"bold"),padx=20,pady=2)
        lblTotalQuCOs.place(x=1080,y=62,width=120,height=45)
        txtentryTotalQuCOs=Label(DataframeTop,textvariable=self.Total_QuCOs,bg="white",fg="Black",font=("times new roman",18,"bold"),padx=20,pady=0)
        txtentryTotalQuCOs.place(x=1200,y=70,width=60,height=25)


    # Note:- *******************DataframeDown*****************
        # Note:- **** COURSE CODE/FIRST****
        lblCourseCode_down=Label(DataframeDown,text="Course Code",font=("times new roman",13,"bold"),padx=1,pady=0)
        lblCourseCode_down.place(x=0,y=5,width=120,height=20)

        # Note:- : Below code is for a function under a function
        def update_courses_down():
            conn = sqlite3.connect("Attainment_record.db")
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT course_code FROM Course_Table ORDER BY course_code") 
            course_codes = [row[0] for row in cursor.fetchall()]
            conn.close()
            # Note:- self.fetch_exam_data()
            return course_codes

        # Note:- :This variable holds the course codes 
        course_codes = update_courses_down()
        comboxCourseCode_down=ttk.Combobox(DataframeDown,textvariable=self.CourseCodeDown,postcommand=self.fetch_score_data,font=("times new roman",12,"bold"),width=35, state="readonly")
        comboxCourseCode_down["values"] = course_codes
        comboxCourseCode_down.place(x=125,y=4,width=180,height=25)

        # Note:- It's bind the ComboboxSelected event to the fetch_exam_data function
        comboxCourseCode_down.bind("<<ComboboxSelected>>",update_courses_down)
        comboxCourseCode_down.bind("<<ComboboxSelected>>",self.fetch_score_data)
        
        # Note:- ****STUDENT ID/SECOND/3rd****
        lblStudentID=Label(DataframeDown,text="Student ID No ",font=("times new roman",13,"bold"),padx=1,pady=1)
        lblStudentID.place(x=335,y=5,width=120,height=25)

        self.student_id_no = StringVar()
        
        # Note:- This function for fetch registration numbers from the STUDENT in the Attainment_record database
        def fetch_registration_numbers_from_database():
            conn = sqlite3.connect("Attainment_record.db")
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT Student_Reg_No FROM STUDENT 
                ORDER BY Academic_year DESC, Semester DESC, Student_Reg_No ASC, Student_name ASC
            ''')
            fetched_registration_numbers = [row[0] for row in cursor.fetchall()]
            conn.close()
            return fetched_registration_numbers

        # Note:- This function for update suggestion list based on input text for registration numbers Combobox
        def update_registration_number_suggestion(event=None):
            fetched_registration_numbers = fetch_registration_numbers_from_database()
            current_text = student_reg_no_entry.get()
            matching_registration_numbers = [str(reg_no) for reg_no in fetched_registration_numbers if str(reg_no).startswith(current_text)]
            student_reg_no_entry["values"] = matching_registration_numbers

        # Note:- Fetch student name based on selected registration number
        def fetch_student_name(reg_no):
            conn = sqlite3.connect("Attainment_record.db")
            cursor = conn.cursor()
            cursor.execute('''
                SELECT Student_name FROM STUDENT WHERE Student_Reg_No = ?
                ORDER BY Academic_year DESC, Semester DESC,Student_Reg_No 
                LIMIT 1
            ''', (reg_no,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else ''

        # Note:- Fetch registration number based on entered student name
        def fetch_registration_number(student_name):
            conn = sqlite3.connect("Attainment_record.db")
            cursor = conn.cursor()
            cursor.execute('''
                SELECT Student_Reg_No FROM STUDENT WHERE Student_name = ?
                ORDER BY Academic_year DESC, Semester DESC
                LIMIT 1
            ''', (student_name,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else ''

        # Note:- Update student name when a registration number is selected
        def update_student_name(event=None):
            selected_id_no = self.student_id_no.get()
            student_name = fetch_student_name(selected_id_no)
            self.student_name.set(student_name)
            update_registration_number_suggestion()

        # Note:- Update registration number when a student name is entered
        def update_registration_number(event=None):
            entered_student_name = self.student_name.get()
            registration_number = fetch_registration_number(entered_student_name)
            self.student_id_no.set(registration_number)
            update_registration_number_suggestion()

        fetched_registration_numbers = fetch_registration_numbers_from_database()

        student_reg_no_entry = ttk.Combobox(DataframeDown, textvariable=self.student_id_no, font=("times new roman", 12, "bold"))
        student_reg_no_entry["values"] = fetched_registration_numbers
        student_reg_no_entry.place(x=465, y=4, width=180,height=25)
        student_reg_no_entry.bind("<KeyRelease>", update_registration_number_suggestion)
        student_reg_no_entry.bind("<<ComboboxSelected>>", update_student_name)
        update_registration_number_suggestion()
       

        # Note:- ****STUDENT NAME/****

        lblStudentname=Label(DataframeDown,text="Student Name ",font=("times new roman",13,"bold"),padx=1,pady=1)
        lblStudentname.place(x=670,y=4,width=120,height=25)
        self.student_name = StringVar()

        student_name_entry = Entry(DataframeDown, textvariable=self.student_name, font=("times new roman", 12, "bold"))
        student_name_entry.place(x=785, y=4, width=215)
        student_name_entry.bind("<KeyRelease>", update_registration_number)

        # Note:- ****Score CA No/4rd****
        
        lblSCAno=Label(DataframeDown,text="Score in Exam",font=("times new roman",13,"bold"),padx=1,pady=1)
        lblSCAno.place(x=1025,y=5,height=25)

        comboxSCAno=ttk.Combobox(DataframeDown,textvariable=self.SCANo, font=("times new roman",12,"bold"),width=25, state="readonly")
        comboxSCAno["values"] = (" CA 1 ", " CA 2 ", " CA 3 ", " CA 4 "," Semester End Exam (SEE)")
        comboxSCAno.place(x=1140,y=4,width= 210,height=25)

        # Note:- *****COs marks in CA************
        lblSCAmarks=Label(DataframeDown,bd=0,relief =RIDGE, text=" CO wise Score in Exam ", fg = "Black", bg ="White",font=("times new roman",12),padx=1,pady=0)
        lblSCAmarks.place(x=-9,y=40,width=1505,height=20)

        # Note:- *********CO 1,2,3,4,5,6**********
        lblCO1=Label(DataframeDown,text="CO 1",font=("times new roman",14,"bold"),padx=1,pady=1)
        lblCO1.place(x=10,y=70,width=50,height=25)
        txtentryCO1=Entry(DataframeDown,textvariable=self.ScoreCO1,font=("times new roman",12,"bold"),width=4)
        txtentryCO1.place(x=70,y=70,width=50,height=25)
        
        lblCO2=Label(DataframeDown,text="CO 2",font=("times new roman",14,"bold"),padx=1,pady=1)
        lblCO2.place(x=200,y=70,width=50,height=25)
        txtentryCO2=Entry(DataframeDown,textvariable=self.ScoreCO2,font=("times new roman",12,"bold"),width=4)
        txtentryCO2.place(x=260,y=70,width=50,height=25)

        lblCO3=Label(DataframeDown,text="CO 3",font=("times new roman",14,"bold"),padx=1,pady=1)
        lblCO3.place(x=390,y=70,width=50,height=25)
        txtentryCO3=Entry(DataframeDown,textvariable=self.ScoreCO3,font=("times new roman",12,"bold"),width=4)
        txtentryCO3.place(x=450,y=70,width=60,height=25)

        lblCO4=Label(DataframeDown,text="CO 4",font=("times new roman",14,"bold"),padx=1,pady=1)
        lblCO4.place(x=580,y=70,width=50,height=25)
        txtentryCO4=Entry(DataframeDown,textvariable=self.ScoreCO4,font=("times new roman",12,"bold"),width=4)
        txtentryCO4.place(x=640,y=70,width=60,height=25)

        lblCO5=Label(DataframeDown,text="CO 5",font=("times new roman",14,"bold"),padx=4,pady=1)
        lblCO5.place(x=735,y=70,width=50,height=25)
        txtentryCO5=Entry(DataframeDown,textvariable=self.ScoreCO5,font=("times new roman",12,"bold"),width=4)
        txtentryCO5.place(x=795,y=70,width=60,height=25)

        lblCO6=Label(DataframeDown,text="CO 6",font=("times new roman",14,"bold"),padx=40,pady=10)
        lblCO6.place(x=920,y=70,width=50,height=25)
        txtentryCO6=Entry(DataframeDown,textvariable=self.ScoreCO6,font=("times new roman",12,"bold"),width=4)
        txtentryCO6.place(x=980,y=70,width=50,height=25)


        lblTotal_ScoreCOs=Label(DataframeDown,text="Total Score\n in COs",font=("times new roman",12,"bold"),padx=2,pady=1)
        lblTotal_ScoreCOs.place(x=1080,y=62,width=120,height=45)
        txtentryTotal_ScoreCOs=Label(DataframeDown,textvariable=self.Total_ScoreCOs,bg="white",fg="Black",font=("times new roman",18,"bold"),padx=2,pady=0)
        txtentryTotal_ScoreCOs.place(x=1200,y=70,width=60,height=25)

    # Note:- ******************************Details frame(end) ******************************

# Note:- ////////////////////////SEARCH BUTTONs///////////////////////
        # Note:- Showall button
        # Note:- ButtonShowall=Button(StudentButtonframe,command=self.fetch_Examwise_data,text="Show all",bd=5,bg="grey",fg="white",font=("times new roman",12,"bold"),width=18,height=1,padx=20)        
        # Note:- ButtonShowall.grid(row=0,column=8)

   
# Note:- ====================================== BUTTONs =========================================
    # Note:- ============= Course BUTTONs TOP ==============
        Course_ButtonAddnew = Button(CourseButtonframe, command=self.add_new_course_marks, text="Add Exam Detail", bd=5, bg="#696969", fg="White", font=("times new roman", 12, "bold"), width=20, height=1, padx=15)
        Course_ButtonAddnew.pack(side='left', fill='x',expand =True)

        Course_ButtonUpdate = Button(CourseButtonframe, command=self.update_existing_course_marks, text="Update Exam Detail", bd=5, bg="#696969", fg="White", font=("times new roman", 12, "bold"), width=20, height=1, padx=15)
        Course_ButtonUpdate.pack(side='left', fill='x',expand =True)

        Course_ButtonDelete = Button(CourseButtonframe, command=self.delete_course_marks, text="Remove Exam Detail", bd=5, bg="#696969", fg="White", font=("times new roman", 12, "bold"), width=20, height=1, padx=15)
        Course_ButtonDelete.pack(side='left', fill='x',expand =True)

        Course_ButtonClear = Button(CourseButtonframe, command=self.Clear_marks, text=" Clear ", bd=5, bg="#696969", fg="White", font=("times new roman", 12, "bold"), width=20, height=1, padx=1)
        Course_ButtonClear.pack(side='left', fill='x',expand =True)

        Course_ButtonExams = Button(CourseButtonframe, command=self.show_frame1, text="View Exam", bd=5, bg="#696969", fg="White", font=("times new roman", 12, "bold"), width=22, height=1, padx=1)
        Course_ButtonExams.pack(side='left', fill='x',expand =True)

        Course_ButtonReport = Button(CourseButtonframe, command=self.Report, text="Report", bd=5, bg="black", fg="White", font=("times new roman", 12, "bold"), width=22, height=1, padx=1)
        Course_ButtonReport.pack(side='left', fill='x',expand =True)

        Course_ButtonSettings = Button(CourseButtonframe, command=self.open_settings, text="Settings", bd=5, bg="black", fg="White", font=("times new roman", 12, "bold"), width=22, height=1, padx=1)
        Course_ButtonSettings.pack(side='left', fill='x',expand =True)


     # Note:- ============ Student BUTTONs DOWN=============
        Student_ButtonAddnew = Button(StudentButtonframe, command=self.add_new, text="Add Score", bd=5, bg="#696969", fg="White", font=("times new roman", 12, "bold"))
        Student_ButtonAddnew.pack(side=LEFT, fill='x', expand=True)

        Student_ButtonUpdate = Button(StudentButtonframe, command=self.update_student_marks, text="Update Score", bd=5, bg="#696969", fg="White", font=("times new roman", 12, "bold"))
        Student_ButtonUpdate.pack(side=LEFT, fill='x', expand=True)

        Student_ButtonDelete = Button(StudentButtonframe, command=self.delete_student_marks, text=" Delete Score", bd=5, bg="#696969", fg="White", font=("times new roman", 12, "bold"))
        Student_ButtonDelete.pack(side=LEFT, fill='x', expand=True)

        Student_ButtonClear = Button(StudentButtonframe, command=self.clear_Student_scores, text="Clear", bd=5, bg="#696969", fg="White", font=("times new roman", 12, "bold"))
        Student_ButtonClear.pack(side=LEFT, fill='x', expand=True)
        
        Student_ButtonScore = Button(StudentButtonframe, command=self.show_frame2, text="View Scores", bd=5, bg="#696969", fg="White", font=("times new roman", 12, "bold"))
        Student_ButtonScore.pack(side=LEFT, fill='x', expand=True)

        Student_ButtonExit = Button(StudentButtonframe, command=self.Exit, text="Exit", bd=5, bg="Gray", fg="White", font=("times new roman", 12, "bold"))
        Student_ButtonExit.pack(side=LEFT, fill='x', expand=True)


        # Note:- # Note:- add more buttons below here if needed--
    
    # Note:- //////////////////////////Main Window Scrollbar/////////////////////////////////////////

    # Note:- ==================   SCROLLBAR  ====================
    # Note:- ============ TREEVIEW TABLES DATA ===========

        # Note:- Add Treeview to Frame1 (Marks Tree)
        Scrollbar_x1 = ttk.Scrollbar(self.Frame1, orient=HORIZONTAL)
        Scrollbar_y1 = ttk.Scrollbar(self.Frame1, orient=VERTICAL)
        self.tree1 = ttk.Treeview(self.Frame1, columns=("Exam", "CO1", "CO2", "CO3", "CO4", "CO5", "CO6", "Total Marks"), xscrollcommand=Scrollbar_x1.set, yscrollcommand=Scrollbar_y1.set)

        Scrollbar_y1.pack(side=RIGHT, fill=Y)
        Scrollbar_y1.config(command=self.tree1.yview)

        self.tree1.heading("Exam", text = "Exam")
        self.tree1.heading("CO1" , text = "CO1" )
        self.tree1.heading("CO2" , text = "CO2" )
        self.tree1.heading("CO3" , text = "CO3" )
        self.tree1.heading("CO4" , text = "CO4" )
        self.tree1.heading("CO5" , text = "CO5" )
        self.tree1.heading("CO6" , text = "CO6" )
        self.tree1.heading("Total Marks", text="Total Marks")

        self.tree1["show"] = "headings"

        self.tree1.column("Exam", width = 100)
        self.tree1.column("CO1" , width = 50 )
        self.tree1.column("CO2" , width = 50 )
        self.tree1.column("CO3" , width = 50 )
        self.tree1.column("CO4" , width = 50 )
        self.tree1.column("CO5" , width = 50 )
        self.tree1.column("CO6" , width = 50 )
        self.tree1.column("Total Marks", width=100)

        self.tree1.pack(fill=BOTH, expand=True)
        

        # Note:- Add Treeview to Frame2 (Student Tree)
        Scrollbar_x2 = ttk.Scrollbar(self.Frame2, orient=HORIZONTAL)
        Scrollbar_y2 = ttk.Scrollbar(self.Frame2, orient=VERTICAL)
        self.tree2 = ttk.Treeview(self.Frame2, columns=("Student Name", "STUDENT ID","Exam", "CO1", "CO2", "CO3", "CO4", "CO5", "CO6", "Total Marks",), xscrollcommand=Scrollbar_x2.set, yscrollcommand=Scrollbar_y2.set)

        Scrollbar_y2.pack(side=RIGHT, fill=Y)
        Scrollbar_y2.config(command=self.tree2.yview)

        self.tree2.heading("Student Name", text="Student Name")
        self.tree2.heading("STUDENT ID", text="STUDENT ID")
        self.tree2.heading("Exam", text = "Exam")
        self.tree2.heading("CO1",  text = "CO1" )
        self.tree2.heading("CO2",  text = "CO2" )
        self.tree2.heading("CO3",  text = "CO3" )
        self.tree2.heading("CO4",  text = "CO4" )
        self.tree2.heading("CO5",  text = "CO5" )
        self.tree2.heading("CO6",  text = "CO6" )
        self.tree2.heading("Total Marks", text="Total Marks")
   

        self.tree2["show"] = "headings"

        self.tree2.column("Student Name", width = 70)
        self.tree2.column("STUDENT ID",   width = 70)
        self.tree2.column("Exam", width = 70)
        self.tree2.column("CO1" , width = 15 )
        self.tree2.column("CO2" , width = 15 )
        self.tree2.column("CO3" , width = 15 )
        self.tree2.column("CO4" , width = 15 )
        self.tree2.column("CO5" , width = 15 )
        self.tree2.column("CO6" , width = 15 )
        self.tree2.column("Total Marks", width = 25)

        self.show_frame1()
        self.tree2.pack(fil=BOTH, expand=True)

        self.tree1.bind("<ButtonRelease-1>",self.get_exam_cursor)
        self.tree2.bind("<ButtonRelease-1>",self.get_score_cursor)

        # Note:- Calling functions
        self.fetch_exam_data()
        self.fetch_score_data()

# Note:- //////////////////////////// MAIN LABEL (End) ////////////////////////////////////

# Note:-   =======================  Functinality Declration  =========================      
# Note:- *****************TotalQuCOs Calculation*******************************
        # Note:- Attach the update_total_qucos function to the trace method of each QuCO variable
        self.QuCO1.trace("w", self.update_total_qucos)
        self.QuCO2.trace("w", self.update_total_qucos)
        self.QuCO3.trace("w", self.update_total_qucos)
        self.QuCO4.trace("w", self.update_total_qucos)
        self.QuCO5.trace("w", self.update_total_qucos)
        self.QuCO6.trace("w", self.update_total_qucos)

        # Note:- Initialize Total_QuCOs
        self.update_total_qucos()

    # Note:- Define a function to update the total sum of QuCOs
    def update_total_qucos(self, *args):
        total_qucos = self.QuCO1.get() + self.QuCO2.get() + self.QuCO3.get() + self.QuCO4.get() + self.QuCO5.get() + self.QuCO6.get()
        self.Total_QuCOs.set(total_qucos)
        self.fetch_exam_data()
        # Note:- Attach the update_total_qucos function to the trace method of each QuCO variable
        self.ScoreCO1.trace("w", self.update_total_scorecos)
        self.ScoreCO2.trace("w", self.update_total_scorecos)
        self.ScoreCO3.trace("w", self.update_total_scorecos)
        self.ScoreCO4.trace("w", self.update_total_scorecos)
        self.ScoreCO5.trace("w", self.update_total_scorecos)
        self.ScoreCO6.trace("w", self.update_total_scorecos)

        # Note:- Initialize Total_QuCOs
        self.update_total_scorecos()
# Note:- ****************************************************************************
    
    # Note:- Define a function to update the total sum of QuCOs
    def update_total_scorecos(self, *args):
       # Note:- Get the values of ScoreCOs
        scorecos_values = [self.ScoreCO1.get(), self.ScoreCO2.get(), self.ScoreCO3.get(), self.ScoreCO4.get(), self.ScoreCO5.get(), self.ScoreCO6.get()]
        
        # Note:- Get the values of QuCOs
        # Note:- qucos_values = [self.QuCO1.get(), self.QuCO2.get(), self.QuCO3.get(), self.QuCO4.get(), self.QuCO5.get(), self.QuCO6.get()]

        # Note:- Check if ScoreCO is greater than QuCO for each CO
        # Note:- warning_message = ""
        # Note:- for i in range(6):
        # Note:-     if scorecos_values[i] > qucos_values[i]:
        # Note:-         warning_message = f"Warning: Score of CO{i} is greater than Maximum of CO{i}.\n"
        # Note:-     break

        # Note:- # Note:- Update the Total_ScoreCOs
        total_scorecos = sum(scorecos_values)
        self.Total_ScoreCOs.set(total_scorecos)
        
        # Note:- if warning_message:
        # Note:-      # Note:- Display warning message box only if it hasn't been shown before
        # Note:-     if not getattr(self, 'warning_shown', False):
        # Note:-         self.warning_shown = True
        # Note:-         messagebox.showwarning("Warning", warning_message)
        # Note:-     else:
        # Note:-         # Note:- Reset the flag to allow the warning to be shown again if conditions persist
        # Note:-         self.warning_shown = False

        
        self.fetch_score_data()

    def show_frame1(self):
        self.fetch_exam_data()
        self.Frame1.place(x=0, y=0, width=1525, height=400)
        self.Frame2.place_forget()

    def show_frame2(self):
        self.fetch_score_data()
        self.Frame2.place(x=0, y=0, width=1525, height=400)
        self.Frame1.place_forget()
        self.fetch_score_data()

# Note:-   ================== SQL-Lite -> write operations=================
    # Note:- Course details and marks details Adding function

    def insert_new_course_ca_marks_data(self, academic_year, semester, course_code, exam_name, quco1, quco2, quco3, quco4, quco5, quco6,totalQuCOs):
        conn = sqlite3.connect('Attainment_record.db')
        my_cursor = conn.cursor()

        try:
            # Note:- Insert data into the QUESTION_MARK table
            my_cursor.execute('''
                INSERT INTO QUESTION_MARK (
                    Academic_year,
                    Semester,
                    Course_code,
                    Exam_Name,
                    QuCO1,
                    QuCO2,
                    QuCO3,
                    QuCO4,
                    QuCO5,
                    QuCO6,
                    Total_QuCOs
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                academic_year,
                semester,
                course_code,
                exam_name,
                quco1,
                quco2,
                quco3,
                quco4,
                quco5,
                quco6,
                totalQuCOs,
            ))
            conn.commit()
            messagebox.showinfo("Data Entry", "Course Marks and Details added successfully!")

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("Error", f"Duplicate entry: Academic year '{academic_year}', Semester '{semester}', Course '{course_code}', This Exam '{exam_name}' already exists.")
            else:
                messagebox.showerror("Error", f"Error inserting data: {e}")
        
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")
        
        finally:
            conn.close()
            
    def add_new_course_marks(self):
        # Note:- Example assuming we are getting data from tkinter widgets
        academic_year = self.AcademicYear.get()
        semester = self.Semester.get()
        course_code = self.CourseCode.get()
        exam_name = self.Exam_Name.get()
        quco1 = self.QuCO1.get()
        quco2 = self.QuCO2.get()
        quco3 = self.QuCO3.get()
        quco4 = self.QuCO4.get()
        quco5 = self.QuCO5.get()
        quco6 = self.QuCO6.get()
        totalQuCOs=self.Total_QuCOs.get()

        if (academic_year == "" or semester == "" or course_code == "" or exam_name == "" or
            not any([quco1, quco2, quco3, quco4, quco5, quco6])):
            messagebox.showerror("Error", f"Please fill in all required fields: \n\u2022 Academic Year,\n\u2022 Semester,\n\u2022 Course Code,\n\u2022 Exam Name,\n\u2022 All QuCOs")
            
        else:
            self.insert_new_course_ca_marks_data(
                academic_year,
                semester,
                course_code,
                exam_name,
                quco1,
                quco2,
                quco3,
                quco4,
                quco5,
                quco6,
                totalQuCOs
            )
    # Note:- > Course details and marks details Update function ///////////////////////////
    def update_existing_course_marks(self):
        # Note:- Example assuming we are getting data from tkinter widgets
        academic_year = self.AcademicYear.get()
        semester = self.Semester.get()
        course_code = self.CourseCode.get()
        exam_name = self.Exam_Name.get()
        quco1 = self.QuCO1.get()
        quco2 = self.QuCO2.get()
        quco3 = self.QuCO3.get()
        quco4 = self.QuCO4.get()
        quco5 = self.QuCO5.get()
        quco6 = self.QuCO6.get()
        totalQuCOs=self.Total_QuCOs.get()
        # Note:- Check for QuCO is filled or not filled
        if (academic_year == "" or semester == "" or course_code == "" or exam_name == "" or
            not any([quco1, quco2, quco3, quco4, quco5, quco6])):
            messagebox.showerror("Error", f"Please fill in all required fields: \n\u2022 Academic Year,\n\u2022 Semester,\n\u2022 Course Code,\n\u2022 Exam Name,\n\u2022 All QuCOs")
            return
        # Note:- Update data in the QUESTION_MARK table
        try:
            conn = sqlite3.connect('Attainment_record.db')
            my_cursor = conn.cursor()

            my_cursor.execute('''
                UPDATE QUESTION_MARK
                SET
                    QuCO1 = ?,
                    QuCO2 = ?,
                    QuCO3 = ?,
                    QuCO4 = ?,
                    QuCO5 = ?,
                    QuCO6 = ?,
                    Total_QuCOs =?
                WHERE
                    Academic_year = ? AND
                    Semester = ? AND
                    Course_code = ? AND
                    Exam_Name = ?
            ''', (
                quco1,
                quco2,
                quco3,
                quco4,
                quco5,
                quco6,
                totalQuCOs,
                academic_year,
                semester,
                course_code,
                exam_name
            ))
            conn.commit()
            if my_cursor.rowcount == 0:
                messagebox.showwarning("Update", "No records found to update.")
            else:
                self.fetch_score_data()   # Note:- Refresh row's data in the details frame
                messagebox.showinfo("Data Update", "CA-Course marks updated successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error updating data in QUESTION_MARK table: {e}")
        finally:
            conn.close() 

    def delete_course_marks(self):
        # Note:- Example assuming we are getting data from tkinter widgets
        academic_year = self.AcademicYear.get()
        semester = self.Semester.get()
        course_code = self.CourseCode.get()
        exam_name = self.Exam_Name.get()

        # Note:- Check if all required fields are filled
        if academic_year == "" or semester == "" or course_code == "" or exam_name == "":
            messagebox.showerror("Error", f"Please fill in all required fields: \n\u2022 Academic Year,\n\u2022 Semester,\n\u2022 Course Code,\n\u2022 Exam Name No")
            return

        # Note:- Confirm deletion
        confirm = messagebox.askyesno("Delete", "Are we sure we want to delete this course mark record?")
        if not confirm:
            return

        # Note:- Delete data from the QUESTION_MARK table
        try:
            conn = sqlite3.connect('Attainment_record.db')
            my_cursor = conn.cursor()

            my_cursor.execute('''
                DELETE FROM QUESTION_MARK
                WHERE
                    Academic_year = ? AND
                    Semester = ? AND
                    Course_code = ? AND
                    Exam_Name = ?
            ''', (
                academic_year,
                semester,
                course_code,
                exam_name
            ))

            conn.commit()

            if my_cursor.rowcount == 0:
                messagebox.showwarning("Delete", "No records found to delete.")
            else:
                self.fetch_data()   # Note:- Refresh row's data in the details frame
                messagebox.showinfo("Delete", "CA-Course mark record deleted successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error deleting data in QUESTION_MARK table: {e}")
        finally:
            conn.close()

    # Note:- Question Mark Tables
    def Clear_marks(self):
        # Note:- Clear all QuCO input fields by setting their values to empty strings
        self.QuCO1.set(0)
        self.QuCO2.set(0)
        self.QuCO3.set(0)
        self.QuCO4.set(0)
        self.QuCO5.set(0)
        self.QuCO6.set(0)
        self.Exam_Name.set("")

# Note:- ///////////////////////////////////////////////////////////////////////////////////////////

# Note:- ///////////////////////////////////////////////////////////////////////////////////////////

    def insert_data(self, student_id_no, course_code, sca_no, score_co1, score_co2, score_co3, score_co4, score_co5, score_co6, total_score_cos):
        conn = sqlite3.connect('Attainment_record.db')
        my_cursor = conn.cursor()

        try:
            # Note:- Insert data into the ANSWER_MARK table
            my_cursor.execute('''
                INSERT INTO ANSWER_MARK (
                    Student_Reg_No,
                    Course_code,
                    SCA_No,
                    Score_CO1,
                    Score_CO2,
                    Score_CO3,
                    Score_CO4,
                    Score_CO5,
                    Score_CO6,
                    Total_ScoreCOs
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                student_id_no,
                course_code,
                sca_no,
                score_co1,
                score_co2,
                score_co3,
                score_co4,
                score_co5,
                score_co6,
                total_score_cos
            ))
            conn.commit()
            self.fetch_score_data()
            messagebox.showinfo("Data Entry", "Data has been inserted successfully!")

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("Error", "Duplicate entry detected.")
            elif "FOREIGN KEY constraint failed" in str(e):
                messagebox.showerror("Error", "Foreign key constraint failed. Ensure all referenced data exists.")
            else:
                messagebox.showerror("Error", f"Error inserting data: {e}")
                print("debraj")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")
        finally:
            conn.close()

    def add_new(self):
        if (self.student_id_no.get() == "" or self.CourseCodeDown.get() == "" or 
            self.SCANo.get() == "" or not any([self.ScoreCO1.get(), self.ScoreCO2.get(), self.ScoreCO3.get(), self.ScoreCO4.get(), self.ScoreCO5.get(), self.ScoreCO6.get()])):
            messagebox.showerror("Error", "Please fill in all required fields: \n\u2022 Student ID No,\n\u2022 Course Code,\n\u2022 SCA No,\n\u2022 All Scores")
        else:
            self.insert_data(
                self.student_id_no.get(),
                self.CourseCodeDown.get(),
                self.SCANo.get(),
                self.ScoreCO1.get(),
                self.ScoreCO2.get(),
                self.ScoreCO3.get(),
                self.ScoreCO4.get(),
                self.ScoreCO5.get(),
                self.ScoreCO6.get(),
                self.Total_ScoreCOs.get()  
            )

    def update_student_marks(self):
        conn = sqlite3.connect('Attainment_record.db')
        my_cursor = conn.cursor()

        try:
            # Note:- Update data in the ANSWER_MARK table
            my_cursor.execute('''
                UPDATE ANSWER_MARK
                SET
                    Score_CO1 = ?,
                    Score_CO2 = ?,
                    Score_CO3 = ?,
                    Score_CO4 = ?,
                    Score_CO5 = ?,
                    Score_CO6 = ?,
                    Total_ScoreCOs = ?
                WHERE
                    Student_Reg_No = ? AND
                    Course_code = ? AND
                    SCA_No = ?
            ''', (
                self.ScoreCO1.get(),
                self.ScoreCO2.get(),
                self.ScoreCO3.get(),
                self.ScoreCO4.get(),
                self.ScoreCO5.get(),
                self.ScoreCO6.get(),
                self.Total_ScoreCOs.get(),
                self.student_id_no.get(),
                self.CourseCodeDown.get(),
                self.SCANo.get()
            ))
            conn.commit()
            if my_cursor.rowcount == 0:
                messagebox.showwarning("Update", "No records found to update.")
            else:
                self.fetch_score_data()
                messagebox.showinfo("Data Update", "Student marks updated successfully!")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error updating data: {e}")
        finally:
            conn.close() 
            # Note:- self.fetch_data()

    def fetch_exam_data(self, event=None):
        conn = sqlite3.connect('Attainment_record.db')
        my_cursor = conn.cursor()
        my_cursor.execute('''
        SELECT Exam_Name, QuCO1, QuCO2, QuCO3, QuCO4, QuCO5, QuCO6, Total_QuCOs 
        FROM QUESTION_MARK 
        WHERE Academic_year = ? AND Semester = ? AND Course_code = ? 
        ORDER BY Exam_Name
    ''', (
        self.AcademicYear.get(),
        self.Semester.get(),
        self.CourseCode.get(),
        # Note:- self.Exam_Name.get() and add  AND Exam_Name = ?
    ))
        rows=my_cursor.fetchall()
        
        if len(rows)!=0:
            self.tree1.delete( * self.tree1.get_children())
            for i in rows:
                self.tree1.insert("",END,values=i)
            conn.commit()
        conn.close() 

# Note:- Note: This is a dynamic sql quary so that the function can work with differnt sceanarios(multi provides functionality)
    def fetch_score_data(self, event=None):
        conn = sqlite3.connect('Attainment_record.db')
        my_cursor = conn.cursor()

        base_query = '''
        SELECT
            COALESCE(s.Student_name, 'None') AS Student_name,
            a.Student_Reg_No,
            a.SCA_No,
            a.Score_CO1,
            a.Score_CO2,
            a.Score_CO3,
            a.Score_CO4,
            a.Score_CO5,
            a.Score_CO6,
            a.Total_ScoreCOs
        FROM
            ANSWER_MARK a
        LEFT JOIN
            STUDENT s ON s.Student_Reg_No = a.Student_Reg_No
        WHERE
            a.Course_code = ?
        '''

        filters = []
        params = [self.CourseCodeDown.get()]

        # Note:- Check if Student_Reg_No is provided
        student_ids_no = self.student_id_no.get()
        if student_ids_no:
            filters.append('a.Student_Reg_No = ?')
            params.append(student_ids_no)

        # Note:- Check if SCA_No is provided
        sca_no = self.SCANo.get()
        if sca_no:
            filters.append('a.SCA_No = ?')
            params.append(sca_no)

        # Note:- Apply filters to the base query if any
        if filters:
            base_query += ' AND ' + ' AND '.join(filters)

        base_query += ' ORDER BY s.Student_name, a.Student_Reg_No, a.SCA_No'

        my_cursor.execute(base_query, tuple(params))
        rows = my_cursor.fetchall()

        if rows:
            self.tree2.delete(*self.tree2.get_children())
            for row in rows:
                self.tree2.insert("", END, values=row)
            conn.commit()

        conn.close()


# Note:- Note: This is a dynamic sql quary so that the function can work with differnt sceanarios(multi provides functionality)
    def fetch_Examwise_data(self, event=None):
        conn = sqlite3.connect('Attainment_record.db')
        my_cursor = conn.cursor()

        base_query = '''
        SELECT
            COALESCE(s.Student_name, 'None') AS Student_name,
            a.Student_Reg_No,
            a.SCA_No,
            a.Score_CO1,
            a.Score_CO2,
            a.Score_CO3,
            a.Score_CO4,
            a.Score_CO5,
            a.Score_CO6,
            a.Total_ScoreCOs
        FROM
            ANSWER_MARK a
        LEFT JOIN
            STUDENT s ON s.Student_Reg_No = a.Student_Reg_No
        WHERE
            a.SCA_No = ?
        '''

        params = [self.SCANo.get()]

        # Note:- Optional Course Code filtering
        course_code = self.CourseCodeDown.get()
        if course_code:
            base_query += ' AND a.Course_code = ?'
            params.append(course_code)

        base_query += ' ORDER BY s.Student_name, a.Student_Reg_No, a.SCA_No'

        my_cursor.execute(base_query, params)
        rows = my_cursor.fetchall()

        if rows:
            self.tree2.delete(*self.tree2.get_children())
            for row in rows:
                self.tree2.insert("", END, values=row)
            conn.commit()

        conn.close()


    # Note:- For treeview 1 values
    def get_exam_cursor(self, event=""):
        cursor_row = self.tree1.focus()
        content = self.tree1.item(cursor_row)
        row = content["values"]

        if row:
            self.Exam_Name.set(row[0]) 
            self.QuCO1.set(row[1])      
            self.QuCO2.set(row[2])      
            self.QuCO3.set(row[3])      
            self.QuCO4.set(row[4])      
            self.QuCO5.set(row[5])      
            self.QuCO6.set(row[6])

    # Note:- For treeview 2 values
    def get_score_cursor(self,event=""):
        cursor_row = self.tree2.focus()
        content = self.tree2.item(cursor_row)
        row=content["values"]

        if row:
            self.SCANo.set   (row[2]) 
            self.ScoreCO1.set(row[3])      
            self.ScoreCO2.set(row[4])      
            self.ScoreCO3.set(row[5])      
            self.ScoreCO4.set(row[6])      
            self.ScoreCO5.set(row[7])      
            self.ScoreCO6.set(row[8])
        

    def delete_student_marks(self):
        conn = sqlite3.connect('Attainment_record.db')
        my_cursor = conn.cursor()

        try:
            # Note:- Delete data from the ANSWER_MARK table
            my_cursor.execute('''
                DELETE FROM ANSWER_MARK
                WHERE
                    Student_Reg_No = ? AND
                    Course_code = ? AND
                    SCA_No = ?
            ''', (
                self.student_id_no.get(),
                self.CourseCodeDown.get(),
                self.SCANo.get()
            ))
            conn.commit()
            if my_cursor.rowcount == 0:
                messagebox.showwarning("Delete", "No records found to delete.")
            else:
                self.fetch_exam_data()   # Note:- Refresh row's data in the details frame
                messagebox.showinfo("Data Delete", "Student marks deleted successfully!")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error deleting data: {e}")
        finally:
            conn.close()
 
        self.fetch_score_data()
    

    def clear_Student_scores(self):
        self.ScoreCO1.set(0)
        self.ScoreCO2.set(0)
        self.ScoreCO3.set(0)
        self.ScoreCO4.set(0)
        self.ScoreCO5.set(0)
        self.ScoreCO6.set(0)
        self.SCANo.set("")
        self.student_name.set("")
        # Note:- self.StudentIDNO.set("")



# Note:--------------------<<[ THIS FUNCTION HELPS TO CALL TOPLEVEL WINDOW of the REPORT function ]>>--------------------
# Note:- In this function we can generate attainment report for the course 
    def Report(self):
        self.Report_window = Toplevel(self.main_window)
        self.Report_window.title("Report")
        self.Report_window.geometry("1025x980+240+0")

        # Note:- Add a button frame for buttons
        Main_report_frame = Frame(self.Report_window, bd=4, bg="white", relief=RIDGE)
        Main_report_frame.place(x=2, y=2, width=1025, height=880)

        Main_report_button_frame = Frame(Main_report_frame, bd=5, bg="white", relief=RIDGE)
        Main_report_button_frame.place(x=-1, y=-1, width=1020, height=35)


        # Note:- Attainment Button
        report_attainment_button = Button(Main_report_button_frame, text="CO-Attainment", command=self.show_attainment_frame, bd=2, bg='gray', width=20)
        report_attainment_button.pack(side=LEFT, padx=1, pady=0)

        # Note:- # Note:- CO-PO mapping Button # Note:-uncomment the below button's code if use CO-PO mapping in future
        # Note:- report_copo_mapping_button = Button(Main_report_button_frame, text="CO-PO mapping", command=self.show_copo_mapping_frame, bd=2, bg='gray', width=20)
        # Note:- report_copo_mapping_button.pack(side=LEFT, padx=1, pady=0)

        # Note:- Exit Button for report window
        report_exit_button = Button(Main_report_button_frame, text="Exit Report", command=self.exit_report_window, bd=2, bg='gray', width=20)
        report_exit_button.pack(side=LEFT, padx=1, pady=0)

        # Note:- Bind keyboard shortcuts--
        self.Report_window.bind('<Alt-Shift-A>', lambda event: self.show_attainment_frame())
        self.Report_window.bind('<Alt-Shift-E>', lambda event: self.exit_report_window())
        
        # Note:- Create a Frame for holding entry fields and buttons (Attainment Frame)
        self.report_attainment_frame1 = Frame(Main_report_frame, bd=5, bg="White", relief=RIDGE)
        self.report_attainment_frame1.place(x=0, y=35, width=1020, height=810)

    
# Note:- : Treeview Frame under the report_attainment_frame1 FRAME//
        # Note:- self.attainment_treeview_Frame = Frame(self.report_attainment_frame1, bd=5, bg="White", relief=RIDGE)
        # Note:- self.attainment_treeview_Frame.place(x=1, y=100, width=1012, height=180)


    # Note:- Example Entry field within report attainment frame
        internal_target_label = Label(self.report_attainment_frame1, text="Course Attainment Result of", font=("times new roman", 15, ),bg="White")
        internal_target_label.place(x=0, y=7)

# Note:- :  ALL Entry Fields for the Report Generator frame i.e. report attainment frame1 //

        # Note:- ****ReportAcademic Year/FIRST****
        ReportlblYear=Label(self.report_attainment_frame1,bg="white",text="Academic Year",font=("times new roman",12,"bold"),padx=2,pady=0)
        ReportlblYear.place(x=170, y=45)

        self.report_attainment_year = StringVar()
        report_comboxYear=ttk.Combobox(self.report_attainment_frame1,textvariable=self.report_attainment_year, font=("times new roman",12,"bold"),width=8, state="readonly")

        report_year_values = [f"{year}-{str(year + 1)[-2:]}" for year in range(datetime.datetime.now().year - 4, datetime.datetime.now().year + 1)]
        report_comboxYear["values"] = report_year_values
        report_comboxYear.place(x=285, y=45, width=80)

        # Note:- ****Semester/SECOND****
        Reportlblsem=Label(self.report_attainment_frame1,bg="white",text="Semester",font=("times new roman",12,"bold"),padx=1,pady=1)
        Reportlblsem.place(x=375, y=45)

        self.report_attainment_semester = StringVar()
        
        report_comboxSem = ttk.Combobox(self.report_attainment_frame1, textvariable=self.report_attainment_semester, font=("times new roman", 12, "bold"), state="readonly")
        report_comboxSem["values"] = [str(i) for i in range(1, 9)]
        report_comboxSem.place(x=445, y=45, width=50)

         # Note:- ****Course Code/Third****
        Report_lblCourseCode=Label(self.report_attainment_frame1,bg="white",text="Course Code",font=("times new roman",12,"bold"),padx=8,pady=0)
        Report_lblCourseCode.place(x=520, y=45, width=90)

        self.report_attainment_course_code = StringVar()

        def update_report_courses_top():
            conn = sqlite3.connect("Attainment_record.db")
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT course_code FROM Course_Table ORDER BY course_code") 
            course_codes = [row[0] for row in cursor.fetchall()]
            conn.close()
            return course_codes

        # Note:- This variable holds the course codes 
        report_course_codes = update_report_courses_top()
        report_comboxCourseCode=ttk.Combobox(self.report_attainment_frame1,textvariable=self.report_attainment_course_code,postcommand=self.fetch_exam_data,font=("times new roman",12,"bold"), state="readonly") # Note:- postcommand function is not in use
        report_comboxCourseCode["values"] = report_course_codes
        report_comboxCourseCode.place(x=615,y=45, width=180,height=25)
        
        # Note:- Binding the Selection Event of the Semester Combobox here
        # Note:- report_comboxSem.bind("<<ComboboxSelected>>",update_report_courses_top)

        Report_attainment_percentage=Label(self.report_attainment_frame1,bg="white",text="Attainment Percentage",font=("times new roman",12,"bold"),padx=1,pady=0)
        Report_attainment_percentage.place(x=3, y=95)

        Report_attainment_level=Label(self.report_attainment_frame1,bg="white",text="Attainment Level",font=("times new roman",12,"bold"),padx=1,pady=0)
        Report_attainment_level.place(x=3, y=118)
    # Note:- ><><><><><><><><><><><>< Student Button ><><><><><><><><><><><><><

        # Note:- Add New Student Button
        self.internal_attainment_button = Button(self.report_attainment_frame1, text="internal attainment", bd=5, command=self.fetch_internal_exam_records)
        self.internal_attainment_button.place(x=380, y=5,width=150)


        # Note:- Remove Student Button
        self.final_examattainment_button = Button(self.report_attainment_frame1, text="SEE attainment", bd=5, command=self.fetch_final_exam_records)
        self.final_examattainment_button.place(x=565, y=5,width=150)

        # Note:- Show All Courses Button
        self.overall_attainment_button = Button(self.report_attainment_frame1, text="overall attainment", bd=5, command=self.fetch_attainment_record_overall)
        self.overall_attainment_button.place(x=745, y=5,width=150)

        # Note:- Clear Fields Button
        self.clear_fields_button = Button(self.report_attainment_frame1, text="Clear ", bd=5, command=self.clear_attainment_fields)
        self.clear_fields_button.place(x=810, y=40,width=80)

        # Note:- Create the Treeview widget
        self.report_attainment_treeview = ttk.Treeview(self.report_attainment_frame1,columns=("CO1", "CO2", "CO3", "CO4", "CO5", "CO6"),show='headings',padding=1)
        
        # Note:- Set the headings for the columns
        self.report_attainment_treeview.heading("CO1", text = "CO1")
        self.report_attainment_treeview.heading("CO2", text = "CO2")
        self.report_attainment_treeview.heading("CO3", text = "CO3")
        self.report_attainment_treeview.heading("CO4", text = "CO4")
        self.report_attainment_treeview.heading("CO5", text = "CO5")
        self.report_attainment_treeview.heading("CO6", text = "CO6")
        
        # Note:- self.report_attainment_treeview["show"] = "headings"

        # Note:- Set the columns to be centered
        self.report_attainment_treeview.column("CO1", anchor = CENTER, width = 20)
        self.report_attainment_treeview.column("CO2", anchor = CENTER, width = 20)
        self.report_attainment_treeview.column("CO3", anchor = CENTER, width = 20)
        self.report_attainment_treeview.column("CO4", anchor = CENTER, width = 20)
        self.report_attainment_treeview.column("CO5", anchor = CENTER, width = 20)
        self.report_attainment_treeview.column("CO6", anchor = CENTER, width = 20)

        # Note:- # Note:- Add vertical scrollbar
        # Note:- scrollbar_vertical = ttk.Scrollbar(self.report_attainment_frame1, orient="vertical", command=self.report_attainment_treeview.yview)
        # Note:- scrollbar_vertical.place(x=985, y=80, height=80)
        # Note:- self.report_attainment_treeview.configure(yscrollcommand=scrollbar_vertical.set)
        # Note:- # Note:- Add horizontal scrollbar
        # Note:- scrollbar_horizontal = ttk.Scrollbar(self.report_attainment_frame1, orient="horizontal", command=self.report_attainment_treeview.xview)
        # Note:- scrollbar_horizontal.place(x=1, y=180, width=1010)
        # Note:- self.report_attainment_treeview.configure(xscrollcommand=scrollbar_horizontal.set)

        self.report_attainment_treeview.place(x=170, y=75, width=720, height=100)

        # Note:- self.report_attainment_treeview.bind("<ButtonRelease-1>",self.get_student_reg_cursor)


    # Note:- ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><

# Note:-   /////////////////// UNCOMMENT BELOW CODE WHEN THE COPO MAPPIING WILL IN USE ////////////////////
# Note:-     # Note:- Create a Frame for holding COPO related fields and buttons (in main report Frame)
# Note:-         self.COPO_mapping_entry_frame2 = Frame(Main_report_frame, bd=5, bg="White", relief=RIDGE)
# Note:-         self.COPO_mapping_entry_frame2.place(x=0, y=35, width=1020, height=738)

# Note:-         # Note:- Add elements for COPO frame (example elements)
# Note:-         COPO_label = Label(self.COPO_mapping_entry_frame2, text="CO-PO Mapping", font=("times new roman", 10, "bold"))
# Note:-         COPO_label.place(x=5, y=5)

# Note:-         # Note:- Initially hide the COPO frame
# Note:-         self.COPO_mapping_entry_frame2.place_forget()


# Note:- +++++++++++++++++++++++++++ This Code Helps To Switch Between Frames ++++++++++++++++++++++++++
    def show_attainment_frame(self):
        self.report_attainment_frame1.place(x=0, y=35, width=1025, height=810)
        # Note:- self.COPO_mapping_entry_frame2.place_forget()
        # Note:- self.student_entry_frame3.place_forget()

    # Note:- (uncomment this below code if copo mapping is in use) 
    # Note:- def show_copo_mapping_frame(self):
    # Note:-     self.COPO_mapping_entry_frame2.place(x=0, y=35, width=1020, height=810)
    # Note:-     self.report_attainment_frame1.place_forget()

    # Note:- def attainment_report_window(self):
    # Note:-     self.attainment_entry_frame2.place(x=0, y=35, width=930, height=738)
    # Note:-     self.course_entry_frame1.place_forget()
    # Note:-     # Note:- self.student_entry_frame3.place_forget()


# Note:- Funtion for Exit from Report
    def exit_report_window(self):
            self.Report_window.destroy()


# Note:- :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def open_settings(self):
        self.Settings()       # Note:-it calls the below function

# Note:--------------------<<[ THIS FUNCTION HELPS TO CALL TOPLEVEL WINDOW of the SETTING function]>>--------------------

    def Settings(self):
        self.Settings_window = Toplevel(self.main_window)
        self.Settings_window.title("Settings")
        self.Settings_window.geometry("940x780+300+0")

    # Note:- Add a button frame for buttons
        Main_settings_frame = Frame(self.Settings_window, bd=4, bg="white", relief=RIDGE)
        Main_settings_frame.place(x=2, y=2, width=935, height=777)

        Main_settings_button_frame = Frame(Main_settings_frame, bd=5, bg="White", relief=RIDGE)
        Main_settings_button_frame.place(x=-1, y=-1, width=933, height=35)

        # Note:- Course Button
        course_button = Button(Main_settings_button_frame, text="Course", command=self.show_course_frame, bd=2, bg='gray', width=20)
        course_button.pack(side=LEFT, padx=5, pady=1)

        # Note:- CAs Button
        cas_button = Button(Main_settings_button_frame, text="Attainment", command=self.show_COattainment_frame, bd=2, bg='gray', width=20)
        cas_button.pack(side=LEFT, padx=5, pady=1)

        # Note:- Student Button
        student_button = Button(Main_settings_button_frame, text="Student", command=self.show_student_frame, bd=2, bg='gray', width=20)
        student_button.pack(side=LEFT, padx=5, pady=1)

        # Note:- Exit Button for settings window
        exit_button = Button(Main_settings_button_frame, text="Exit", command=self.exit_settings_window, bd=2, bg='gray', width=20)
        exit_button.pack(side=LEFT, padx=5, pady=1)

        # Note:- Bind keyboard shortcuts--
        self.Settings_window.bind('<Alt-s>', lambda event: self.show_course_frame())
        self.Settings_window.bind('<Alt-c>', lambda event: self.show_COattainment_frame())
        self.Settings_window.bind('<Alt-r>', lambda event: self.show_student_frame())
        self.Settings_window.bind('<Alt-e>', lambda event: self.exit_settings_window())


        # Note:- Create a Frame for holding entry fields and buttons (Course Frame)
        self.course_entry_frame1 = Frame(Main_settings_frame, bd=5, bg="White", relief=RIDGE)
        self.course_entry_frame1.place(x=0, y=35, width=930, height=738)

        # Note:- Entry field for New Course Code
        new_course_label = Label(self.course_entry_frame1, text="Enter Course Code:", font=("times new roman", 12, "bold"))
        new_course_label.place(x=5, y=10)
        self.new_course_code = StringVar()
        new_course_entry = Entry(self.course_entry_frame1, bd=2, textvariable=self.new_course_code, font=("times new roman", 12, "bold"))
        new_course_entry.place(x=155, y=10)

        # Note:- Entry field for Semester Number
        semester_label = Label(self.course_entry_frame1, text="Semester No:", font=("times new roman", 12, "bold"))
        semester_label.place(x=5, y=50)
        self.semester_no = StringVar()
        semester_entry = Entry(self.course_entry_frame1, textvariable=self.semester_no, bd=2, font=("times new roman", 12, "bold"), width=5)
        semester_entry.place(x=155, y=50)
        new_course_entry.bind("<KeyRelease>", self.convert_to_uppercase)

        # Note:- Add New Course Button
        self.add_course_button = Button(self.course_entry_frame1, text="Add New Course", bd=4, command=self.add_new_course)
        self.add_course_button.place(x=230, y=45)
        self.add_course_button.bind("<ButtonRelease-1>", lambda event: self.show_all_courses())

        # Note:- Show All Courses Button
        self.show_all_button = Button(self.course_entry_frame1, text="Show all Courses", bd=4, command=self.show_all_courses)
        self.show_all_button.place(x=350, y=10)

        # Note:- Remove Course Button
        self.remove_course_button = Button(self.course_entry_frame1, text="Remove Course", bd=4, command=self.remove_course)
        self.remove_course_button.place(x=350, y=45)
        self.remove_course_button.bind("<ButtonRelease-1>", lambda event: self.show_all_courses())

        # Note:- Create the Treeview widget
        self.course_tree = ttk.Treeview(self.course_entry_frame1, columns=("Semester", "Course Code"), show='headings')
        self.course_tree.heading("Semester", text="Semester")
        self.course_tree.heading("Course Code", text="Course Code")
        self.course_tree.column("Semester", anchor=CENTER)
        self.course_tree.column("Course Code", anchor=CENTER)

        # Note:- Add vertical scrollbar
        vsb = ttk.Scrollbar(self.course_entry_frame1, orient="vertical", command=self.course_tree.yview)
        vsb.place(x=895, y=100, height=600)
        self.course_tree.configure(yscrollcommand=vsb.set)

        # Note:- Add horizontal scrollbar
        hsb = ttk.Scrollbar(self.course_entry_frame1, orient="horizontal", command=self.course_tree.xview)
        hsb.place(x=10, y=710, width=885)
        self.course_tree.configure(xscrollcommand=hsb.set)

        # Note:- Place the Treeview widget
        self.course_tree.place(x=10, y=100, width=885, height=600)
# Note:- //////////////////////////////////////////////////////////////////////////////////////

        # Note:- Create a Frame for holding Attainment related fields and buttons (Attainment Frame)
        self.attainment_entry_frame2 = Frame(Main_settings_frame, bd=5, bg="White", relief=RIDGE)
        self.attainment_entry_frame2.place(x=0, y=35, width=930, height=738)

        # Note:- Label for "label for attainment settings
        self.attainment_settings_label = Label(self.attainment_entry_frame2, text="Attainment Target and Weightage Settings -", font=("times new roman", 16, "bold"), bg="White",fg="Blue")
        self.attainment_settings_label.place(x=5, y=2)

        # Note:- Label for "Choose Course"
        self.choose_course_label = Label(self.attainment_entry_frame2, text="Choose Course", font=("times new roman", 13, "bold"), bg="White")
        self.choose_course_label.place(x=25, y=50)

        # Note:- For Target label course referancing function
        def report_update_courses_target():
            conn = sqlite3.connect("Attainment_record.db")
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT course_code FROM Course_Table ORDER BY course_code")
            course_codes = [row[0] for row in cursor.fetchall()]
            conn.close()
            return course_codes

        # Note:- ComboBox for course codes
        self.course_code_combo = ttk.Combobox(self.attainment_entry_frame2)
        self.course_code_combo.place(x=150, y=50,width=200)
        self.course_code_combo['values'] = report_update_courses_target()

        # Note:- Label for "Type"
        self.target_type_label = Label(self.attainment_entry_frame2, text="Target-Type", font=("times new roman", 12, "bold"), bg="White")
        self.target_type_label.place(x=370, y=50)

        # Note:- ComboBox for target type
        self.target_type_combo = ttk.Combobox(self.attainment_entry_frame2, values=['internal', 'final', 'overall'])
        self.target_type_combo.place(x=460, y=52)
        self.target_type_combo.current(0) 

        # Note:- Add elements for Internal Target frame
        target_label = Label(self.attainment_entry_frame2, text="Target Mark in %", font=("times new roman", 12, "bold"), bg="White")
        target_label.place(x=215, y=135)

        self.target_label = IntVar()
        self.target_label.set("")  # Note:- Set the initial value to empty string
        target_label_entry = Entry(self.attainment_entry_frame2, bd=2, textvariable=self.target_label, font=("times new roman", 13, "bold"))
        target_label_entry.place(x=345, y=135, width=50)

        # Note:- Level 3
        target_label3 = Label(self.attainment_entry_frame2, text="Level 3 ", font=("times new roman", 12, "bold"), bg="White")
        target_label3.place(x=405, y=105)

        self.settarget_label3 = IntVar()
        self.settarget_label3.set("")  # Note:- Set the initial value to empty string
        target_label_entry3 = Entry(self.attainment_entry_frame2, bd=2, textvariable=self.settarget_label3, font=("times new roman", 13, "bold"))
        target_label_entry3.place(x=470, y=105, width=50)

        # Note:- Level 2
        target_label2 = Label(self.attainment_entry_frame2, text="Level 2 ", font=("times new roman", 12, "bold"), bg="White")
        target_label2.place(x=405, y=140)

        self.settarget_label2 = IntVar()
        self.settarget_label2.set("")  # Note:- Set the initial value to empty string
        target_label_entry2 = Entry(self.attainment_entry_frame2, bd=2, textvariable=self.settarget_label2, font=("times new roman", 13, "bold"))
        target_label_entry2.place(x=470, y=140, width=50)

        # Note:- Level 1
        target_label1 = Label(self.attainment_entry_frame2, text="Level 1 ", font=("times new roman", 12, "bold"), bg="White")
        target_label1.place(x=405, y=180)

        self.settarget_label1 = IntVar()
        self.settarget_label1.set("")  # Note:- Set the initial value to empty string
        target_label_entry1 = Entry(self.attainment_entry_frame2, bd=2, textvariable=self.settarget_label1, font=("times new roman", 13, "bold"))
        target_label_entry1.place(x=470, y=180, width=50)

        # Note:- Add Update Button for Internal Target Level
        update_btn = Button(self.attainment_entry_frame2, bd=4, text="Update Target Level", font=("times new roman", 12, "bold"),command=self.update_target_level)
        update_btn.place(x=50, y=115)

        # Note:- Add Show Data Button
        show_data_btn = Button(self.attainment_entry_frame2, bd=4, text="Show Data", font=("times new roman", 12, "bold"), command=self.show_target_data)
        show_data_btn.place(x=50, y=165,width=155)

        # Note:- Add elements for Internal and External Weights
        internal_weight_label = Label(self.attainment_entry_frame2, text="Internal Weight", font=("times new roman", 12, "bold"), bg="White")
        internal_weight_label.place(x=45, y=265)
        self.internal_weight_entry = Entry(self.attainment_entry_frame2, bd=2, font=("times new roman", 13, "bold"))
        self.internal_weight_entry.place(x=180, y=265, width=50)

        external_weight_label = Label(self.attainment_entry_frame2, text="External Weight", font=("times new roman", 12, "bold"), bg="White")
        external_weight_label.place(x=250, y=265)
        self.external_weight_entry = Entry(self.attainment_entry_frame2, bd=2, font=("times new roman", 13, "bold"))
        self.external_weight_entry.place(x=380, y=265, width=50)

        # Note:- Add combined Update and Show Button for Internal and External Weights
        update_show_btn = Button(self.attainment_entry_frame2, bd=4, text="Update", font=("times new roman", 12, "bold"), command = self.update_weights)
        update_show_btn.place(x=50, y=310, width=150)

        # Note:- Example usage of the show_weights function:
        # Note:- Assuming we have a button that calls this function when clicked
        show_weights_btn = Button(self.attainment_entry_frame2, bd=4, text="Show Weights", font=("times new roman", 12, "bold"), command=self.show_weights)
        show_weights_btn.place(x=250, y=310, width=150)

        # Note:- Initially hide the CAs frame
        self.attainment_entry_frame2.place_forget()


    # Note:- Create a Frame for holding student related fields and buttons (Student Registration Frame)
        self.student_entry_frame3 = Frame(Main_settings_frame, bd=5, bg="White", relief=RIDGE)
        self.student_entry_frame3.place(x=0, y=35, width=930, height=738)

        # Note:- Add elements for Student frame
        stu_reg_label = Label(self.student_entry_frame3, text="Student Registration", font=("times new roman", 16, "bold"),bg="White")
        stu_reg_label.place(x=5, y=4)

        # Note:- Entry fields for student information in a single line

        # Note:- Student Name Entry
        student_name_label = Label(self.student_entry_frame3, text="Student Name:", font=("times new roman", 12, "bold"), bg="White")
        student_name_label.place(x=2, y=50)

        self.student_name = StringVar()
        # Note:- This function for fetch student names from the STUDENT in the Attainment_record database
        def fetch_student_names_from_database():
            conn = sqlite3.connect("Attainment_record.db")  
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT DISTINCT Student_name FROM STUDENT 
                    ORDER BY Academic_year DESC, Semester DESC, Student_name ASC, Student_Reg_No ASC
                ''')
            fetched_student_names = [row[0] for row in cursor.fetchall()]
            conn.close()
            return fetched_student_names

        # Note:- This function for update suggestion list based on input text for student names Combobox
        def update_student_name_suggestion(event=None):
            fetched_student_names = fetch_student_names_from_database()
            current_text = student_name_entry.get()
            matching_student_names = [name for name in fetched_student_names if name.startswith(current_text)]
            student_name_entry["values"] = matching_student_names

        fetched_student_names = fetch_student_names_from_database()

        student_name_entry = ttk.Combobox(self.student_entry_frame3, textvariable=self.student_name, font=("times new roman", 12, "bold"))
        student_name_entry["values"] = fetched_student_names
        student_name_entry.place(x=107, y=50, width=180)
        student_name_entry.bind("<KeyRelease>", update_student_name_suggestion)
        update_student_name_suggestion()

        # Note:- Student ID No Entry
        student_reg_no_label = Label(self.student_entry_frame3, text="ID No:", font=("times new roman", 12, "bold"), bg="White")
        student_reg_no_label.place(x=300, y=50)
        self.register_student_reg_no = StringVar()
        student_reg_no_entry = ttk.Combobox(self.student_entry_frame3, textvariable=self.register_student_reg_no, font=("times new roman", 12, "bold"))
        student_reg_no_entry.place(x=365, y=50, width=170)

        # Note:- Semester Combobox
        semester_label = Label(self.student_entry_frame3, text="Semester:", font=("times new roman", 12, "bold"), bg="White")
        semester_label.place(x=560, y=50)
        self.student_semester = StringVar()
        semester_entry = ttk.Combobox(self.student_entry_frame3, textvariable=self.student_semester, font=("times new roman", 12, "bold"), state="readonly")
        semester_entry["values"] = [str(i) for i in range(1, 9)]
        semester_entry.place(x=645, y=50, width=45)

        # Note:- Academic Year Combobox
        academic_year_label = Label(self.student_entry_frame3, text="Academic Year:", font=("times new roman", 11, "bold"), bg="White")
        academic_year_label.place(x=707, y=50)
        self.academic_year = StringVar()
        academic_year_entry = ttk.Combobox(self.student_entry_frame3, textvariable=self.academic_year, font=("times new roman", 12, "bold"), state="readonly")
        student_year_values = [f"{year}-{str(year + 1)[-2:]}" for year in range(datetime.datetime.now().year - 4, datetime.datetime.now().year + 1)]
        academic_year_entry["values"] = student_year_values
        academic_year_entry.place(x=825, y=50, width=80)

    # Note:- ><><><><><><><><><><><>< Student Button ><><><><><><><><><><><><><

        # Note:- Add New Student Button
        self.add_student_button = Button(self.student_entry_frame3, text="Add New Student", bd=5, command=self.add_new_student)
        self.add_student_button.place(x=410, y=10)
        self.add_student_button.bind("<ButtonRelease-1>", lambda event: self.show_all_students())
        # Note:- Remove Student Button
        self.remove_student_button = Button(self.student_entry_frame3, text="Remove Student", bd=5, command=self.delete_student_data)
        self.remove_student_button.place(x=535, y=10)
        self.remove_student_button.bind("<ButtonRelease-1>", lambda event: self.show_all_students())
        # Note:- Show All Courses Button
        self.show_all_student_button = Button(self.student_entry_frame3, text="Show all Students", bd=5, command=self.show_all_students)
        self.show_all_student_button.place(x=655, y=10)
        # Note:- Clear Fields Button
        self.clear_fields_button = Button(self.student_entry_frame3, text="Clear", bd=5, command=self.clear_fields)
        self.clear_fields_button.place(x=780, y=10,width=100)

        # Note:- Create the Treeview widget
        self.student_tree = ttk.Treeview(self.student_entry_frame3, columns=("Academic Year", "Semester", "Student Name", "Student ID"), show='headings')
        
        # Note:- Set the headings for the columns
        self.student_tree.heading("Academic Year", text="Academic Year")
        self.student_tree.heading("Semester", text="Semester")
        self.student_tree.heading("Student Name", text="Student Name")
        self.student_tree.heading("Student ID", text="Student ID")
        
        # Note:- Set the columns to be centered
        self.student_tree.column("Academic Year", anchor=CENTER)
        self.student_tree.column("Semester", anchor=CENTER)
        self.student_tree.column("Student Name", anchor=CENTER)
        self.student_tree.column("Student ID", anchor=CENTER)

        # Note:- Add vertical scrollbar
        vsb_student = ttk.Scrollbar(self.student_entry_frame3, orient="vertical", command=self.student_tree.yview)
        vsb_student.place(x=895, y=100, height=600)
        self.student_tree.configure(yscrollcommand=vsb_student.set)

        # Note:- Add horizontal scrollbar
        hsb_student = ttk.Scrollbar(self.student_entry_frame3, orient="horizontal", command=self.student_tree.xview)
        hsb_student.place(x=10, y=710, width=885)
        self.student_tree.configure(xscrollcommand=hsb_student.set)

        self.student_tree.place(x=10, y=100, width=885, height=600)

        self.student_tree.bind("<ButtonRelease-1>",self.get_student_reg_cursor)

        # Note:- This below three functions insert in blank Tables only**
        self.initialize_default_targets()
        self.initialize_default_levels()
        self.initialize_default_weights()
        
        # Note:- ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><

# Note:- +++++++++++++++++++++++++++ This Code Helps To Switch Between Frames +++++++++++++++++++++++++++++++++++++++++++
    def show_course_frame(self):
        self.course_entry_frame1.place(x=0, y=35, width=930, height=738)
        self.attainment_entry_frame2.place_forget()
        self.student_entry_frame3.place_forget()

    def show_COattainment_frame(self):
        self.attainment_entry_frame2.place(x=0, y=35, width=930, height=738)
        self.course_entry_frame1.place_forget()
        self.student_entry_frame3.place_forget()

    def show_student_frame(self):
        self.student_entry_frame3.place(x=0, y=35, width=930, height=738)
        self.course_entry_frame1.place_forget()
        self.attainment_entry_frame2.place_forget()

    def convert_to_uppercase(self, event):
        entry = event.widget
        entry_value = entry.get()
        entry.delete(0, END)
        entry.insert(0, entry_value.upper())
# Note:- /////////////////////////////////////////////////////////////////////////////////////////////
    def create_course_table(self):
        try:
            conn = sqlite3.connect('Attainment_record.db')
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Course_Table (
                course_code TEXT PRIMARY KEY,
                semester_no INTEGER NOT NULL
            )
            ''')
            conn.commit()
        except Exception as e:
            self.show_warning(f"Error creating table: {e}")
        finally:
            conn.close()

    def add_new_course(self):
        self.create_course_table()

        course_code = self.new_course_code.get()
        semester_no = self.semester_no.get()

        if not course_code or not semester_no:
            self.show_warning("Fields cannot be blank!")
            return

        try:
            conn = sqlite3.connect('Attainment_record.db')
            cursor = conn.cursor()

            # Note:- Insert the new course into the table
            cursor.execute('''
            INSERT INTO Course_Table (course_code, semester_no)
            VALUES (?, ?)
            ''', (course_code, semester_no))

            conn.commit()
        except Exception as e:
            self.show_warning(f"Error: {e}")
        finally:
            conn.close()

        self.new_course_code.set("")  # Note:- Clear the input field
        self.semester_no.set("")  # Note:- Clear the semester input field
    

    def remove_course(self):
        self.create_course_table()

        course_code = self.new_course_code.get()
        semester_no = self.semester_no.get()

        if not course_code or not semester_no:
            self.show_warning("Fields cannot be blank!")
            return

        try:
            conn = sqlite3.connect('Attainment_record.db')
            cursor = conn.cursor()

            # Note:- Remove the course from the table
            cursor.execute('''
            DELETE FROM Course_Table WHERE course_code = ? AND semester_no = ?
            ''', (course_code, semester_no))

            conn.commit()
            self.show_all_courses()
        except Exception as e:
            self.show_warning(f"Error: {e}")
        finally:
            conn.close()

        self.new_course_code.set("")  # Note:- Clear the input field
        self.semester_no.set("")  # Note:- Clear the semester input field

    def show_all_courses(self):
        self.create_course_table()

        try:
            conn = sqlite3.connect('Attainment_record.db')
            cursor = conn.cursor()

            # Note:- Fetch all courses from the table
            cursor.execute("SELECT semester_no, course_code FROM Course_Table ORDER BY course_code ASC, semester_no ASC")
            courses = cursor.fetchall()
        except Exception as e:
            self.show_warning(f"Error: {e}")
            return
        finally:
            conn.close()

        # Note:- Clear previous entries in the Treeview
        for row in self.course_tree.get_children():
            self.course_tree.delete(row)

        # Note:- Add data to the Treeview
        for course in courses:
            self.course_tree.insert("", END, values=course)
    # Note:- +++++++++++++++++++++++++++++++ Student ++++++++++++++++++++++++++++++++++
    # Note:- ////////////////////////// Student Table /////////////////////////
    def create_student_table(self):
        try:
            conn = sqlite3.connect('Attainment_record.db')
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS STUDENT (
                Academic_year VARCHAR(10),
                Student_name TEXT,
                Student_Reg_No INTEGER PRIMARY KEY,
                Semester INTEGER
            )
            ''')
            conn.commit()
            
        except Exception as e:
            self.show_warning(f"Error creating table: {e}")
        finally:
            conn.close()
    
    # Note:- Register new Student function-->
    def insert_new_student_data(self, academic_year, student_name, register_student_reg_no, semester):
        conn = sqlite3.connect('Attainment_record.db')
        my_cursor = conn.cursor()

        try:
            # Note:- Insert data into the STUDENT table
            my_cursor.execute('''
                INSERT INTO STUDENT (
                    Academic_year,
                    Student_name,
                    Student_Reg_No,
                    Semester
                ) VALUES (?, ?, ?, ?)
            ''', (
                academic_year,
                student_name,
                register_student_reg_no,
                semester
            ))
            conn.commit()
            self.show_warning("New Student Registered Successfully!")
            self.show_all_students()

        except sqlite3.Error as e:
            self.show_warning(f"Error: {e}")
        finally:
            conn.close()

# Note:- This function help to register new students0
    def add_new_student(self):
        self.create_student_table()
        

        if self.academic_year.get() == "" or self.student_name.get() == "" or self.register_student_reg_no.get() == "" or self.student_semester.get() == "":
            self.show_warning("  Please fill in all required fields:\n\u2022 Academic Year \u2022 Student Name\n\u2022 Semester \n\u2022 Registration Number  ")
        else:
            self.insert_new_student_data(
                self.academic_year.get(),
                self.student_name.get(),
                self.register_student_reg_no.get(),
                self.student_semester.get()
            )
        
    # Note:-///////////////// Delete Student //////////////////
    def delete_student_data(self):
        self.create_student_table()
        academic_year = self.academic_year.get()
        select_student_reg_no = self.register_student_reg_no.get()
        semester = self.student_semester.get()

        if academic_year == "" or select_student_reg_no == "" or semester == "":
            self.show_warning("Please fill in all required fields:\n\u2022 Academic Year\n\u2022 Semester\n\u2022 Course Code\n\u2022 Exam Name\n\u2022 At least one QuCO")
            return

        conn = sqlite3.connect('Attainment_record.db')
        my_cursor = conn.cursor()

        try:
            # Note:- Check if student with given details exists
            my_cursor.execute('''
                SELECT COUNT(*)
                FROM STUDENT
                WHERE Academic_year = ? AND Semester = ? AND Student_Reg_No = ?
            ''', (academic_year, semester, select_student_reg_no))

            count = my_cursor.fetchone()[0]
            if count == 0:
                self.show_warning("Error: No student found with the specified details.")
                return

            # Note:- Delete student data
            my_cursor.execute('''
                DELETE FROM STUDENT
                WHERE Academic_year = ? AND Semester = ? AND Student_Reg_No = ?
            ''', (academic_year, semester, select_student_reg_no))

            conn.commit()

            self.show_warning("Delete: Student data has been deleted successfully!")
            self.show_all_students()
        except sqlite3.Error as e:
            self.show_warning(f": deleting data: {e}")
        finally:
            conn.close()


    def show_all_students(self):
        self.create_student_table()
        try:
            conn = sqlite3.connect('Attainment_record.db')
            cursor = conn.cursor()
            cursor.execute("SELECT Academic_year, Semester, Student_name, Student_Reg_No FROM STUDENT ORDER BY Academic_year DESC, Semester ASC, Student_name ASC, Student_Reg_No ASC")
            students = cursor.fetchall()
        except Exception as e:
            self.show_warning(f"Error: {e}")
            return
        finally:
            conn.close()

        # Note:- Clear previous entries in the Treeview
        for row in self.student_tree.get_children():
            self.student_tree.delete(row)
        # Note:- Add data to the Treeview
        for student in students:
            self.student_tree.insert("", 'end', values=student)


    # Note:- This cursor helps to autofill the field of the Student ID Fields
    def get_student_reg_cursor(self, event=""):
        cursor_row = self.student_tree.focus()
        content = self.student_tree.item(cursor_row)
        row = content["values"]

        if row:
            self.academic_year.set(row[0])       
            self.student_semester.set(row[1])     
            self.student_name.set(row[2])    
            self.register_student_reg_no.set(row[3])      


    def clear_fields(self):
        self.academic_year.set("")               # Note:- Clear Academic Year
        self.student_name.set("")                # Note:- Clear Student Name
        self.register_student_reg_no.set("")     # Note:- Clear Student ID Number

        # Note:- +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def exit_settings_window(self):
        self.Settings_window.destroy()

# Note:-This is a custom function to show error in error occur in setting window
    def show_warning(self, message):
        # Note:- Create and configure the warning window
        warning_window = Toplevel(self.Settings_window)
        warning_window.title("Warning")
        warning_window.geometry("240x200")

        # Note:- Calculate and set the position to center the warning window
        settings_geometry = [int(i) for i in self.Settings_window.geometry().replace('+', 'x').split('x')]
        settings_width, settings_height, settings_x, settings_y = settings_geometry

        warning_width, warning_height = 270, 150
        position_right = settings_x + (settings_width - warning_width) // 2
        position_down = settings_y + (settings_height - warning_height) // 2

        warning_window.geometry(f"{warning_width}x{warning_height}+{position_right}+{position_down}")

        # Note:- Add a message label in the warning window
        Label(warning_window, text=message, wraplength=180, justify='center').pack(expand=True, padx=10, pady=10)

        # Note:- Add an OK button to close the warning window and re-enable buttons
        Button(warning_window, text="OK", command=warning_window.destroy).pack(pady=10)

# Note:-__________________________________________________________________________________________________

# Note:- ---------------------Attainment Function(sql quaries)-------------------------------------
# Note:- ----------------------------- Backend Processing ------------------------------
    def clear_attainment_fields(self):
        self.report_attainment_year.get("")
        self.report_attainment_semester.get("")
        self.report_attainment_course_code.get("")


    def show_target_data(self):
        course_code = self.course_code_combo.get()
        target_type = self.target_type_combo.get()

        if course_code and target_type:
            try:
                conn = sqlite3.connect("Attainment_record.db")
                cursor = conn.cursor()

                # Note:- Retrieve target value from Target_Variable_Table
                cursor.execute(f"SELECT {target_type}_target FROM Target_Variable_Table WHERE course_code = ?", (course_code,))
                target_row = cursor.fetchone()

                # Note:- Retrieve levels from Level_Table
                cursor.execute("SELECT level_0, level_1, level_2 FROM Level_Table WHERE course_code = ? AND target_type = ?", (course_code, target_type))
                level_row = cursor.fetchone()

                if target_row and level_row:
                    # Note:- Populate UI fields with target and level values
                    self.target_label.set(target_row[0])  # Note:- Target value

                    self.settarget_label3.set(level_row[2])  # Note:- Level 3
                    self.settarget_label2.set(level_row[1])  # Note:- Level 2
                    self.settarget_label1.set(level_row[0])  # Note:- Level 1

                elif target_row and not level_row:
                    # Note:- If target exists but levels do not, show target and clear levels
                    self.target_label.set(target_row[0])  # Note:- Target value

                    self.settarget_label3.set("")
                    self.settarget_label2.set("")
                    self.settarget_label1.set("")

                elif not target_row and level_row:
                    # Note:- If levels exist but target does not, show levels and clear target
                    self.target_label.set("")

                    self.settarget_label3.set(level_row[2])  # Note:- Level 3
                    self.settarget_label2.set(level_row[1])  # Note:- Level 2
                    self.settarget_label1.set(level_row[0])  # Note:- Level 1

                else:
                    # Note:- If neither target nor levels exist, show message and clear fields
                    messagebox.showinfo("No Data", "No target data found for selected course and type.")
                    self.target_label.set("")
                    self.settarget_label3.set("")
                    self.settarget_label2.set("")
                    self.settarget_label1.set("")

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

            finally:
                if conn:
                    conn.close()

        else:
            messagebox.showerror("Error", "Please select a course and target type.")



    def update_target_level(self):
        course_code = self.course_code_combo.get()
        target_type = self.target_type_combo.get()
        level_0 = self.target_label.get()
        level_1 = self.settarget_label1.get()
        level_2 = self.settarget_label2.get()
        level_3 = self.settarget_label3.get()

        if course_code and target_type:
            try:
                conn = sqlite3.connect("Attainment_record.db")
                cursor = conn.cursor()

                # Note:- Update Level_Table
                cursor.execute("""
                    INSERT OR REPLACE INTO Level_Table (course_code, target_type, level_0, level_1, level_2)
                    VALUES (?, ?, ?, ?, ?)
                """, (course_code, target_type, level_1, level_2, level_3))

                # Note:- Check if the course_code already exists in Target_Variable_Table
                cursor.execute("SELECT 1 FROM Target_Variable_Table WHERE course_code = ?", (course_code,))
                exists = cursor.fetchone()

                if exists:
                    # Note:- Update the specific target column in Target_Variable_Table
                    cursor.execute(f"""
                        UPDATE Target_Variable_Table
                        SET {target_type}_target = ?
                        WHERE course_code = ?
                    """, (level_0, course_code))
                else:
                    # Note:- Insert new row into Target_Variable_Table
                    cursor.execute("""
                        INSERT INTO Target_Variable_Table (course_code, internal_target, final_target, overall_target)
                        VALUES (?, ?, ?, ?)
                    """, (course_code,
                        level_0 if target_type == 'internal' else None,
                        level_0 if target_type == 'final' else None,
                        level_0 if target_type == 'overall' else None))

                conn.commit()
                messagebox.showinfo("Success", "Target levels updated successfully.")

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

            finally:
                if conn:
                    conn.close()

        else:
            messagebox.showerror("Error", "Please select a course and target type.")


    def remove_current_label(self):
        if hasattr(self, 'current_label') and self.current_label:
            self.current_label.destroy()
            self.current_label = None


    def initialize_default_targets(self, course_code):
        conn = sqlite3.connect("Attainment_record.db")
        cursor = conn.cursor()

        # Note:- Check if the row with the given course_code exists in Target_Variable_Table
        cursor.execute('SELECT COUNT(*) FROM Target_Variable_Table WHERE course_code = ?', (course_code,))
        count = cursor.fetchone()[0]

        if count == 0:
            # Note:- Insert default values if the row with the given course_code does not exist
            cursor.execute('''
                INSERT INTO Target_Variable_Table (course_code, internal_target, final_target, overall_target)
                VALUES (?, 60, 60, 60)
            ''', (course_code,))
            conn.commit()

        conn.close()


    def initialize_default_levels(self, course_code):
        conn = sqlite3.connect("Attainment_record.db")
        cursor = conn.cursor()

        target_types = ['internal', 'final', 'overall']

        for target_type in target_types:
            # Note:- Check if the row with the given course_code and target_type exists in Level_Table
            cursor.execute('SELECT COUNT(*) FROM Level_Table WHERE course_code = ? AND target_type = ?', (course_code, target_type))
            count = cursor.fetchone()[0]

            if count == 0:
                # Note:- Insert default values if the row with the given course_code and target_type does not exist
                cursor.execute('''
                    INSERT INTO Level_Table (course_code, target_type, level_0, level_1, level_2)
                    VALUES (?, ?, 40, 50, 60)
                ''', (course_code, target_type))
                conn.commit()

        conn.close()



    def initialize_default_weights(self):
        conn = sqlite3.connect("Attainment_record.db")
        cursor = conn.cursor()
        
        # Note:- Check if the row with id = 1 exists
        cursor.execute('SELECT COUNT(*) FROM weight_table WHERE id = 1')
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Note:- Insert default values if the row with id = 1 does not exist
            cursor.execute('INSERT INTO weight_table (id, internal_weight, external_weight) VALUES (1, 30, 70)')
            conn.commit()
        
        conn.close()

    # Note:- Function to update both internal and external weights in the database
    def update_weights(self):
        internal_weight = self.internal_weight_entry.get()
        external_weight = self.external_weight_entry.get()

        # Note:- Validate input (optional)
        if not internal_weight or not external_weight:
            messagebox.showerror("Error", "Internal Weight and External Weight cannot be empty.")
            return

        try:
            # Note:- Convert weights to float (assuming weights are floating point numbers)
            internal_weight = float(internal_weight)
            external_weight = float(external_weight)
        except ValueError:
            messagebox.showerror("Error", "Invalid input for weights. Please enter valid numbers.")
            return

        conn = sqlite3.connect("Attainment_record.db")
        cursor = conn.cursor()

        update_query = '''
        UPDATE weight_table
        SET internal_weight = ?,
            external_weight = ?
        WHERE id = 1
        '''

        cursor.execute(update_query, (internal_weight, external_weight))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Weights updated successfully.")

        # Note:- Optionally, clear the entry fields after updating
        self.internal_weight_entry.delete(0, END)
        self.external_weight_entry.delete(0, END)



    # Note:- Function to show weights (both internal and external) from the database
    def show_weights(self):
        conn = sqlite3.connect("Attainment_record.db")
        cursor = conn.cursor()
        
        fetch_query = '''
        SELECT internal_weight, external_weight
        FROM weight_table
        WHERE id = 1  -- Assuming id 1 represents the coefficients for wer application
        '''
        
        cursor.execute(fetch_query)
        weights = cursor.fetchone()  # Note:- Fetch the first row
        
        conn.close()
        
        if weights:
            internal_weight, external_weight = weights
            self.internal_weight_entry.delete(0, END)
            self.internal_weight_entry.insert(0, internal_weight)
            
            self.external_weight_entry.delete(0, END)
            self.external_weight_entry.insert(0, external_weight)
        else:
            # Note:- Handle case where no weights are found (optional)
            messagebox.showwarning("No Data", "No weights found in the database.")


    def fetch_attainment_record_overall(self, event=None):

        # Note:- Checking and removing the label
        self.remove_current_label()
        self.current_label = Label(self.report_attainment_frame1, text="Overall Attainment report", font=("times new roman", 11, "bold"), fg="Red")
        self.current_label.place(x=400, y=180, width=180)

        # Note:- Retrieve the values from the input fields
        year = self.report_attainment_year.get()
        semester = self.report_attainment_semester.get()
        course_code = self.report_attainment_course_code.get()

        conn = sqlite3.connect('Attainment_record.db')
        my_cursor = conn.cursor()
        
         # Note:- Fetch coefficients from the database
        fetch_coefficients_query = '''
            SELECT internal_weight, external_weight
            FROM weight_table
            WHERE id = 1  -- Assuming id 1 represents the coefficients for wer application
        '''
        my_cursor.execute(fetch_coefficients_query)
        coefficients = my_cursor.fetchone()

        if coefficients:
            internal_weight, external_weight = coefficients
        else:
            # Note:- Default values if coefficients are not found (we can adjust these as needed)
            internal_weight, external_weight = 0.3, 0.7

        fetch_query1 = f"""
        SELECT overall_target
        FROM Target_Variable_Table
        WHERE course_code = '{course_code}'
        """
        my_cursor.execute(fetch_query1)
        row1 = my_cursor.fetchone()

        
        if row1:
            overall_target = row1[0]
        fetch_query2 = f"""
        SELECT level_0, level_1, level_2
        FROM Level_Table
        WHERE course_code = '{course_code}' AND target_type = 'overall'
        """
        my_cursor.execute(fetch_query2)
        row2 = my_cursor.fetchone()

        if row2:
            level_0, level_1, level_2 = row2
        my_cursor.execute("DROP VIEW IF EXISTS 'OVERALL'")
        
        # Note:- Create the view without parameterized query
        create_view_query = f"""
        CREATE VIEW 'OVERALL' AS
        WITH CTE1 AS (
            SELECT 
                am.Student_Reg_No,
                am.Course_code,
                ROUND((SUM(CASE WHEN am.SCA_No IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO1 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO1 ELSE 0 END)), 2) AS Percentage_CO1,
                ROUND((SUM(CASE WHEN am.SCA_No IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO2 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO2 ELSE 0 END)), 2) AS Percentage_CO2,
                ROUND((SUM(CASE WHEN am.SCA_No IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO3 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO3 ELSE 0 END)), 2) AS Percentage_CO3,
                ROUND((SUM(CASE WHEN am.SCA_No IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO4 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO4 ELSE 0 END)), 2) AS Percentage_CO4,
                ROUND((SUM(CASE WHEN am.SCA_No IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO5 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO5 ELSE 0 END)), 2) AS Percentage_CO5,
                ROUND((SUM(CASE WHEN am.SCA_No IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO6 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO6 ELSE 0 END)), 2) AS Percentage_CO6
            FROM 
                ANSWER_MARK am
            JOIN 
                QUESTION_MARK qm ON am.Course_code = qm.Course_code AND am.SCA_No = qm.Exam_Name
            JOIN 
                STUDENT st ON am.Student_Reg_No = st.Student_Reg_No
            WHERE  
                st.Academic_year = '{year}'
                AND am.Course_code = '{course_code}'
                AND st.Semester = '{semester}'
            GROUP BY 
                am.Student_Reg_No, am.Course_code
        ),
        CTE2 AS (
            SELECT 
                am.Student_Reg_No,
                am.Course_code,
                ROUND((SUM(CASE WHEN am.SCA_No NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO1 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO1 ELSE 0 END)), 2) AS Percentage_CO1,
                ROUND((SUM(CASE WHEN am.SCA_No NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO2 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO2 ELSE 0 END)), 2) AS Percentage_CO2,
                ROUND((SUM(CASE WHEN am.SCA_No NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO3 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO3 ELSE 0 END)), 2) AS Percentage_CO3,
                ROUND((SUM(CASE WHEN am.SCA_No NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO4 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO4 ELSE 0 END)), 2) AS Percentage_CO4,
                ROUND((SUM(CASE WHEN am.SCA_No NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO5 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO5 ELSE 0 END)), 2) AS Percentage_CO5,
                ROUND((SUM(CASE WHEN am.SCA_No NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO6 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO6 ELSE 0 END)), 2) AS Percentage_CO6
            FROM 
                ANSWER_MARK am
            JOIN 
                QUESTION_MARK qm ON am.Course_code = qm.Course_code AND am.SCA_No = qm.Exam_Name
            JOIN 
                STUDENT st ON am.Student_Reg_No = st.Student_Reg_No
            WHERE  
                st.Academic_year = '{year}'
                AND am.Course_code = '{course_code}'
                AND st.Semester = '{semester}'
            GROUP BY 
                am.Student_Reg_No, am.Course_code
        ),
        FinalScores AS (
            SELECT 
                CTE1.Student_Reg_No,
                CTE1.Course_code,
                st.Student_Name,
                ROUND(( {internal_weight} * CTE1.Percentage_CO1 + {external_weight} * CTE2.Percentage_CO1), 2) AS Combined_Score_CO1,
                ROUND(( {internal_weight} * CTE1.Percentage_CO2 + {external_weight} * CTE2.Percentage_CO2), 2) AS Combined_Score_CO2,
                ROUND(( {internal_weight} * CTE1.Percentage_CO3 + {external_weight} * CTE2.Percentage_CO3), 2) AS Combined_Score_CO3,
                ROUND(( {internal_weight} * CTE1.Percentage_CO4 + {external_weight} * CTE2.Percentage_CO4), 2) AS Combined_Score_CO4,
                ROUND(( {internal_weight} * CTE1.Percentage_CO5 + {external_weight} * CTE2.Percentage_CO5), 2) AS Combined_Score_CO5,
                ROUND(( {internal_weight} * CTE1.Percentage_CO6 + {external_weight} * CTE2.Percentage_CO6), 2) AS Combined_Score_CO6
            FROM 
                CTE1
            JOIN 
                CTE2 ON CTE1.Student_Reg_No = CTE2.Student_Reg_No AND CTE1.Course_code = CTE2.Course_code
            JOIN 
                STUDENT st ON CTE1.Student_Reg_No = st.Student_Reg_No
            WHERE
                st.Academic_year = '{year}'
                AND st.Semester = '{semester}'
        ),
        CountStudents AS (
            SELECT
                COUNT(*) AS TotalStudents
            FROM
                FinalScores
        ),
    
        CountAboveTarget AS (
            SELECT
                COUNT(*) FILTER (WHERE Combined_Score_CO1 >= {overall_target}) AS StudentsAboveTarget_CO1,
                COUNT(*) FILTER (WHERE Combined_Score_CO2 >= {overall_target}) AS StudentsAboveTarget_CO2,
                COUNT(*) FILTER (WHERE Combined_Score_CO3 >= {overall_target}) AS StudentsAboveTarget_CO3,
                COUNT(*) FILTER (WHERE Combined_Score_CO4 >= {overall_target}) AS StudentsAboveTarget_CO4,
                COUNT(*) FILTER (WHERE Combined_Score_CO5 >= {overall_target}) AS StudentsAboveTarget_CO5,
                COUNT(*) FILTER (WHERE Combined_Score_CO6 >= {overall_target}) AS StudentsAboveTarget_CO6
            FROM
                FinalScores
        )
        SELECT
            ROUND((StudentsAboveTarget_CO1 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO1,
            ROUND((StudentsAboveTarget_CO2 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO2,
            ROUND((StudentsAboveTarget_CO3 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO3,
            ROUND((StudentsAboveTarget_CO4 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO4,
            ROUND((StudentsAboveTarget_CO5 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO5,
            ROUND((StudentsAboveTarget_CO6 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO6
        FROM
            CountAboveTarget, CountStudents
        """

        # Note:- Execute the SQL query
        my_cursor.execute(create_view_query)

        # Note:- Fetch the results
        fetch_results_query = f"""
        SELECT
            Percentage_AboveLevel_CO1,
            Percentage_AboveLevel_CO2,
            Percentage_AboveLevel_CO3,
            Percentage_AboveLevel_CO4,
            Percentage_AboveLevel_CO5,
            Percentage_AboveLevel_CO6
        FROM
            'OVERALL'
        UNION ALL
        SELECT
            CASE
                WHEN Percentage_AboveLevel_CO1 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO1 >= {level_0} AND Percentage_AboveLevel_CO1 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO1 >= {level_1} AND Percentage_AboveLevel_CO1 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO1 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO1,
            CASE
                WHEN Percentage_AboveLevel_CO2 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO2 >= {level_0} AND Percentage_AboveLevel_CO2 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO2 >= {level_1} AND Percentage_AboveLevel_CO2 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO2 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO2,
            CASE
                WHEN Percentage_AboveLevel_CO3 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO3 >= {level_0} AND Percentage_AboveLevel_CO3 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO3 >= {level_1} AND Percentage_AboveLevel_CO3 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO3 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO3,
            CASE 
                WHEN Percentage_AboveLevel_CO4 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO4 >= {level_0} AND Percentage_AboveLevel_CO4 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO4 >= {level_1} AND Percentage_AboveLevel_CO4 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO4 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO4,
            CASE
                WHEN Percentage_AboveLevel_CO5 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO5 >= {level_0} AND Percentage_AboveLevel_CO5 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO5 >= {level_1} AND Percentage_AboveLevel_CO5 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO5 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO5,
            CASE
                WHEN Percentage_AboveLevel_CO6 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO6 >= {level_0} AND Percentage_AboveLevel_CO6 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO6 >= {level_1} AND Percentage_AboveLevel_CO6 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO6 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO6
        FROM
            'OVERALL'
        """

        my_cursor.execute(fetch_results_query)

        rows = my_cursor.fetchall()

        if len(rows) != 0:
            self.report_attainment_treeview.delete(*self.report_attainment_treeview.get_children())
            for i in rows:
                self.report_attainment_treeview.insert("", END, values=i)
            conn.commit()

        conn.close()



    def fetch_internal_exam_records(self, event=None):

        # Note:- Checking and removing the label
        self.remove_current_label()
        self.current_label = Label(self.report_attainment_frame1, text="Internal Attainment report", font=("times new roman", 11, "bold"), fg="Red")
        self.current_label.place(x=400, y=180, width=180)

        label = Label(self.report_attainment_frame1, text="Internal Attainment report",font=("times new roman", 11, "bold"), fg="Red")
        label.place(x=400, y=180, width=180)
        academic_year = self.report_attainment_year.get()
        semester = self.report_attainment_semester.get()
        course_code = self.report_attainment_course_code.get()

        conn = sqlite3.connect('Attainment_record.db')
        my_cursor = conn.cursor()

        fetch_query1 = f"""
        SELECT internal_target
        FROM Target_Variable_Table
        WHERE course_code = '{course_code}'
        """
        my_cursor.execute(fetch_query1)
        row1 = my_cursor.fetchone()

        
        if row1:
            internal_target = row1[0]
        fetch_query2 = f"""
        SELECT level_0, level_1, level_2
        FROM Level_Table
        WHERE course_code = '{course_code}' AND target_type = 'internal'
        """
        my_cursor.execute(fetch_query2)
        row2 = my_cursor.fetchone()

        if row2:
            level_0, level_1, level_2 = row2

        # Note:- Drop the view if it exists
        my_cursor.execute("DROP VIEW IF EXISTS 'INTERNAL EXAM'")

        # Note:- Create the view with parameterized query
        create_view_query = f"""
        CREATE VIEW 'INTERNAL EXAM' AS
        WITH IndividualScores AS (
            SELECT 
                am.Student_Reg_No,
                am.Course_code,
                ROUND((SUM(CASE WHEN am.SCA_No IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO1 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO1 ELSE 0 END)), 2) AS Percentage_CO1,
                ROUND((SUM(CASE WHEN am.SCA_No IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO2 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO2 ELSE 0 END)), 2) AS Percentage_CO2,
                ROUND((SUM(CASE WHEN am.SCA_No IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO3 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO3 ELSE 0 END)), 2) AS Percentage_CO3,
                ROUND((SUM(CASE WHEN am.SCA_No IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO4 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO4 ELSE 0 END)), 2) AS Percentage_CO4,
                ROUND((SUM(CASE WHEN am.SCA_No IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO5 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO5 ELSE 0 END)), 2) AS Percentage_CO5,
                ROUND((SUM(CASE WHEN am.SCA_No IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO6 ELSE 0 END) * 100.0 / SUM(CASE WHEN qm.Exam_Name IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO6 ELSE 0 END)), 2) AS Percentage_CO6
            FROM 
                ANSWER_MARK am
            JOIN 
                QUESTION_MARK qm ON am.Course_code = qm.Course_code AND am.SCA_No = qm.Exam_Name
            JOIN 
                STUDENT st ON am.Student_Reg_No = st.Student_Reg_No
            WHERE  
                st.Academic_year = '{academic_year}'
                AND am.Course_code = '{course_code}'
                AND st.Semester = '{semester}'
            GROUP BY 
                am.Student_Reg_No, am.Course_code
        ),

        CountAboveTarget AS (
            SELECT
                SUM(CASE WHEN Percentage_CO1 >= {internal_target} THEN 1 ELSE 0 END) AS StudentsAboveTarget_CO1,
                SUM(CASE WHEN Percentage_CO2 >= {internal_target} THEN 1 ELSE 0 END) AS StudentsAboveTarget_CO2,
                SUM(CASE WHEN Percentage_CO3 >= {internal_target} THEN 1 ELSE 0 END) AS StudentsAboveTarget_CO3,
                SUM(CASE WHEN Percentage_CO4 >= {internal_target} THEN 1 ELSE 0 END) AS StudentsAboveTarget_CO4,
                SUM(CASE WHEN Percentage_CO5 >= {internal_target} THEN 1 ELSE 0 END) AS StudentsAboveTarget_CO5,
                SUM(CASE WHEN Percentage_CO6 >= {internal_target} THEN 1 ELSE 0 END) AS StudentsAboveTarget_CO6
            FROM
                IndividualScores
        ),
        CountStudents AS (
            SELECT
                COUNT(*) AS TotalStudents
            FROM
                IndividualScores
        )
        SELECT
            ROUND((StudentsAboveTarget_CO1 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO1,
            ROUND((StudentsAboveTarget_CO2 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO2,
            ROUND((StudentsAboveTarget_CO3 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO3,
            ROUND((StudentsAboveTarget_CO4 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO4,
            ROUND((StudentsAboveTarget_CO5 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO5,
            ROUND((StudentsAboveTarget_CO6 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO6
        FROM
            CountAboveTarget, CountStudents
        """
        # Note:- Execute the SQL query
        my_cursor.execute(create_view_query)
        # Note:- Fetch the results
        fetch_results_query = f"""
        SELECT
            Percentage_AboveLevel_CO1,
            Percentage_AboveLevel_CO2,
            Percentage_AboveLevel_CO3,
            Percentage_AboveLevel_CO4,
            Percentage_AboveLevel_CO5,
            Percentage_AboveLevel_CO6
        FROM
            'INTERNAL EXAM'
        UNION ALL
        SELECT
            CASE
                WHEN Percentage_AboveLevel_CO1 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO1 >= {level_0} AND Percentage_AboveLevel_CO1 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO1 >= {level_1} AND Percentage_AboveLevel_CO1 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO1 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO1,
            CASE
                WHEN Percentage_AboveLevel_CO2 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO2 >= {level_0} AND Percentage_AboveLevel_CO2 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO2 >= {level_1} AND Percentage_AboveLevel_CO2 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO2 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO2,
            CASE
                WHEN Percentage_AboveLevel_CO3 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO3 >= {level_0} AND Percentage_AboveLevel_CO3 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO3 >= {level_1} AND Percentage_AboveLevel_CO3 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO3 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO3,
            CASE
                WHEN Percentage_AboveLevel_CO4 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO4 >= {level_0} AND Percentage_AboveLevel_CO4 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO4 >= {level_1} AND Percentage_AboveLevel_CO4 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO4 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO4,
            CASE
                WHEN Percentage_AboveLevel_CO5 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO5 >= {level_0} AND Percentage_AboveLevel_CO5 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO5 >= {level_1} AND Percentage_AboveLevel_CO5 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO5 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO5,
            CASE
                WHEN Percentage_AboveLevel_CO6 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO6 >= {level_0} AND Percentage_AboveLevel_CO6 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO6 >= {level_1} AND Percentage_AboveLevel_CO6 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO6 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO6
        FROM
            'INTERNAL EXAM'
        """

       

        my_cursor.execute(fetch_results_query)

        rows = my_cursor.fetchall()

        if len(rows) != 0:
            self.report_attainment_treeview.delete(*self.report_attainment_treeview.get_children())
            for i in rows:
                self.report_attainment_treeview.insert("", END, values=i)
            conn.commit()

        conn.close()




    def fetch_final_exam_records(self, event=None):
        
        # Note:- Checking and removing the label
        self.remove_current_label()
        self.current_label = Label(self.report_attainment_frame1, text="Final Attainment report", font=("times new roman", 11, "bold"), fg="Red")
        self.current_label.place(x=400, y=180, width=180)

        academic_year = self.report_attainment_year.get()
        semester = self.report_attainment_semester.get()
        course_code = self.report_attainment_course_code.get()

        conn = sqlite3.connect('Attainment_record.db')
        my_cursor = conn.cursor()
        fetch_query1 = f"""
        SELECT final_target
        FROM Target_Variable_Table
        WHERE course_code = '{course_code}'
        """
        my_cursor.execute(fetch_query1)
        row1 = my_cursor.fetchone()

        
        if row1:
            final_target = row1[0]
        fetch_query2 = f"""
        SELECT level_0, level_1, level_2
        FROM Level_Table
        WHERE course_code = '{course_code}' AND target_type = 'final'
        """
        my_cursor.execute(fetch_query2)
        row2 = my_cursor.fetchone()

        if row2:
            level_0, level_1, level_2 = row2
       

        my_cursor.execute("DROP VIEW IF EXISTS 'FINAL EXAM'")
        # Note:- Create the view with parameterized query
        create_view_query = f"""
        CREATE VIEW 'FINAL EXAM' AS
        WITH IndividualScores AS (
            SELECT 
                am.Student_Reg_No,
                am.Course_code,
                ROUND((SUM(CASE WHEN am.SCA_No NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO1 ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN qm.Exam_Name NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO1 ELSE 0 END), 0)), 2) AS Percentage_CO1,
                ROUND((SUM(CASE WHEN am.SCA_No NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO2 ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN qm.Exam_Name NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO2 ELSE 0 END), 0)), 2) AS Percentage_CO2,
                ROUND((SUM(CASE WHEN am.SCA_No NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO3 ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN qm.Exam_Name NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO3 ELSE 0 END), 0)), 2) AS Percentage_CO3,
                ROUND((SUM(CASE WHEN am.SCA_No NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO4 ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN qm.Exam_Name NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO4 ELSE 0 END), 0)), 2) AS Percentage_CO4,
                ROUND((SUM(CASE WHEN am.SCA_No NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO5 ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN qm.Exam_Name NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO5 ELSE 0 END), 0)), 2) AS Percentage_CO5,
                ROUND((SUM(CASE WHEN am.SCA_No NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN am.Score_CO6 ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN qm.Exam_Name NOT IN (' CA 1 ', ' CA 2 ', ' CA 3 ', ' CA 4 ') THEN qm.QuCO6 ELSE 0 END), 0)), 2) AS Percentage_CO6
            FROM 
                ANSWER_MARK am
            JOIN 
                QUESTION_MARK qm ON am.Course_code = qm.Course_code AND am.SCA_No = qm.Exam_Name
            JOIN 
                STUDENT st ON am.Student_Reg_No = st.Student_Reg_No
            WHERE  
                st.Academic_year = '{academic_year}'
                AND am.Course_code = '{course_code}'
                AND st.Semester = '{semester}'
            GROUP BY 
                am.Student_Reg_No, am.Course_code
        ),

        CountAboveTarget AS (
            SELECT
                SUM(CASE WHEN Percentage_CO1 >= {final_target} THEN 1 ELSE 0 END) AS StudentsAboveTarget_CO1,
                SUM(CASE WHEN Percentage_CO2 >= {final_target} THEN 1 ELSE 0 END) AS StudentsAboveTarget_CO2,
                SUM(CASE WHEN Percentage_CO3 >= {final_target} THEN 1 ELSE 0 END) AS StudentsAboveTarget_CO3,
                SUM(CASE WHEN Percentage_CO4 >= {final_target} THEN 1 ELSE 0 END) AS StudentsAboveTarget_CO4,
                SUM(CASE WHEN Percentage_CO5 >= {final_target} THEN 1 ELSE 0 END) AS StudentsAboveTarget_CO5,
                SUM(CASE WHEN Percentage_CO6 >= {final_target} THEN 1 ELSE 0 END) AS StudentsAboveTarget_CO6
            FROM
                IndividualScores
        ),
        CountStudents AS (
            SELECT
                COUNT(*) AS TotalStudents
            FROM
                IndividualScores
        )
        SELECT
            ROUND((StudentsAboveTarget_CO1 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO1,
            ROUND((StudentsAboveTarget_CO2 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO2,
            ROUND((StudentsAboveTarget_CO3 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO3,
            ROUND((StudentsAboveTarget_CO4 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO4,
            ROUND((StudentsAboveTarget_CO5 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO5,
            ROUND((StudentsAboveTarget_CO6 * 100.0 / TotalStudents), 2) AS Percentage_AboveLevel_CO6
        FROM
            CountAboveTarget, CountStudents
        """

        # Note:- Execute the SQL query
        my_cursor.execute(create_view_query)
        # Note:- Fetch the results
        fetch_results_query3 = f"""
        SELECT
            Percentage_AboveLevel_CO1,
            Percentage_AboveLevel_CO2,
            Percentage_AboveLevel_CO3,
            Percentage_AboveLevel_CO4,
            Percentage_AboveLevel_CO5,
            Percentage_AboveLevel_CO6
        FROM
            'FINAL EXAM'
        UNION ALL
        SELECT
            CASE
                WHEN Percentage_AboveLevel_CO1 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO1 >= {level_0} AND Percentage_AboveLevel_CO1 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO1 >= {level_1} AND Percentage_AboveLevel_CO1 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO1 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO1,
            CASE
                WHEN Percentage_AboveLevel_CO2 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO2 >= {level_0} AND Percentage_AboveLevel_CO2 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO2 >= {level_1} AND Percentage_AboveLevel_CO2 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO2 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO2,
            CASE
                WHEN Percentage_AboveLevel_CO3 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO3 >= {level_0} AND Percentage_AboveLevel_CO3 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO3 >= {level_1} AND Percentage_AboveLevel_CO3 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO3 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO3,
            CASE
                WHEN Percentage_AboveLevel_CO4 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO4 >= {level_0} AND Percentage_AboveLevel_CO4 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO4 >= {level_1} AND Percentage_AboveLevel_CO4 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO4 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO4,
            CASE
                WHEN Percentage_AboveLevel_CO5 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO5 >= {level_0} AND Percentage_AboveLevel_CO5 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO5 >= {level_1} AND Percentage_AboveLevel_CO5 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO5 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO5,
            CASE
                WHEN Percentage_AboveLevel_CO6 <  {level_0} THEN 'Level 0'
                WHEN Percentage_AboveLevel_CO6 >= {level_0} AND Percentage_AboveLevel_CO6 < 70 THEN 'Level 1'
                WHEN Percentage_AboveLevel_CO6 >= {level_1} AND Percentage_AboveLevel_CO6 < 80 THEN 'Level 2'
                WHEN Percentage_AboveLevel_CO6 >= {level_2} THEN 'Level 3'
                ELSE NULL  -- Handle any unexpected cases
            END AS Percentage_AboveLevel_CO6
        FROM
            'FINAL EXAM'
        """

        my_cursor.execute(fetch_results_query3)

        rows = my_cursor.fetchall()

        if len(rows) != 0:
            self.report_attainment_treeview.delete(*self.report_attainment_treeview.get_children())
            for i in rows:
                self.report_attainment_treeview.insert("", END, values=i)
            conn.commit()

        conn.close()

# Note:-:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Note:- This function helps to exit from the main window(important main function)
    def Exit(self):
        # Note:- self.main_window.destroy()
        Exit=messagebox.askyesno("Attainment ","Confirm we want to Exit")
        if Exit>0:
            self.main_window.destroy()
            return 


if __name__=="__main__":
    main_window=Tk()
    ob=Attainment(main_window)
    main_window.mainloop()

                                        # Note:-  <<< MAIN CODE END >>> 