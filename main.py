# import required libraries
import tkinter
import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from tkcalendar import Calendar
from datetime import date
import random
from datetime import datetime, timedelta
import customtkinter
import smtplib
from email.message import EmailMessage
import ssl
import re
import os


# class for help menu hover functionality
class HoverInfo(Menu):
    def __init__(self, parent, text, command=None):
       self._com = command
       Menu.__init__(self,parent, tearoff=0)
       if not isinstance(text, str):
          raise TypeError('Trying to initialise a Hover Menu with a non string type: ' + text.__class__.__name__)
       toktext=re.split('\n', text)
       for t in toktext:
          self.add_command(label = t)
       self._displayed=False
       self.master.bind("<Enter>",self.Display )
       self.master.bind("<Leave>",self.Remove )


    def Display(self,event):
       if not self._displayed:
          self._displayed=True
          self.post(event.x_root, event.y_root)
       if self._com != None:
          self.master.unbind_all("<Return>")
          self.master.bind_all("<Return>", self.Click)

    def Remove(self, event):
     if self._displayed:
       self._displayed=False
       self.unpost()
     if self._com != None:
       self.unbind_all("<Return>")

    def Click(self, event):
       self._com()

# set all theme and characteristics of user interface
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")
root = customtkinter.CTk()
root.title("SFHS Tracker")
root.geometry("1000x700")
root.minsize(1000, 700)
root.maxsize(1000, 700)

# connect to SQL database
mydb = mysql.connector.connect(host="127.0.0.1", user="root", password="KrishnaK123", database="pythonlogin")
mycursor = mydb.cursor()
mydb.autocommit = True

# global variables
user_name = ""
adminID = tkinter.StringVar()
adminPass = tkinter.StringVar()
studentID = tkinter.StringVar()
studentPass = tkinter.StringVar()
logo = Frame(root, borderwidth=0, bg='black')
logo.pack(side=TOP, fill="x")
img = ImageTk.PhotoImage(Image.open("assets/SFHSlogo.png"))
logo_display = Label(logo, image=img)
home_icon = PhotoImage(file=r"assets\home.png")
home_image = home_icon.subsample(7, 7)
events_icon = PhotoImage(file=r"assets\calendar.png")
events_image = events_icon.subsample(7, 7)
rank_icon = PhotoImage(file=r"assets\leaderboard.png")
rank_image = rank_icon.subsample(7, 7)
bell_icon = PhotoImage(file=r"assets\bell.png")
bell_image = bell_icon.subsample(7, 7)
add_icon = PhotoImage(file=r"assets\download.png")
add_image = add_icon.subsample(7, 7)
settings_icon = PhotoImage(file=r"assets\settings.png")
settings_image = settings_icon.subsample(7, 7)
ninth_sort = []
tenth_sort = []
eleven_sort = []
twelve_sort = []
help_mode = customtkinter.StringVar(value="off")
start_am = True
end_am = True
mycursor.execute("select * from settings")
records = mycursor.fetchall()
disable_login = customtkinter.StringVar(value=records[0][1])
disable_leaderboard = customtkinter.StringVar(value=records[1][1])
disable_message = customtkinter.StringVar(value=records[2][1])


# function called to back up data whenever change is made or admin clicks backup button
def backup_data():
  current_datetime = str(datetime.today().replace(microsecond=0)).replace(" ", "_").replace(":", "-")
  file_name = "C:/Users/krish/PycharmProjects/CodingProgramming2023/backup_files/"+current_datetime+".txt"
  f = open(file_name, "w")
  table_list = ["admin_notifications", "adminlogin", "awards", "events", "registered", "student_notifications", "studentlogin"]
  for table in table_list:
    f.write(("TABLE: " + table + "\n"))
    mycursor.execute(str("DESCRIBE " + table))
    backup_rows = mycursor.fetchall()
    f.write("COLUMNS: ")
    for i in backup_rows:
      f.write(("(" + i[0] + ") "))
    f.write("\n")
    mycursor.execute(str("select * from " + table))
    backup_rows = mycursor.fetchall()
    for i in backup_rows:
      f.write(str(i))
      f.write("\n")
    f.write("\n")


# function called to assign widget to hover text
def help_labels(help_bool, *widget_to_text):
  if help_bool == "on":
    for hover_text in widget_to_text:
      HoverInfo(hover_text[0], hover_text[1])
  else:
    for hover_text in widget_to_text:
      hover_text[0].unbind("<Enter>")
      hover_text[0].unbind("<Leave>")


# function called whenever a new page is loaded to populate navigation icons for admins
def nav_bar(current_page):
  home_button = customtkinter.CTkButton(root, image=home_image, text="Home", compound='top',command=lambda: [clear_frame(), admin_home()])
  home_button.place(x=0, y=150)
  event_button = customtkinter.CTkButton(root, image=events_image, text="Events", compound='top',command=lambda: [clear_frame(), events_page()])
  event_button.place(x=0, y=260)
  bell_button = customtkinter.CTkButton(root, image=bell_image, text="Notifications", compound='top',command=lambda: [clear_frame(), message_page()])
  bell_button.place(x=0, y=370)
  student_control_button = customtkinter.CTkButton(root, image=add_image, text="Student Control", compound='top',command=lambda: [clear_frame(), account_page()])
  student_control_button.place(x=0, y=480)
  settings_button = customtkinter.CTkButton(root, image=settings_image, text="Settings", compound='top',command=lambda: [clear_frame(), settings_page()])
  settings_button.place(x=0, y=590)
  string_to_page = {"home": home_button, "event": event_button, "bell": bell_button, "student": student_control_button, "settings": settings_button}
  string_to_page[current_page].config(command=None)
  signout = customtkinter.CTkButton(text='Sign Out', command=lambda: [clear_frame(), loginpage()]).place(x=840, y=20)
  hello_text = customtkinter.CTkLabel(root, text=user_name, fg='black', bg='blue', text_font=("Times New Roman", 15, "bold")).place(x=0, y=0)
  program_name = customtkinter.CTkLabel(root, text="SFHS Tracker", bg='blue', fg='white', text_font=("Times New Roman", 45, "bold")).place(x=310, y=0)


# function called whenever a new page is loaded to populate navigation icons for students
def program_defaults():
  signout = customtkinter.CTkButton(text='Sign Out', command=lambda: [clear_frame(), loginpage()]).place(x=840, y=20)
  hello_text = customtkinter.CTkLabel(root, text=user_name, fg='black', bg='blue', text_font=("Times New Roman", 15, "bold")).place(x=20, y=0)
  program_name = customtkinter.CTkLabel(root, text="SFHS Tracker", bg='blue', fg='white', text_font=("Times New Roman", 45, "bold")).place(x=310, y=0)
  customtkinter.CTkButton(root, image=home_image, text="Home", compound='top', corner_radius=20, command=lambda: [clear_frame(), student_home()]).place(x=20, y=30)
  customtkinter.CTkButton(root, image=bell_image, text="Notifications", compound='top', corner_radius=20, command=lambda: [clear_frame(), student_message_page()]).place(x=20, y=550)
  request = "select * from studentlogin where name = " + "\'" + user_name + "\'"
  mycursor.execute(request)
  records = mycursor.fetchall()
  if records[0][-1] is None:
    prize = "None"
  else:
    prize = records[0][-1]
  points = records[0][-2]
  request = "SELECT * FROM studentlogin WHERE grade=" + "\'" + str(records[0][-3]) + "\'" + "ORDER BY score DESC"
  rank = 1
  mycursor.execute(request)
  records = mycursor.fetchall()
  for i in range(len(records)):
    if records[i][-2] != points:
      rank += 1
    else:
      break
  profile_frame = customtkinter.CTkFrame(root, width=150, height=300, corner_radius=20)
  profile_frame.place(x=20, y=220)
  customtkinter.CTkLabel(root, text="Profile", text_font=("Times New Roman", 20, "bold")).place(
    x=20, y=170)
  customtkinter.CTkLabel(profile_frame, text="Grade: " + str(records[0][-3]), text_font=("Times New Roman", 15, "bold")).place(x=10, y=50)
  customtkinter.CTkLabel(profile_frame, text="Prize: " + prize, text_font=("Times New Roman", 15, "bold")).place(x=10, y=100)
  customtkinter.CTkLabel(profile_frame, text="Points: " + str(records[0][-2]), text_font=("Times New Roman", 15, "bold")).place(x=10, y=150)
  customtkinter.CTkLabel(profile_frame, text="Rank: " + str(rank), text_font=("Times New Roman", 15, "bold")).place(x=10, y=200)
  leaderboard_button = customtkinter.CTkButton(profile_frame, text="Leaderboard", command=lambda: [leaderboard_tracker()])
  if disable_leaderboard.get() == "True": leaderboard_button.configure(state="disabled")
  leaderboard_button.place(x=5, y=250)


