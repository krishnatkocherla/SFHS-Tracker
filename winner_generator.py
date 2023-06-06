import tkinter
from tkinter import *
import random

# generates winners when administrators clicks winner generator
def generate_winners():
  grade_nine = customtkinter.CTkLabel(root, text="9th Grade Winners", bg='blue', fg='white', text_font=("Time New Roman", 15, "bold")).place(x=150, y=300)
  grade_nine_score = customtkinter.CTkLabel(root, text="Highest Score", bg='blue', fg='white', text_font=("Times New Roman", 12, "bold")).place(x=170, y=330)
  grade_nine_random = customtkinter.CTkLabel(root, text="Random", bg='blue', fg='white', text_font=("Times New Roman", 12, "bold")).place(x=170, y=360)

  grade_ten = customtkinter.CTkLabel(root, text="10th Grade Winners", bg='blue', fg='white', text_font=("Time New Roman", 15, "bold")).place(x=150, y=400)
  grade_ten_score = customtkinter.CTkLabel(root, text="Highest Score", bg='blue', fg='white', text_font=("Times New Roman", 12, "bold")).place(x=170, y=430)
  grade_ten_random = customtkinter.CTkLabel(root, text="Random", bg='blue', fg='white', text_font=("Times New Roman", 12, "bold")).place(x=170, y=460)

  grade_11 = customtkinter.CTkLabel(root, text="11th Grade Winners", bg='blue', fg='white', text_font=("Time New Roman", 15, "bold")).place(x=150, y=500)
  grade_eleven_score = customtkinter.CTkLabel(root, text="Highest Score", bg='blue', fg='white', text_font=("Times New Roman", 12, "bold")).place(x=170, y=530)
  grade_eleven_random = customtkinter.CTkLabel(root, text="Random", bg='blue', fg='white', text_font=("Times New Roman", 12, "bold")).place(x=170, y=560)

  grade_12 = customtkinter.CTkLabel(root, text="12th Grade Winners", bg='blue', fg='white', text_font=("Time New Roman", 15, "bold")).place(x=150, y=600)
  grade_twelve_score = customtkinter.CTkLabel(root, text="Highest Score", bg='blue', fg='white', text_font=("Times New Roman", 12, "bold")).place(x=170, y=630)
  grade_twelve_random = customtkinter.CTkLabel(root, text="Random", bg='blue', fg='white', text_font=("Times New Roman", 12, "bold")).place(x=170, y=660)

  ninth_winner_name = customtkinter.CTkLabel(root, text=ninth_sort[0][1], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=370, y=330)
  ninth_winner_id = customtkinter.CTkLabel(root, text=ninth_sort[0][0], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=550, y=330)
  ninth_winner_score = customtkinter.CTkLabel(root, text=ninth_sort[0][3], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=750, y=330)
  ninth_winner_award = customtkinter.CTkLabel(root, text=ninth_sort[0][4], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=850, y=330)
  picker = random.randint(0, len(ninth_sort)-1)
  ninth_random_name = customtkinter.CTkLabel(root, text=ninth_sort[picker][1], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=370, y=360)
  ninth_random_id = customtkinter.CTkLabel(root, text=ninth_sort[picker][0], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=550, y=360)
  ninth_random_score = customtkinter.CTkLabel(root, text=ninth_sort[picker][3], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=750, y=360)
  ninth_random_award = customtkinter.CTkLabel(root, text=ninth_sort[picker][4], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=850, y=360)

  tenth_winner_name = customtkinter.CTkLabel(root, text=tenth_sort[0][1], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=370, y=430)
  tenth_winner_id = customtkinter.CTkLabel(root, text=tenth_sort[0][0], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=550, y=430)
  tenth_winner_score = customtkinter.CTkLabel(root, text=tenth_sort[0][3], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=750, y=430)
  tenth_winner_award = customtkinter.CTkLabel(root, text=tenth_sort[0][4], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=850, y=430)
  picker = random.randint(0, len(tenth_sort)-1)
  tenth_random_name = customtkinter.CTkLabel(root, text=tenth_sort[picker][1], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=370, y=460)
  tenth_random_id = customtkinter.CTkLabel(root, text=tenth_sort[picker][0], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=550, y=460)
  tenth_random_score = customtkinter.CTkLabel(root, text=tenth_sort[picker][3], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=750, y=460)
  tenth_random_award = customtkinter.CTkLabel(root, text=tenth_sort[picker][4], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=850, y=460)

  eleventh_winner_name = customtkinter.CTkLabel(root, text=eleven_sort[0][1], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=370, y=530)
  eleventh_winner_id = customtkinter.CTkLabel(root, text=eleven_sort[0][0], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=550, y=530)
  eleventh_winner_score = customtkinter.CTkLabel(root, text=eleven_sort[0][3], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=750, y=530)
  eleventh_winner_award = customtkinter.CTkLabel(root, text=eleven_sort[0][4], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=850, y=530)
  picker = random.randint(0, len(eleven_sort)-1)
  eleventh_random_name = customtkinter.CTkLabel(root, text=eleven_sort[picker][1], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=370, y=560)
  eleventh_random_id = customtkinter.CTkLabel(root, text=eleven_sort[picker][0], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=550, y=560)
  eleventh_random_score = customtkinter.CTkLabel(root, text=eleven_sort[picker][3], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=750, y=560)
  eleventh_random_award = customtkinter.CTkLabel(root, text=eleven_sort[picker][4], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=850, y=560)

  twelve_winner_name = customtkinter.CTkLabel(root, text=twelve_sort[0][1], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=370, y=630)
  twelve_winner_id = customtkinter.CTkLabel(root, text=twelve_sort[0][0], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=550, y=630)
  twelve_winner_score = customtkinter.CTkLabel(root, text=twelve_sort[0][3], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=750, y=630)
  twelve_winner_award = customtkinter.CTkLabel(root, text=twelve_sort[0][4], bg='blue', fg='white',text_font=("Times New Roman", 12)).place(x=850, y=630)
  picker = random.randint(0, len(twelve_sort)-1)
  twelve_random_name = customtkinter.CTkLabel(root, text=twelve_sort[picker][1], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=370, y=660)
  twelve_random_id = customtkinter.CTkLabel(root, text=twelve_sort[picker][0], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=550, y=660)
  twelve_random_score = customtkinter.CTkLabel(root, text=twelve_sort[picker][3], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=750, y=660)
  twelve_random_award = customtkinter.CTkLabel(root, text=twelve_sort[picker][4], bg='blue', fg='white', text_font=("Times New Roman", 12)).place(x=850, y=660)

  name_show = customtkinter.CTkLabel(root, text="Name", bg='blue', fg='white', text_font=("Times New Roman", 12, "bold")).place(x=370, y=270)
  id_show = customtkinter.CTkLabel(root, text="ID", bg='blue', fg='white', text_font=("Times New Roman", 12, "bold")).place(x=550, y=270)
  score_show = customtkinter.CTkLabel(root, text="Score", bg='blue', fg='white', text_font=("Times New Roman", 12, "bold")).place(x=750, y=270)
  award_show = customtkinter.CTkLabel(root, text="Award", bg='blue', fg='white', text_font=("Times New Roman", 12, "bold")).place(x=850, y=270)


generate_winners()