# clears notifications from user who clicks button
def clearNotifications(notification_box, student=False, student_id=False):
  notification_box.configure(state="normal")
  notification_box.delete("1.0", "end")
  if not student:
    mycursor.execute("DELETE FROM admin_notifications")
  else:
    request = "DELETE FROM student_notifications WHERE recipient_id = " + str(student_id)
    mycursor.execute(request)
  notification_box.configure(state="disabled")


# sends email to recipient
def send_email(email, recipient, subject, body):
  if email == 'on':
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "sfhstracker@gmail.com"
    msg['To'] = recipient
    msg.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
      smtp.login("sfhstracker@gmail.com", "ponmtekdjlwbcygr")
      smtp.sendmail("sfhstracker@gmail.com", recipient, msg.as_string())


# sends notification to recipient
def send_notification(notify, recipient, subject, body):
  if notify == "on":
    request = "INSERT INTO student_notifications (recipient_id, subject, body) VALUES (" + str(recipient) + ", '" + subject + "', '" + body + "')"
    mycursor.execute(request)


# sends message to administrators from student
def student_send_message(email, notify, subject, body, sender):
  if notify == "on":
    request = "INSERT INTO admin_notifications (sender, subject, body) VALUES ('" + sender + "', '" + subject + "', '" + body + "')"
    mycursor.execute(request)
  send_email(email, "krishnatkocherla@gmail.com", subject, body)
  send_email(email, "sfhstracker@gmail.com", subject, body)


# sends message to student from administrators
def send_message(email, notify, grades, events, recipient, subject, body):  # student does not send grades, events, or recipient
  if recipient != "":
    mycursor.execute("SELECT * FROM studentlogin WHERE email ='" + recipient + "'")
    results = mycursor.fetchall()
    if len(results) > 0:
      send_email(email, recipient, subject, body)
      send_notification(notify, results[0][0], subject, body)
    mycursor.execute("SELECT * FROM studentlogin WHERE id ='" + recipient + "'")
    results = mycursor.fetchall()
    if len(results) > 0:
      send_email(email, results[0][3], subject, body)
      send_notification(notify, recipient, subject, body)
    mycursor.execute("SELECT * FROM studentlogin WHERE name ='" + recipient + "'")
    results = mycursor.fetchall()
    if len(results) > 0:
      send_email(email, results[0][3], subject, body)
      send_notification(notify, results[0][0], subject, body)
  else:
    if grades != "All Grades":
      request = "SELECT * FROM studentlogin WHERE grade ='" + grades + "'"
      mycursor.execute(request)
    else:
      mycursor.execute("SELECT * FROM studentlogin")
    results = mycursor.fetchall()
    if events == "All Events":
      for i in results:
        send_email(email, i[3], subject, body)
        send_notification(notify, i[0], subject, body)
    else:
      request1 = "SELECT * FROM registered WHERE event_name ='" + events + "'"
      mycursor.execute(request1)
      results1 = mycursor.fetchall()
      for i in results:
        for j in results1:
          if i[1] == j[0]:
            send_email(email, i[3], subject, body)
            send_notification(notify, i[0], subject, body)


# converts time to database required format
def to_period(full_time):
  if full_time is None:
    return None
  full_time = str(full_time)
  full_time = full_time[:len(full_time)-3]
  full_time = datetime.strptime(full_time, "%H:%M")
  full_time = full_time.strftime("%I:%M %p")
  return full_time


# checks if time format is valid
def is_time_format(time_input):
  try:
    datetime.strptime(time_input, '%H:%M')
    return True
  except ValueError:
    return False


# clears frame whenever page is changed
def clear_frame():
  for widgets in root.winfo_children():
    widgets.destroy()


# unregisters student from event
def unregister_event(id_given):
  sql_select_query = "DELETE FROM registered WHERE student_name = \"" + user_name + "\" and event_name =\"" + id_given + "\""
  mycursor.execute(sql_select_query)


# deletes event from database
def delete_event(id_given):
  sql_query = "delete from events where name = \"" + id_given + "\"" # DELETE FROM REGISTEREDEVENTS TABLE AS WELL
  mycursor.execute(sql_query)


# changes tab in event viewer
def change_tab(tab_number, event_panel, event_list, button_command, button_name):
  for widget in event_panel.winfo_children():
    widget.destroy()
  y_place = -20
  for index in range(1, len(event_list) + 1):
    if (index < 5 * (tab_number - 1) + 1) or (index > 5 * tab_number):
      continue
    e = customtkinter.CTkLabel(event_panel, text=event_list[index - 1][0], width=30, anchor="w").place(x=0,
                                                                                                       y=y_place + 20)
    e = customtkinter.CTkLabel(event_panel, text=event_list[index - 1][1], width=10, anchor="w").place(x=150,
                                                                                                       y=y_place + 20)
    e = customtkinter.CTkLabel(event_panel, text=to_period(event_list[index - 1][2]), width=10, anchor="w").place(
      x=250,
      y=y_place + 20)
    e = customtkinter.CTkLabel(event_panel, text=to_period(event_list[index - 1][3]), width=10, anchor="w").place(
      x=325,
      y=y_place + 20)
    e = customtkinter.CTkLabel(event_panel, text=event_list[index - 1][4], width=20, anchor="w").place(x=400,
                                                                                                       y=y_place + 20)
    e = customtkinter.CTkLabel(event_panel, text=event_list[index - 1][5], anchor="w").place(x=500, y=y_place + 20)
    e = customtkinter.CTkButton(event_panel, text=button_name, command=lambda d=event_list[index - 1][0]: button_command(d)).place(x=590, y=y_place + 20 + 3)
    y_place += 30


# generates leaderboard window
def leaderboard_tracker():
  # creates the general frame of the new window and components (such as scrollbar)
  demo = customtkinter.CTk()
  demo.title("Leaderboard")
  demo.geometry("760x500")
  demo.minsize(760, 500)
  demo.maxsize(760, 500)
  main_frame = customtkinter.CTkFrame(demo)
  main_frame.pack(fill=BOTH, expand=1)

  new_canvas = customtkinter.CTkCanvas(main_frame, borderwidth=0, highlightthickness=0, bg='#2B2C2E')
  new_canvas.pack(side=LEFT, fill=BOTH, expand=1)

  my_scrollbar = customtkinter.CTkScrollbar(main_frame, orientation=VERTICAL, command=new_canvas.yview)
  my_scrollbar.pack(side=RIGHT, fill=Y)

  new_canvas.configure(yscrollcommand=my_scrollbar.set)
  new_canvas.bind('<Configure>', lambda e: new_canvas.configure(scrollregion=new_canvas.bbox("all")))

  second_frame = customtkinter.CTkFrame(new_canvas)
  new_canvas.create_window((0, 0), window=second_frame, anchor="nw")

  # shows all the students in the database in 9th grade
  mycursor.execute("SELECT * FROM studentlogin WHERE grade=9 ORDER BY score DESC")
  ninth_label = customtkinter.CTkLabel(second_frame, text="9th Grade", fg='black',
                                       text_font=("Times New Roman", 30, "bold"))
  ninth_label.grid(row=0, column=3, sticky='w')
  e = customtkinter.CTkLabel(second_frame, text='ID')
  e.grid(row=1, column=0)
  e = customtkinter.CTkLabel(second_frame, text='Name')
  e.grid(row=1, column=1)
  e = customtkinter.CTkLabel(second_frame, text='Email')
  e.grid(row=1, column=3)
  e = customtkinter.CTkLabel(second_frame, text='Score')
  e.grid(row=1, column=5)
  e = customtkinter.CTkLabel(second_frame, text='Award')
  e.grid(row=1, column=6)
  i = 2
  for student in mycursor:
    for j in range(len(student)):
      if j == 2 or j == 4:
        continue
      if student[j] is not None:
        if (j == 1) or (j == 3):
          e = customtkinter.CTkLabel(second_frame, width=40, text=student[j])
        else:
          e = customtkinter.CTkLabel(second_frame, width=10, text=student[j])
        e.grid(row=i, column=j)
      else:
        e = customtkinter.CTkLabel(second_frame, width=10, text="None")
        e.grid(row=i, column=j)
    i = i + 1

  # shows all the students in the database in 10th grade
  ten_label = customtkinter.CTkLabel(second_frame, text="10th Grade", fg='black',
                                     text_font=("Times New Roman", 30, "bold"))
  ten_label.grid(row=i + 1, column=3, sticky='w')
  e = customtkinter.CTkLabel(second_frame, text='ID')
  e.grid(row=i + 2, column=0)
  e = customtkinter.CTkLabel(second_frame, text='Name')
  e.grid(row=i + 2, column=1)
  e = customtkinter.CTkLabel(second_frame, text='Email')
  e.grid(row=i + 2, column=3)
  e = customtkinter.CTkLabel(second_frame, text='Score')
  e.grid(row=i + 2, column=5)
  e = customtkinter.CTkLabel(second_frame, text='Award')
  e.grid(row=i + 2, column=6)
  i += 3
  mycursor.execute("SELECT * FROM studentlogin WHERE grade=10 ORDER BY score DESC")
  for student in mycursor:
    for j in range(len(student)):
      if j == 2 or j == 4:
        continue
      if student[j] is not None:
        if (j == 1) or (j == 3):
          e = customtkinter.CTkLabel(second_frame, width=40, text=student[j])
        else:
          e = customtkinter.CTkLabel(second_frame, width=10, text=student[j])
        e.grid(row=i, column=j)
      else:
        e = customtkinter.CTkLabel(second_frame, width=10, text="None")
        e.grid(row=i, column=j)
    i = i + 1

  # shows all the students in the database in 10th grade
  eleven_label = customtkinter.CTkLabel(second_frame, text="11th Grade", fg='black',
                                        text_font=("Times New Roman", 30, "bold"))
  eleven_label.grid(row=i + 1, column=3, sticky='w')
  e = customtkinter.CTkLabel(second_frame, text='ID')
  e.grid(row=i + 2, column=0)
  e = customtkinter.CTkLabel(second_frame, text='Name')
  e.grid(row=i + 2, column=1)
  e = customtkinter.CTkLabel(second_frame, text='Email')
  e.grid(row=i + 2, column=3)
  e = customtkinter.CTkLabel(second_frame, text='Score')
  e.grid(row=i + 2, column=5)
  e = customtkinter.CTkLabel(second_frame, text='Award')
  e.grid(row=i + 2, column=6)
  i += 3
  mycursor.execute("SELECT * FROM studentlogin WHERE grade=11 ORDER BY score DESC")
  for student in mycursor:
    for j in range(len(student)):
      if j == 2 or j == 4:
        continue
      if student[j] is not None:
        if (j == 1) or (j == 3):
          e = customtkinter.CTkLabel(second_frame, width=40, text=student[j])
        else:
          e = customtkinter.CTkLabel(second_frame, width=10, text=student[j])
        e.grid(row=i, column=j)
      else:
        e = customtkinter.CTkLabel(second_frame, width=10, text="None")
        e.grid(row=i, column=j)
    i = i + 1

  # shows all the students in the database in 10th grade
  twelve_label = customtkinter.CTkLabel(second_frame, text="12th Grade", fg='black',
                                        text_font=("Times New Roman", 30, "bold"))
  twelve_label.grid(row=i + 1, column=3, sticky='w')
  e = customtkinter.CTkLabel(second_frame, text='ID')
  e.grid(row=i + 2, column=0)
  e = customtkinter.CTkLabel(second_frame, text='Name')
  e.grid(row=i + 2, column=1)
  e = customtkinter.CTkLabel(second_frame, text='Email')
  e.grid(row=i + 2, column=3)
  e = customtkinter.CTkLabel(second_frame, text='Score')
  e.grid(row=i + 2, column=5)
  e = customtkinter.CTkLabel(second_frame, text='Award')
  e.grid(row=i + 2, column=6)
  i += 3
  mycursor.execute("SELECT * FROM studentlogin WHERE grade=12 ORDER BY score DESC")
  for student in mycursor:
    for j in range(len(student)):
      if j == 2 or j == 4:
        continue
      if student[j] is not None:
        if (j == 1) or (j == 3):
          e = customtkinter.CTkLabel(second_frame, width=40, text=student[j])
        else:
          e = customtkinter.CTkLabel(second_frame, width=10, text=student[j])
        e.grid(row=i, column=j)
      else:
        e = customtkinter.CTkLabel(second_frame, width=10, text="None")
        e.grid(row=i, column=j)
    i = i + 1

  demo.mainloop()


# imports event added by admin into database
def event_to_database(date_picked, name, location, start, end, points):
  global start_am
  global end_am
  if name == "":
    messagebox.showerror('Invalid Entry', 'Name should not be empty')
    start_am = True
    end_am = True
    return
  try:
    points = int(points)
  except ValueError:
    messagebox.showerror('Invalid Entry', 'Points should have an integer input')
    start_am = True
    end_am = True
    return
  if name == "":
    name = None
  if location == "":
    location = None
  if start != "" and not is_time_format(start):
    messagebox.showerror('Invalid Entry', 'Start time should be correct format')
    start_am = True
    end_am = True
    return
  elif start == "":
    start = None
  elif start_am:
    start += "AM"
    if int(start.partition(":")[0]) + 12 > 24:
      messagebox.showerror('Invalid Entry', 'Times should be correct format')
      return
  else:
    start += "PM"
    if int(start.partition(":")[0]) + 12 > 24:
      messagebox.showerror('Invalid Entry', 'Times should be correct format')
      return
    start = start.replace(start.partition(":")[0], str(int(start.partition(":")[0]) + 12))
  if end != "" and not is_time_format(end):
    messagebox.showerror('Invalid Entry', 'End time should be correct format')
    start_am = True
    end_am = True
    return
  elif end == "":
    end = None
  elif end_am:
    end += "AM"
    if int(end.partition(":")[0]) + 12 > 24:
      messagebox.showerror('Invalid Entry', 'Times should be correct format')
      return
  else:
    end += "PM"
    if int(end.partition(":")[0]) + 12 > 24:
      messagebox.showerror('Invalid Entry', 'Times should be correct format')
      return
    end = end.replace(end.partition(":")[0], str(int(end.partition(":")[0]) + 12))
  check1 = """INSERT IGNORE INTO events (name, day, start_time, end_time, location, point_value) VALUES (%s, %s, %s, %s, %s, %s)"""
  mycursor.execute(check1, (name, date_picked, start, end, location, points))
  start_am = True
  end_am = True


# creates the add event screen
def add_event(date_picked):
  # normalizes the date and time values for no syntax errors during database changes
  date_picked = date_picked.replace("/", "-")
  date_picked = date_picked[:-2] + "20" + date_picked[-2:]
  date_picked = datetime.strptime(date_picked, '%m-%d-%Y')
  datetime.strftime(date_picked, "YYYY-MM-DD")
  date_picked = date_picked.strftime('%Y-%m-%d')
  date_picked.replace(" 00:00:00", "")

  # creates new window to add event characteristics
  addscreen = customtkinter.CTk()
  addscreen.geometry("400x400")
  addscreen.minsize(400, 400)
  addscreen.maxsize(400, 400)
  addscreen.title("Event Creator")

  # switch from am to pm using toggle
  def switch_period(period):
    if period == "start":
      global start_am
      start_am = not start_am
    if period == "end":
      global end_am
      end_am = not end_am
  eventname = customtkinter.StringVar(master=addscreen)
  locationname = customtkinter.StringVar(master=addscreen)
  pointvalue = customtkinter.StringVar(master=addscreen)
  event_label = customtkinter.CTkLabel(addscreen, text="Event Information").place(x=130, y=10)
  event_name_label = customtkinter.CTkLabel(addscreen, text="Name").place(x=40, y=40)
  event_location_label = customtkinter.CTkLabel(addscreen, text="Location").place(x=35, y=110)
  event_name = customtkinter.CTkEntry(addscreen, textvariable=eventname).place(x=130, y=40)
  event_location = customtkinter.CTkEntry(addscreen, textvariable=locationname).place(x=130, y=110)
  customtkinter.CTkLabel(addscreen, text="Points").place(x=40, y=180)
  customtkinter.CTkEntry(addscreen, textvariable=pointvalue).place(x=130, y=180)

  time_label = customtkinter.CTkLabel(addscreen, text="Event Times").place(x=130, y=218)
  start_time_label = customtkinter.CTkLabel(addscreen, text="Start Time").place(x=27, y=245)
  end_time_label = customtkinter.CTkLabel(addscreen, text="End Time").place(x=30, y=335)

  customtkinter.CTkLabel(addscreen, text="AM").place(x=220, y=240)
  customtkinter.CTkLabel(addscreen, text="AM").place(x=220, y=330)
  start_period = customtkinter.CTkSwitch(addscreen, text="PM", command=lambda: [switch_period("start")]).place(x=310, y=245)
  end_period = customtkinter.CTkSwitch(addscreen, text="PM", command=lambda: [switch_period("end")]).place(x=310, y=335)
  end_time = customtkinter.CTkEntry(addscreen, placeholder_text="hh:mm")
  end_time.pack(side=tkinter.BOTTOM, pady=40)
  start_time = customtkinter.CTkEntry(addscreen, placeholder_text="hh:mm")
  start_time.pack(side=tkinter.BOTTOM, pady=20)

  def remove():
    addscreen.destroy()
  make_event = customtkinter.CTkButton(addscreen, text='Add Event', command=lambda: [event_to_database(date_picked, eventname.get(), locationname.get(), start_time.get(), end_time.get(), pointvalue.get()), remove()]).place(x=130, y=370)
  addscreen.mainloop()


# adds points to student score after event is over
def add_points():
  # generates list of all events that are over
  sql_select_query = "select * from events where day < DATE_SUB(NOW() , INTERVAL 1 DAY)"
  mycursor.execute(sql_select_query)
  event_to_point = mycursor.fetchall()
  finished_events = [(i[0], i[5]) for i in event_to_point]
  finished_events = dict(finished_events)

  sql_select_query = "select * from registered"  # all registrations (student, event)
  mycursor.execute(sql_select_query)
  registered_events = mycursor.fetchall()
  # checks every registration to see if points need to be added
  for registration in registered_events:  # add point then delete from registered events if event is over
    if registration[1] in finished_events.keys():
      sql_select_query = "update studentlogin set score = score + " + str(finished_events[registration[1]]) + " where name = " + registration[0]

  sql_select_query = "delete from events where day < DATE_SUB(NOW() , INTERVAL 1 DAY)"
  mycursor.execute(sql_select_query)
  mycursor.execute("SELECT * FROM awards")
  results = mycursor.fetchall()
  threshold_to_award = [(results[1][2], results[1][1]), (results[0][2], results[0][1]), (results[2][2], results[2][1])]
  threshold_to_award.sort()
  mycursor.execute(('update studentlogin set award="' + threshold_to_award[0][1] + '" where score > ' + str(threshold_to_award[0][0])))
  mycursor.execute(('update studentlogin set award="' + threshold_to_award[1][1] + '" where score > ' + str(threshold_to_award[1][0])))
  mycursor.execute(('update studentlogin set award="' + threshold_to_award[2][1] + '" where score > ' + str(threshold_to_award[2][0])))


# initial page for student or admin logins
def loginpage():
  global help_mode
  help_mode = customtkinter.StringVar(value="off")
  # displaying the logo
  user_name = ""
  global img, logo, logo_display
  logo = customtkinter.CTkFrame(root)  # borderwidth=0
  logo.pack(side=TOP)
  img = ImageTk.PhotoImage(Image.open("assets/SFHSlogo.png"))
  logo_display = customtkinter.CTkLabel(logo, image=img)
  logo_display.pack()
  program_name = customtkinter.CTkLabel(root, text="SFHS Tracker", text_font=("Times New Roman", 45, "bold")).place(
    x=310, y=250)

  # send login information to database for verification
  def adminlog():
    check = "SELECT name FROM adminlogin WHERE (id ='" + adminID.get() + "') and (password ='" + adminPass.get() + "')"
    mycursor.execute(check)
    global user_name
    user_name = mycursor.fetchall()
    if len(user_name) > 0:
      user_name = user_name[0][0]
      clear_frame()
      admin_home()
  def studentlog():
    check = "SELECT * FROM studentlogin WHERE (id ='" + studentID.get() + "') and (password ='" + studentPass.get() + "')"
    mycursor.execute(check)
    global user_name
    user_name = mycursor.fetchall()
    if len(user_name) > 0:
      user_name = user_name[0][1]
      clear_frame()
      student_home()
  # displays text and components like entry boxes
  global adminID, adminPass, studentID, studentPass
  adminID = tkinter.StringVar()
  adminPass = tkinter.StringVar()
  studentID = tkinter.StringVar()
  studentPass = tkinter.StringVar()
  # displaying login elements
  admin_login = customtkinter.CTkLabel(root, text="Admin Login", text_font=("Times New Roman", 15, "bold")).place(x=170, y=400)
  student_login = customtkinter.CTkLabel(root, text="Student Login", text_font=("Times New Roman", 15, "bold")).place(x=670, y=400)
  admin_id = customtkinter.CTkLabel(root, text="ID").place(x=90, y=450)
  admin_pass = customtkinter.CTkLabel(root, text="Password").place(x=65, y=500)
  admin_id_entry = customtkinter.CTkEntry(root, textvariable=adminID).place(x=170, y=450)
  admin_pass_entry = customtkinter.CTkEntry(root,   textvariable=adminPass).place(x=170, y=500)
  student_id = customtkinter.CTkLabel(root, text="ID").place(x=590, y=450)
  student_pass = customtkinter.CTkLabel(root, text="Password").place(x=565, y=500)
  student_id_entry = customtkinter.CTkEntry(root,   textvariable=studentID).place(x=670, y=450)
  student_pass_entry = customtkinter.CTkEntry(root,   textvariable=studentPass).place(x=670, y=500)
  adminbutton = customtkinter.CTkButton(root, text='Login', command=adminlog).place(x=170, y=550)
  studentbutton = customtkinter.CTkButton(root, text='Login', command=studentlog)
  if disable_login.get() == "True": studentbutton.configure(state="disabled")
  studentbutton.place(x=670, y=550)


# home page for students
def student_home():
  program_defaults()
  # ALL EVENTS PANEL
  def register_event(id_given):
    sql_select_query = "insert ignore into registered (student_name, event_name) values ('" + user_name + "', \"" + id_given + "\")"
    mycursor.execute(sql_select_query)

  customtkinter.CTkLabel(root, text="All Events", fg='white', bg='blue', text_font=("Times New Roman", 25, "bold")).place(x=310, y=380)

  event_frame = customtkinter.CTkFrame(root, width=750, height=200)
  event_frame.place(x=200, y=450)
  second_event_frame = customtkinter.CTkFrame(event_frame, width=750, height=200)
  second_event_frame.place(x=0, y=25)

  e = customtkinter.CTkLabel(event_frame, text='Name', anchor="w", width=220).place(x=0, y=0)
  e = customtkinter.CTkLabel(event_frame, text='Date', anchor="w").place(x=150, y=0)
  e = customtkinter.CTkLabel(event_frame, text='Start Time', anchor="w").place(x=250, y=0)
  e = customtkinter.CTkLabel(event_frame, text='End Time', anchor="w").place(x=325, y=0)
  e = customtkinter.CTkLabel(event_frame, text='Location', anchor="w", width=300).place(x=400, y=0)
  e = customtkinter.CTkLabel(event_frame, text='Points', anchor="w").place(x=500, y=0)
  add_points()
  sql_select_query = "select * from events ORDER BY day, end_time, start_time"
  mycursor.execute(sql_select_query)
  records = mycursor.fetchall()

  # function which changes tabs for viewing of different events
  def change_tab_reg(tab_number):
    sql_select_query = "select * from events ORDER BY day, end_time, start_time"
    mycursor.execute(sql_select_query)
    records = mycursor.fetchall()
    sql_select_query = "select * from registered where student_name= '" + user_name + "'"
    mycursor.execute(sql_select_query)
    records1 = mycursor.fetchall()
    for widget in second_event_frame.winfo_children():
      widget.destroy()
    y_place = -20
    for index in range(1, len(records) + 1):
      if (index < 5 * (tab_number - 1) + 1) or (index > 5 * tab_number):
        continue
      e = customtkinter.CTkLabel(second_event_frame, text=records[index - 1][0], width=30, anchor="w").place(x=0,
                                                                                                         y=y_place + 20)
      e = customtkinter.CTkLabel(second_event_frame, text=records[index - 1][1], width=10, anchor="w").place(x=150,
                                                                                                         y=y_place + 20)
      e = customtkinter.CTkLabel(second_event_frame, text=to_period(records[index - 1][2]), width=10, anchor="w").place(
        x=250,
        y=y_place + 20)
      e = customtkinter.CTkLabel(second_event_frame, text=to_period(records[index - 1][3]), width=10, anchor="w").place(
        x=325,
        y=y_place + 20)
      e = customtkinter.CTkLabel(second_event_frame, text=records[index - 1][4], width=20, anchor="w").place(x=400,
                                                                                                         y=y_place + 20)
      e = customtkinter.CTkLabel(second_event_frame, text=records[index - 1][5], anchor="w").place(x=500, y=y_place + 20)
      temp_tuple = (user_name, records[index-1][0])
      if temp_tuple not in records1:
        e = customtkinter.CTkButton(second_event_frame, text="Register", command=lambda d=records[index - 1][0]: register_event(d)).place(x=590, y=y_place + 20 + 3)
      y_place += 30

  x_place = 200
  for i in range((len(records) // 5 + (len(records) % 5 > 0))):
    customtkinter.CTkButton(root, text=("Tab " + str(i+1)), command=lambda d=(i+1): change_tab_reg(d)).place(x=x_place, y=420)
    x_place += 150
  change_tab_reg(1)
  # REGISTERED EVENTS PANEL
  customtkinter.CTkLabel(root, text="Registered Events", fg='white', bg='blue',
                         text_font=("Times New Roman", 25, "bold")).place(x=310, y=80)

  event_frame_reg = customtkinter.CTkFrame(root, width=750, height=200)
  event_frame_reg.place(x=200, y=150)
  second_event_frame_reg = customtkinter.CTkFrame(event_frame_reg, width=750, height=195)
  second_event_frame_reg.place(x=0, y=25)
  records_registered = []
  records_all = []
  events_registered = []
  # function which changes tabs for viewing of different events
  def registered_events_list():
    events_registered.clear()
    sql_select_query = "select * from registered where student_name= '" + user_name + "'"
    mycursor.execute(sql_select_query) # all events student registered for
    records_registered = mycursor.fetchall()
    sql_select_query = "select * from events"
    mycursor.execute(sql_select_query)
    records_all = mycursor.fetchall() # all events
    for event in records_all:
      temp_tuple_reg = (user_name, event[0])
      if temp_tuple_reg in records_registered:
        events_registered.append(event) # all events user registered for
  registered_events_list()
  x_place = 200
  for i in range((len(events_registered) // 5 + (len(events_registered) % 5 > 0))): # originally len(records)
    customtkinter.CTkButton(root, text=("Tab " + str(i+1)), command=lambda d=(i+1): [registered_events_list(), change_tab(d, second_event_frame_reg, events_registered, unregister_event, "Unregister")]).place(x=x_place, y=120)
    x_place += 150
  e = customtkinter.CTkLabel(event_frame_reg, text='Name', anchor="w", width=220).place(x=0, y=0)
  e = customtkinter.CTkLabel(event_frame_reg, text='Date', anchor="w").place(x=150, y=0)
  e = customtkinter.CTkLabel(event_frame_reg, text='Start Time', anchor="w").place(x=250, y=0)
  e = customtkinter.CTkLabel(event_frame_reg, text='End Time', anchor="w").place(x=325, y=0)
  e = customtkinter.CTkLabel(event_frame_reg, text='Location', anchor="w", width=300).place(x=400, y=0)
  e = customtkinter.CTkLabel(event_frame_reg, text='Points', anchor="w").place(x=500, y=0)
  change_tab(1, second_event_frame_reg, events_registered, unregister_event, "Unregister")
  student_home_help_dict = {
    "event_frame": "Shows all events in order of date. Each tab holds up to 5 events. Click Register to sign up for an event.",
    "event_frame_reg": "Shows all user-registered events in order of date. Each tab holds up to 5 events. Click Unregister to remove sign up for an event."
  }
  help_switch = customtkinter.CTkSwitch(master=root, text="Help Mode", onvalue="on", offvalue="off", variable=help_mode, command=lambda: help_labels(help_switch.get(), (event_frame, student_home_help_dict["event_frame"]),(event_frame_reg, student_home_help_dict["event_frame_reg"])))
  help_switch.place(x=840, y=80)
  if help_switch.get() == "on":
    help_labels(help_switch.get(), (
    event_frame, student_home_help_dict["event_frame"]),
    (event_frame_reg, student_home_help_dict["event_frame_reg"])
    )


# messaging page for students
def student_message_page():
  program_defaults()
  customtkinter.CTkLabel(root, text="Message", text_font=("Times New Roman", 20, "bold")).place(x=300, y=100)
  student_main_message_frame = customtkinter.CTkFrame(root, width=300, height=490, corner_radius=10)
  student_main_message_frame.place(x=230, y=150)
  student_message_frame = customtkinter.CTkFrame(student_main_message_frame, width=300, height=490, corner_radius=10)
  student_message_frame.place(x=10, y=230)
  student_message_box = customtkinter.CTkTextbox(master=student_message_frame, width=270, height=220)
  student_message_box.pack(side=LEFT, expand=1, fill=BOTH)
  student_message_bar = customtkinter.CTkScrollbar(student_message_frame, orientation=VERTICAL, command=student_message_box.yview)
  student_message_bar.pack(side=RIGHT, fill=Y)
  student_message_box.configure(yscrollcommand=student_message_bar.set)
  student_message_box.bind('<Configure>', lambda: student_message_box.configure(scrollregion=student_message_box.bbox("all")))
  student_body_label = customtkinter.CTkLabel(student_main_message_frame, text="Body").place(x=85, y=200)
  student_email_bool = tkinter.StringVar(value="off")
  student_notify_bool = tkinter.StringVar(value="off")
  student_subject = tkinter.StringVar()
  student_subject_label = customtkinter.CTkLabel(student_main_message_frame, text="Subject").place(x=85, y=140)
  student_subject_entry = customtkinter.CTkEntry(student_main_message_frame, textvariable=student_subject).place(x=85, y=170)
  student_email_checkbox = customtkinter.CTkCheckBox(student_main_message_frame, text="Email", variable=student_email_bool, onvalue="on", offvalue="off").place(x=0, y=0)
  student_notify_checkbox = customtkinter.CTkCheckBox(student_main_message_frame, text="Notify", variable=student_notify_bool, onvalue="on", offvalue="off").place(x=0, y=30)

  def disable_options():
    student_email_bool.set("off")
    student_notify_bool.set("off")
    student_subject.set("")
    student_message_box.delete("1.0", "end")

  send_message_button = customtkinter.CTkButton(student_main_message_frame, text="Send", command=lambda: [student_send_message(student_email_bool.get(), student_notify_bool.get(), student_subject.get(), student_message_box.get(1.0, "end-1c"), user_name), disable_options()])
  if disable_message.get() == "True": send_message_button.configure(state="disabled")
  send_message_button.place(x=85, y=460)

  customtkinter.CTkLabel(root, text="Notifications", text_font=("Times New Roman", 20, "bold")).place(x=700, y=100)
  main_notification_frame = customtkinter.CTkFrame(root, width=400, height=490, corner_radius=10)
  main_notification_frame.place(x=550, y=150)
  notification_frame = customtkinter.CTkFrame(main_notification_frame, width=350, height=430, corner_radius=10)
  notification_frame.place(x=20, y=50)
  notification_box = customtkinter.CTkTextbox(master=notification_frame, width=350, height=430)
  notification_box.pack(side=LEFT, expand=1, fill=BOTH)
  notification_bar = customtkinter.CTkScrollbar(notification_frame, orientation=VERTICAL, command=notification_box.yview)
  notification_bar.pack(side=RIGHT, fill=Y)
  notification_box.configure(yscrollcommand=notification_bar.set)
  notification_box.bind('<Configure>', lambda: notification_box.configure(scrollregion=notification_box.bbox("all")))
  request = "SELECT * FROM student_notifications WHERE recipient_id = '" + studentID.get() + "'"
  mycursor.execute(request)
  results = mycursor.fetchall()
  for i in results:
    notification_box.insert("end", "SUBJECT: " + i[1] + "\n")
    notification_box.insert("end", "BODY: " + i[2] + "\n")
    notification_box.insert("end", "\n\n")
  customtkinter.CTkButton(main_notification_frame, text="Clear", command=lambda: clearNotifications(notification_box, student=True, student_id=studentID.get())).place(x=150, y=10)
  notification_box.configure(state="disabled")
  notification_help_dict = {
    "student_main_message_frame": "Notify and/or email administrators.",
    "main_notification_frame": "Check all notifications from most to least recent. Cleared notifications are gone forever unless backed up."
  }
  help_switch = customtkinter.CTkSwitch(master=root, text="Help Mode", onvalue="on", offvalue="off", variable=help_mode, command=lambda: help_labels(help_switch.get(), (student_main_message_frame, notification_help_dict["student_main_message_frame"]),(main_notification_frame, notification_help_dict["main_notification_frame"])))
  help_switch.place(x=840, y=80)
  if help_switch.get() == "on":
    help_labels(help_switch.get(), (
    student_main_message_frame, notification_help_dict["student_main_message_frame"]),
    (main_notification_frame, notification_help_dict["main_notification_frame"])
    )


# home page for administrators
def admin_home():
  # prepare winners to be updated whenever admins clicks winner generator
  add_points()
  sql_select_query = "select * from studentlogin"
  mycursor.execute(sql_select_query)
  records = mycursor.fetchall()
  for row in records:
    if row[4] == 9:
      ninth_sort.append((row[0], row[1], row[4], row[5], row[6]))
    if row[4] == 10:
      tenth_sort.append((row[0], row[1], row[4], row[5], row[6]))
    if row[4] == 11:
      eleven_sort.append((row[0], row[1], row[4], row[5], row[6]))
    if row[4] == 12:
      twelve_sort.append((row[0], row[1], row[4], row[5], row[6]))
  ninth_sort.sort(key=lambda x: x[3], reverse=True)
  tenth_sort.sort(key=lambda x: x[3], reverse=True)
  eleven_sort.sort(key=lambda x: x[3], reverse=True)
  twelve_sort.sort(key=lambda x: x[3], reverse=True)
  # create appropriate buttons and text fields for admin functionality
  leaderboard_button = customtkinter.CTkButton(root, text="Leaderboard", command=lambda: [leaderboard_tracker()])
  leaderboard_button.place(x=435, y=130)
  generate = customtkinter.CTkButton(text='Generate Winners', command=lambda: (exec(open('winner_generator.py').read())))
  generate.place(x=435, y=160)
  nav_bar("home")
  # interactive help menu information for specific page
  winners = customtkinter.CTkLabel(root, text="Winners", bg='blue', fg='white', text_font=("Times New Roman", 30, "bold")).place(x=435, y=200)
  home_help_dict = {
    "generate":  "Generate the profiles of the highest scoring and a randomly selected student from each grade",
    "leaderboard_button": "Create a new window with the profiles of all students by grade."
  }
  help_switch = customtkinter.CTkSwitch(master=root, text="Help Mode", onvalue="on", offvalue="off", variable=help_mode, command=lambda: help_labels(help_switch.get(), (generate, home_help_dict["generate"]), (leaderboard_button, home_help_dict["leaderboard_button"])))
  help_switch.place(x=840, y=80)
  if help_switch.get() == "on":
    help_labels(help_switch.get(), (
    generate, home_help_dict["generate"]),
                (leaderboard_button, home_help_dict["leaderboard_button"]))


# events page for administrators
def events_page():
  nav_bar("event")
  # calendar for date picking
  today = date.today()
  cal = Calendar(root, background="black", disabledbackground="black", bordercolor="black",
               headersbackground="black", normalbackground="black", foreground='white',
               normalforeground='white', headersforeground='white', selectmode='day', year=today.year, month=today.month, day=today.day)
  cal.pack(pady=100)
  customtkinter.CTkButton(root, text="Add Event", command=lambda: [add_event(cal.get_date())]).place(x=440, y=300)

  customtkinter.CTkLabel(root, text="Events", text_font=("Times New Roman", 25, "bold")).place(x=445, y=380)

  # frame which displays all events within database
  event_frame = customtkinter.CTkFrame(root, width=750, height=220)
  event_frame.place(x=200, y=470)
  second_event_frame = customtkinter.CTkFrame(event_frame, width=750, height=195)
  second_event_frame.place(x=0, y=25)
  add_points()
  sql_select_query = "select * from events ORDER BY day, end_time, start_time"
  mycursor.execute(sql_select_query)
  records = mycursor.fetchall()

  x_place = 200
  for i in range((len(records) // 5 + (len(records) % 5 > 0))):
    customtkinter.CTkButton(root, text=("Tab " + str(i+1)), command=lambda d=(i+1): change_tab(d, second_event_frame, records, delete_event, "Remove")).place(x=x_place, y=440)
    x_place += 150
  e = customtkinter.CTkLabel(event_frame, text='Name', anchor="w", width=220).place(x=0, y=0)
  e = customtkinter.CTkLabel(event_frame, text='Date', anchor="w").place(x=150, y=0)
  e = customtkinter.CTkLabel(event_frame, text='Start Time', anchor="w").place(x=250, y=0)
  e = customtkinter.CTkLabel(event_frame, text='End Time', anchor="w").place(x=325, y=0)
  e = customtkinter.CTkLabel(event_frame, text='Location', anchor="w", width=300).place(x=400, y=0)
  e = customtkinter.CTkLabel(event_frame, text='Points', anchor="w").place(x=500, y=0)
  change_tab(1, second_event_frame, records, delete_event, "Remove")
  # interactive help menu information for specific page
  event_help_dict = {
    "cal": "Creates a new window to select optional values for event. Default date for event is today unless another date is chosen in the calendar. If any incorrect values are given (like a string for points) it will be ignored.",
    "event_frame": "Shows all events in order of date. Each tab holds 5 events."
  }
  help_switch = customtkinter.CTkSwitch(master=root, text="Help Mode", onvalue="on", offvalue="off", variable=help_mode, command=lambda: help_labels(help_switch.get(), (cal, event_help_dict["cal"]), (event_frame, event_help_dict["event_frame"])))
  help_switch.place(x=840, y=80)
  if help_switch.get() == "on":
    help_labels(help_switch.get(), (
    cal, event_help_dict["cal"]), (event_frame, event_help_dict["event_frame"]))


# messaging page for administrators
def message_page():
  nav_bar("bell")
  customtkinter.CTkLabel(root, text="Message", text_font=("Times New Roman", 20, "bold")).place(x=300, y=100)
  # messaging frame and accompanying widgets (dropbox, text  box, scrollbar)
  main_message_frame = customtkinter.CTkFrame(root, width=300, height=490, corner_radius=10)
  main_message_frame.place(x=230, y=150)
  message_frame = customtkinter.CTkFrame(main_message_frame, width=300, height=490, corner_radius=10)
  message_frame.place(x=10, y=230)
  message_box = customtkinter.CTkTextbox(master=message_frame, width=270, height=220)
  message_box.pack(side=LEFT, expand=1, fill=BOTH)
  message_bar = customtkinter.CTkScrollbar(message_frame, orientation=VERTICAL, command=message_box.yview)
  message_bar.pack(side=RIGHT, fill=Y)
  message_box.configure(yscrollcommand=message_bar.set)
  message_box.bind('<Configure>', lambda: message_box.configure(scrollregion=message_box.bbox("all")))
  body_label = customtkinter.CTkLabel(main_message_frame, text="Body").place(x=85, y=200)
  email_bool = tkinter.StringVar(value="off")
  notify_bool = tkinter.StringVar(value="off")
  subject = tkinter.StringVar()
  subject_label = customtkinter.CTkLabel(main_message_frame, text="Subject").place(x=85, y=140)
  subject_entry = customtkinter.CTkEntry(main_message_frame, textvariable=subject).place(x=85, y=170)
  email_checkbox = customtkinter.CTkCheckBox(main_message_frame, text="Email", variable=email_bool, onvalue="on", offvalue="off").place(x=0, y=0)
  notify_checkbox = customtkinter.CTkCheckBox(main_message_frame, text="Notify", variable=notify_bool, onvalue="on", offvalue="off").place(x=0, y=30)
  grade_value = tkinter.StringVar()
  event_value = tkinter.StringVar()
  grade_list = ["All Grades", "12", "11", "10", "9"]
  grade_combobox = customtkinter.CTkComboBox(main_message_frame, variable=grade_value, values=grade_list)
  grade_combobox.set("All Grades")
  grade_combobox.place(x=150, y=0)
  event_list = ["All Events"]
  check1 = "SELECT * FROM events"
  mycursor.execute(check1)
  for event in mycursor:
    event_list.append(event[0])
  event_combobox = customtkinter.CTkComboBox(main_message_frame, variable=event_value, values=event_list)
  event_combobox.set("All Events")
  event_combobox.place(x=150, y=30)
  customtkinter.CTkLabel(main_message_frame, text="Recipient").place(x=85, y=80)
  recipient = tkinter.StringVar()

  def disable_options():
    email_bool.set("off")
    notify_bool.set("off")
    grade_value.set("All Grades")
    event_value.set("All Events")
    recipient.set("")
    subject.set("")
    message_box.delete("1.0", "end")

  recipient_entry = customtkinter.CTkEntry(main_message_frame, textvariable=recipient)
  recipient_entry.place(x=85, y=110)
  recipient_entry.bind("<FocusIn>", lambda e: [event_combobox.set("All Events"), grade_combobox.set("All Grades")])
  recipient_entry.bind("<FocusOut>", lambda e: [event_combobox.set("All Events"), grade_combobox.set("All Grades")])
  grade_combobox.configure(command=lambda e: recipient.set(""))
  event_combobox.configure(command=lambda e: recipient.set(""))
  customtkinter.CTkButton(main_message_frame, text="Send", command=lambda: [send_message(email_bool.get(), notify_bool.get(), grade_value.get(), event_value.get(), recipient.get(), subject.get(), message_box.get(1.0, "end-1c")), disable_options()]).place(x=85, y=460)
  # notification box
  customtkinter.CTkLabel(root, text="Notifications", text_font=("Times New Roman", 20, "bold")).place(x=670, y=100)
  main_notification_frame = customtkinter.CTkFrame(root, width=400, height=490, corner_radius=10)
  main_notification_frame.place(x=550, y=150)
  notification_frame = customtkinter.CTkFrame(main_notification_frame, width=350, height=430, corner_radius=10)
  notification_frame.place(x=20, y=50)
  notification_box = customtkinter.CTkTextbox(master=notification_frame, width=350, height=430)
  notification_box.pack(side=LEFT, expand=1, fill=BOTH)
  notification_bar = customtkinter.CTkScrollbar(notification_frame, orientation=VERTICAL, command=notification_box.yview)
  notification_bar.pack(side=RIGHT, fill=Y)
  notification_box.configure(yscrollcommand=notification_bar.set)
  notification_box.bind('<Configure>', lambda: notification_box.configure(scrollregion=notification_box.bbox("all")))
  mycursor.execute("SELECT * FROM admin_notifications")
  results = mycursor.fetchall()
  for i in results:
    notification_box.insert("end", "FROM: " + i[0] + "\n")
    notification_box.insert("end", "SUBJECT: " + i[1] + "\n")
    notification_box.insert("end", "BODY: " + i[2] + "\n")
    notification_box.insert("end", "\n\n")
  customtkinter.CTkButton(main_notification_frame, text="Clear", command=lambda: clearNotifications(notification_box)).place(x=130, y=10)
  notification_box.configure(state="disabled")
  # interactive help menu information for specific page
  notification_help_dict = {
    "main_message_frame": "Notify and/or email students. Filter using dropdown boxes. If recipient email, id, or full name is entered filters will not be checked.",
    "main_notification_frame": "Check all notifications from most to least recent. If notifications are cleared, they cannot be recovered unless backed up."
  }
  help_switch = customtkinter.CTkSwitch(master=root, text="Help Mode", onvalue="on", offvalue="off", variable=help_mode, command=lambda: help_labels(help_switch.get(), (main_message_frame, notification_help_dict["main_message_frame"]),(main_notification_frame, notification_help_dict["main_notification_frame"])))
  help_switch.place(x=840, y=80)
  if help_switch.get() == "on":
    help_labels(help_switch.get(), (
    main_message_frame, notification_help_dict["main_message_frame"]),
    (main_notification_frame, notification_help_dict["main_notification_frame"])
    )


# accounts page for administrators
def account_page():
  nav_bar("student")
  student_frame = customtkinter.CTkFrame(root, width=250, height=560, corner_radius=10)
  student_frame.place(x=290, y=80)

  customtkinter.CTkLabel(root, text="Add Student", bg_color='#2B2C2E', text_font=("Times New Roman", 25, "bold")).place(x=330, y=110)

  id_input = tkinter.StringVar()
  name_input = tkinter.StringVar()
  password_input = tkinter.StringVar()
  email_input = tkinter.StringVar()
  grade_input = tkinter.StringVar()

  # function to add student to database (checks for all correct characteristics and throws errors otherwise)
  def add_student():
    if name_input.get() == "":
      messagebox.showerror('Invalid Entry', 'Name should not be empty')
      return
    if password_input.get() == "":
      messagebox.showerror('Invalid Entry', 'Password should not be empty')
      return
    try:
      int(id_input.get())
    except ValueError:
      messagebox.showerror('Invalid Entry', 'ID should be an integer')
      return
    if len(password_input.get()) > 8:
      messagebox.showerror('Invalid Entry', 'Password must be 8 characters or less')
      return
    try:
      if not(int(grade_input.get()) == 9 or int(grade_input.get()) == 10 or int(grade_input.get()) == 11 or int(grade_input.get()) == 12):
        messagebox.showerror('Invalid Entry', 'Grade must be between 9 and 12')
        return
    except ValueError:
      messagebox.showerror('Invalid Entry', 'Grade must be between 9 and 12')
      return

    check1 = """INSERT INTO studentlogin(id, name, password, email, grade, score) VALUES (%s, %s, %s, %s, %s, %s)"""
    try:
      mycursor.execute(check1, (id_input.get(), name_input.get(), password_input.get(), email_input.get(), grade_input.get(), 0))
    except:
      messagebox.showerror('Invalid Entry', 'ID has already been used for another student')
      return
    id_input.set("")
    name_input.set("")
    password_input.set("")
    email_input.set("")
    grade_input.set("")

  id_label = customtkinter.CTkLabel(text="ID", anchor='w', bg_color='#2B2C2E').place(x=340, y=180)
  name_label = customtkinter.CTkLabel(text="Name", anchor='w', bg_color='#2B2C2E').place(x=320, y=250)
  password_label = customtkinter.CTkLabel(text="Password", anchor='w', bg_color='#2B2C2E').place(x=295, y=320)
  email_label = customtkinter.CTkLabel(text="Email", anchor='w', bg_color='#2B2C2E').place(x=320, y=390)
  grade_label = customtkinter.CTkLabel(text="Grade", anchor='w', bg_color='#2B2C2E').place(x=320, y=460)

  id_entry = customtkinter.CTkEntry(textvariable=id_input).place(x=360, y=180)
  name_entry = customtkinter.CTkEntry(textvariable=name_input).place(x=360, y=250)
  password_entry = customtkinter.CTkEntry(textvariable=password_input).place(x=360, y=320)
  email_entry = customtkinter.CTkEntry(textvariable=email_input).place(x=360, y=390)
  grade_entry = customtkinter.CTkEntry(textvariable=grade_input).place(x=360, y=460)
  customtkinter.CTkButton(text='Add', command=lambda: [add_student()]).place(x=360, y=530)

  # REMOVE students
  remove_student_frame = customtkinter.CTkFrame(root, width=250, height=560, corner_radius=10)
  remove_student_frame.place(x=640, y=80)

  customtkinter.CTkLabel(remove_student_frame, text="Remove Student", text_font=("Times New Roman", 25, "bold")).place(x=10, y=30)

  id_input_delete = tkinter.StringVar()
  name_input_delete = tkinter.StringVar()

  # function called to delete student from database using ID or name
  def delete_student(type_id, delete_id):
    if type_id == "id":
      check1 = "DELETE FROM studentlogin WHERE id = " + delete_id
      id_input_delete.set("")
    else:
      check1 = 'DELETE FROM studentlogin WHERE name = "' + delete_id + '"'
      name_input_delete.set("")
    mycursor.execute(check1)

  customtkinter.CTkLabel(remove_student_frame, text="ID", anchor='w').place(x=50, y=100)
  customtkinter.CTkEntry(remove_student_frame, textvariable=id_input_delete).place(x=70, y=100)
  customtkinter.CTkButton(remove_student_frame, text='Remove', command=lambda: [delete_student("id", id_input_delete.get())]).place(x=70, y=150)
  customtkinter.CTkLabel(remove_student_frame, text="Name", anchor='w').place(x=30, y=250)
  customtkinter.CTkEntry(remove_student_frame, textvariable=name_input_delete).place(x=70, y=250)
  customtkinter.CTkButton(remove_student_frame, text='Remove', command=lambda: [delete_student("name", name_input_delete.get())]).place(x=70, y=300)

  # BUTTON TO DELETE ALL STUDENTS, GRADUATE, AND REMOVE ALL POINTS
  def graduate():
    mycursor.execute("DELETE FROM studentlogin WHERE grade = 12")
    mycursor.execute("UPDATE studentlogin SET grade = 10 WHERE grade = 9")
    mycursor.execute("UPDATE studentlogin SET grade = 11 WHERE grade = 10")
    mycursor.execute("UPDATE studentlogin SET grade = 12 WHERE grade = 11")
  customtkinter.CTkButton(remove_student_frame, text="Graduate", command=lambda: [graduate()]).place(x=70, y=400)
  customtkinter.CTkButton(remove_student_frame, text="Remove All Students", command=lambda: [mycursor.execute("DELETE FROM studentlogin")]).place(x=70, y=450)
  customtkinter.CTkButton(remove_student_frame, text="Remove All Points", command=lambda: [mycursor.execute("UPDATE studentlogin SET score = 0")]).place(x=70, y=500)
  # interactive help menu information for specific page
  account_help_dict = {
    "student_frame": "Add other students. Email is optional.",
    "remove_student_frame": "Delete student through ID (recommended) or Name. Graduate to remove 12th graders and increase each grade by 1. Other buttons are self-explanatory."
  }
  help_switch = customtkinter.CTkSwitch(master=root, text="Help Mode", onvalue="on", offvalue="off", variable=help_mode, command=lambda: help_labels(help_switch.get(), (student_frame, account_help_dict["student_frame"]),(remove_student_frame, account_help_dict["remove_student_frame"])))
  help_switch.place(x=840, y=60)
  if help_switch.get() == "on":
    help_labels(help_switch.get(), (
    student_frame, account_help_dict["student_frame"]),
    (remove_student_frame, account_help_dict["remove_student_frame"])
    )


# settings page for administrators
def settings_page():
  # changes settings for user experience
  def change_setting(toggle_value, setting_string):
    request = 'update settings set toggle = "' + toggle_value + '" where setting = "' + setting_string + '"'
    mycursor.execute(request)
  # clears mysql tables for database cleansing
  def clear_table(*table_names):
    for table in table_names:
      mycursor.execute(("DELETE FROM " + table))

  nav_bar("settings")
  # award frame for settings (changing award and threshold values)
  customtkinter.CTkLabel(root, text="Award Settings", text_font=("Times New Roman", 20, "bold")).place(x=300, y=100)
  award_setting_frame = customtkinter.CTkFrame(root, width=300, height=490, corner_radius=10)
  award_setting_frame.place(x=230, y=150)
  school_award = tkinter.StringVar()
  food_award = tkinter.StringVar()
  spirit_award = tkinter.StringVar()
  school_threshold = tkinter.StringVar()
  food_threshold = tkinter.StringVar()
  spirit_threshold = tkinter.StringVar()
  mycursor.execute("SELECT * FROM awards")
  results = mycursor.fetchall()
  school_award.set(results[1][1])
  school_threshold.set(results[1][2])
  food_award.set(results[0][1])
  food_threshold.set(results[0][2])
  spirit_award.set(results[2][1])
  spirit_threshold.set(results[2][2])

  def set_award():  # add update award accordingly code
    try:
      int(school_threshold.get())
      int(spirit_threshold.get())
      int(food_threshold.get())
    except ValueError:
      messagebox.showerror('Invalid Entry', 'Thresholds should have integer inputs')
      return
    check1 = 'UPDATE IGNORE awards SET award="' + school_award.get() + '", threshold = ' + school_threshold.get() + ' WHERE award_type = "school"'
    mycursor.execute(check1)
    check1 = """UPDATE IGNORE awards SET award=%s, threshold=%s WHERE award_type=%s;"""
    mycursor.execute(check1, (food_award.get(), food_threshold.get(), "food"))
    check1 = """UPDATE IGNORE awards SET award=%s, threshold=%s WHERE award_type=%s;"""
    mycursor.execute(check1, (spirit_award.get(), spirit_threshold.get(), "spirit"))
    threshold_to_award = [(int(school_threshold.get()), school_award.get()), (int(food_threshold.get()), food_award.get()), (int(spirit_threshold.get()), spirit_award.get())]
    threshold_to_award.sort()
    mycursor.execute(('update studentlogin set award="' + "None" + '" where score <= ' + str(threshold_to_award[0][0])))
    mycursor.execute(('update studentlogin set award="' + threshold_to_award[0][1] + '" where score > ' + str(threshold_to_award[0][0])))
    mycursor.execute(('update studentlogin set award="' + threshold_to_award[1][1] + '" where score > ' + str(threshold_to_award[1][0])))
    mycursor.execute(('update studentlogin set award="' + threshold_to_award[2][1] + '" where score > ' + str(threshold_to_award[2][0])))

  customtkinter.CTkLabel(award_setting_frame, text="School Award", text_font=("Times New Roman", 12, "bold")).place(x=70, y=0)
  customtkinter.CTkLabel(award_setting_frame, text="Award", text_font=("Times New Roman", 12, "bold")).place(x=0, y=30)
  customtkinter.CTkLabel(award_setting_frame, text="Threshold", text_font=("Times New Roman", 12, "bold")).place(x=0, y=60)
  customtkinter.CTkLabel(award_setting_frame, text="Food Award", text_font=("Times New Roman", 12, "bold")).place(x=70, y=110)
  customtkinter.CTkLabel(award_setting_frame, text="Award", text_font=("Times New Roman", 12, "bold")).place(x=0, y=140)
  customtkinter.CTkLabel(award_setting_frame, text="Threshold", text_font=("Times New Roman", 12, "bold")).place(x=0, y=170)
  customtkinter.CTkLabel(award_setting_frame, text="Spirit Award", text_font=("Times New Roman", 12, "bold")).place(x=70, y=220)
  customtkinter.CTkLabel(award_setting_frame, text="Award", text_font=("Times New Roman", 12, "bold")).place(x=0, y=250)
  customtkinter.CTkLabel(award_setting_frame, text="Threshold", text_font=("Times New Roman", 12, "bold")).place(x=0, y=280)
  customtkinter.CTkEntry(award_setting_frame, textvariable=school_award).place(x=120, y=30)
  customtkinter.CTkEntry(award_setting_frame, textvariable=school_threshold).place(x=120, y=60)
  customtkinter.CTkEntry(award_setting_frame, textvariable=food_award).place(x=120, y=140)
  customtkinter.CTkEntry(award_setting_frame, textvariable=food_threshold).place(x=120, y=170)
  customtkinter.CTkEntry(award_setting_frame, textvariable=spirit_award).place(x=120, y=250)
  customtkinter.CTkEntry(award_setting_frame, textvariable=spirit_threshold).place(x=120, y=280)
  customtkinter.CTkButton(award_setting_frame, text="Save", command=lambda: [set_award()]).place(x=70, y=450)

  # general settings frame customizes user experience using toggle switches
  general_settings_frame = customtkinter.CTkFrame(root, width=300, height=490, corner_radius=10)
  general_settings_frame.place(x=600, y=150)
  customtkinter.CTkLabel(root, text="General Settings", text_font=("Times New Roman", 20, "bold")).place(x=670, y=100)
  customtkinter.CTkButton(general_settings_frame, text="Backup Data", command=lambda: [backup_data()]).place(x=80, y=400)
  customtkinter.CTkButton(general_settings_frame, text="Documentation", command=lambda: [os.startfile(r"C:\Users\krish\PycharmProjects\CodingProgramming2023\documentation.txt")]).place(x=80, y=450)
  customtkinter.CTkSwitch(general_settings_frame, text="Disable Login", onvalue="True", offvalue="False", variable=disable_login, command=lambda: [change_setting(disable_login.get(), "disable_login")]).place(x=80, y=20)
  customtkinter.CTkSwitch(general_settings_frame, text="Disable Leaderboard", onvalue="True", offvalue="False", variable=disable_leaderboard, command=lambda: [change_setting(disable_leaderboard.get(), "disable_leaderboard")]).place(x=80, y=70)
  customtkinter.CTkSwitch(general_settings_frame, text="Disable Message", onvalue="True", offvalue="False", variable=disable_message, command=lambda: [change_setting(disable_message.get(), "disable_message")]).place(x=80, y=120)
  customtkinter.CTkButton(general_settings_frame, text="Clear Messages", command=lambda: [clear_table("student_notifications", "admin notifications")]).place(x=80, y=200)
  customtkinter.CTkButton(general_settings_frame, text="Clear Registrations", command=lambda: [clear_table("registered")]).place(x=80, y=250)
  customtkinter.CTkButton(general_settings_frame, text="Clear Events", command=lambda: [clear_table("events", "registered")]).place(x=80, y=300)

  # interactive help menu information for specific page
  settings_help_dict = {
    "award_setting_frame": "Change awards and thresholds. Student must be greater than threshold to get award.",
    "general_settings_frame": "Disable login, leaderboard view, or messaging for students. Backup is recommended before clearing any data. Clicking the backup button will back up the entire database to the backup_files folder."
  }
  help_switch = customtkinter.CTkSwitch(master=root, text="Help Mode", onvalue="on", offvalue="off", variable=help_mode, command=lambda: help_labels(help_switch.get(), (award_setting_frame, settings_help_dict["award_setting_frame"]),(general_settings_frame, settings_help_dict["general_settings_frame"])))
  help_switch.place(x=840, y=80)
  if help_switch.get() == "on":
    help_labels(help_switch.get(), (
    award_setting_frame, settings_help_dict["award_setting_frame"]),
    (general_settings_frame, settings_help_dict["general_settings_frame"])
    )


# starts the user off at the login page
# data is first backed up and then session is closed when user closes window
loginpage()
root.protocol("WM_DELETE_WINDOW", lambda: [backup_data(), root.destroy()])
root.mainloop()
