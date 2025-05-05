#game_ui.py
import tkinter as tk
from tkinter import messagebox
from difficulty import DifficultyManager
from score_manager import ScoreManager
from quiz_manager import QuizManager
import pygame

class SoundManager:
    def __init__(self, music_file, volume=0.5):
        pygame.mixer.init()
        self.music_file = music_file
        pygame.mixer.music.set_volume(volume)

    def start_music(self):
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play(-1)

class GameUI:
    def __init__(self, mast):
        self.mast = mast
        self.mast.title("MASTER QUIZ")
        self.mast.geometry("1000x600")
        self.mast.config(bg="#0a1128")

        self.sound_manager = SoundManager("Resources/sound.mp3")
        self.sound_manager.start_music()
        self.score_manager = ScoreManager("data/scores.json")
        self.quiz_manager = QuizManager()
        self.difficulty_manager = DifficultyManager()

        self.reset_game_state()
        self.frame_welcome()

    def reset_game_state(self):
        self.timer_running = False
        self.user_Name = self.level = self.selected_category = ""
        self.score = self.question_index = 0
        self.timer_label = self.timer_update_id = None

    def clear_window(self):
        if self.timer_update_id:
            self.mast.after_cancel(self.timer_update_id)
            self.timer_update_id = None
        self.timer_running = False
        for w in self.mast.winfo_children(): w.destroy()

    def frame_welcome(self):
        self.clear_window()
        f = tk.Frame(self.mast, bg="#0a1128")
        f.place(relx=0.5, rely=0.5, anchor="center", width=500, height=450)
        tk.Label(f, text="Welcome to Master Quiz", font=("Arial", 24, "bold"),
                fg="#fefcfb", bg="#1282a2").pack(fill="x", pady=20)
        tk.Label(f, text="Enter your username", font=("Arial", 16, "bold"),
                fg="#fefcfb", bg="#0a1128").pack(pady=20)
        self.pseudo_entry = tk.Entry(f, font=("Arial", 14), width=20)
        self.pseudo_entry.pack(pady=10)
        self.pseudo_entry.focus()
        tk.Button(f, text="Start Quiz", font=("Arial", 14), bg="#3c6e71", 
                 fg="#fefcfb", command=self.validate_pseudo).pack(pady=5, fill="x", padx=60)
        tk.Button(f, text="View Scores", font=("Arial", 14), bg="#034078", 
                 fg="#fefcfb", command=self.view_scores).pack(pady=5, fill="x", padx=60)
        tk.Button(f, text="Quit", font=("Arial", 14), bg="#d62828", 
                 fg="#fefcfb", command=self.mast.destroy).pack(pady=5, fill="x", padx=60)

    def validate_pseudo(self):
        name = self.pseudo_entry.get().strip()
        if name:
            self.user_Name = name
            self.frame_select_level()
        else:
            messagebox.showerror("Error", "Please enter a username")

    def frame_select_level(self):
        self.clear_window()
        f = tk.Frame(self.mast, bg="#0a1128")
        f.place(relx=0.5, rely=0.5, anchor="center", width=500, height=400)
        tk.Label(f, text="Select Difficulty Level", font=("Arial", 24, "bold"),
                fg="#fefcfb", bg="#1282a2").pack(pady=20, fill="x")
        buttons = tk.Frame(f, bg="#0a1128")
        buttons.pack(pady=30)
        colors = {"easy": "#3c6e71", "medium": "#f77f00", "hard": "#d62828"}
        for lvl in ["easy", "medium", "hard"]:
            settings = self.difficulty_manager.get_settings(lvl)
            row = tk.Frame(buttons, bg="#0a1128", pady=5)
            row.pack()
            tk.Button(row, text=lvl.capitalize(), font=("Arial", 16), bg=colors[lvl], 
                     fg="#fefcfb", command=lambda l=lvl: self.select_level(l)).pack(side="left", padx=10)
            time_pts = f"Time: {settings['time_per_question']}s | Points: {settings['score_per_question']}"
            tk.Label(row, text=time_pts, font=("Arial", 12), 
                    fg="#fefcfb", bg="#0a1128").pack(side="left")
        bottom = tk.Frame(f, bg="#0a1128")
        bottom.pack(side="bottom", fill="x", pady=10)
        tk.Button(bottom, text="Back", font=("Arial", 14), bg="#034078", 
                 fg="#fefcfb", command=self.frame_welcome).pack(side="left", padx=20)
        tk.Button(bottom, text="Quit", font=("Arial", 14), bg="#d62828", 
                 fg="#fefcfb", command=self.mast.destroy).pack(side="right", padx=20)

    def select_level(self, level):
        self.level = level
        cats = self.quiz_manager.get_categories(level)
        if cats: self.frame_select_category(cats)

    def frame_select_category(self, cats):
        self.clear_window()
        f = tk.Frame(self.mast, bg="#0a1128")
        f.place(relx=0.5, rely=0.5, anchor="center", width=500, height=450)
        
        tk.Label(f, text="Select Category", font=("Arial", 24, "bold"),
                fg="#fefcfb", bg="#1282a2").pack(pady=20, fill="x")
        
        for cat in sorted(cats):
            tk.Button(f, text=cat, font=("Arial", 14), bg="#034078", fg="#fefcfb",
                     width=25, command=lambda c=cat: self.start_quiz(c)).pack(pady=10)
        
        tk.Button(f, text="Back", font=("Arial", 14), bg="#034078", fg="#fefcfb",
                 command=self.frame_select_level).pack(side="left", padx=20, pady=20)
        tk.Button(f, text="Quit", font=("Arial", 14), bg="#d62828", fg="#fefcfb",
                 command=self.mast.destroy).pack(side="right", padx=20, pady=20)

    def start_quiz(self, category):
        self.selected_category = category
        self.question_index = self.score = 0
        q = self.quiz_manager.get_questions(self.level, category, count=10)
        if q:
            self.questions_for_current_session = q
            self.show_question()

    def show_question(self):
        if self.question_index >= len(self.questions_for_current_session):
            self.end_quiz()
            return   
        q = self.questions_for_current_session[self.question_index]
        self.clear_window()
        f = tk.Frame(self.mast, bg="#0a1128")
        f.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)
        tk.Label(f, text=f"Question {self.question_index + 1}/{len(self.questions_for_current_session)} - {self.selected_category}",
                font=("Arial", 12), fg="#fefcfb", bg="#1282a2").pack(fill="x", pady=5)
        tk.Label(f, text=q["question"], font=("Arial", 16, "bold"),
                fg="#fefcfb", bg="#0a1128", wraplength=550, justify="center").pack(pady=20)
        opt_frame = tk.Frame(f, bg="#0a1128")
        opt_frame.pack(expand=True)
        self.selected_option = tk.IntVar(value=-1)
        for i, opt in enumerate(q["options"]):
            tk.Radiobutton(opt_frame, text=opt, variable=self.selected_option, value=i,font=("Arial", 14), bg="#0a1128", fg="#fefcfb",
                         selectcolor="#034078", anchor="w", width=50,
                         command=lambda idx=i: self.submit_answer(idx)).pack(anchor="w", padx=20)
        self.time_remaining = self.difficulty_manager.get_time(self.level)
        self.timer_label = tk.Label(f, text=f"Time: {self.time_remaining} seconds",
                                  font=("Arial", 14), fg="#ffd700", bg="#0a1128")
        self.timer_label.pack(pady=5)
        tk.Label(f, text=f"Score: {self.score}", font=("Arial", 12),
                fg="#3c6e71", bg="#0a1128").pack(pady=5)
        bottom = tk.Frame(f, bg="#0a1128")
        bottom.pack(side="bottom", fill="x", pady=10)
        tk.Button(bottom, text="Home", font=("Arial", 12), bg="#034078", fg="#fefcfb", 
                 command=self.frame_welcome).pack(side="left", padx=20)
        tk.Button(bottom, text="Quit", font=("Arial", 12), bg="#d62828", fg="#fefcfb", 
                 command=self.mast.destroy).pack(side="right", padx=20)
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if not self.timer_running or not self.timer_label: return
        self.time_remaining -= 1
        if self.time_remaining > 0:
            if self.timer_label.winfo_exists():
                self.timer_label.config(text=f"Time: {self.time_remaining} seconds")
                self.timer_update_id = self.mast.after(1000, self.update_timer)
        else:
            self.show_timeout()

    def show_timeout(self):
        f = tk.Frame(self.mast, padx=20, pady=10, relief="raised")
        f.place(relx=0.5, rely=0.8, anchor="center", width=400)
        tk.Label(f, text="Time's up!", font=("Arial", 14, "bold"), 
                fg="#fefcfb", bg="#d62828").pack(fill="x")
        self.mast.after(1500, self.next_question)

    def submit_answer(self, ans_idx):
        if self.timer_running:
            self.timer_running = False
            if self.timer_update_id:
                self.mast.after_cancel(self.timer_update_id)
                self.timer_update_id = None
        
        q = self.questions_for_current_session[self.question_index]
        correct = self.quiz_manager.check_answer(self.user_Name, q, ans_idx)
        
        f = tk.Frame(self.mast, padx=20, pady=10, relief="raised")
        f.place(relx=0.5, rely=0.8, anchor="center", width=400)
        
        if correct:
            pts = self.difficulty_manager.get_score(self.level)
            self.score += pts
            msg = f"Correct! +{pts} points"
            clr = "#3c6e71"
        else:
            correct_ans = q["options"][q["answer"]]
            msg = f"Wrong! Correct: {correct_ans}"
            clr = "#d62828"
            
        tk.Label(f, text=msg, font=("Arial", 14, "bold"), 
                fg="#fefcfb", bg=clr).pack(fill="x")
        
        self.mast.after(1500, self.next_question)

    def next_question(self):
        self.question_index += 1
        self.show_question()

    def end_quiz(self):
        self.score_manager.update_score(self.user_Name, self.level, self.score)
        self.show_results()

    def show_results(self):
        self.clear_window()
        f = tk.Frame(self.mast, bg="#0a1128")
        f.place(relx=0.5, rely=0.5, anchor="center", width=500, height=400)
        
        tk.Label(f, text="Quiz Complete!", font=("Arial", 24, "bold"),
                fg="#fefcfb", bg="#1282a2").pack(pady=20, fill="x")
        
        info = tk.Frame(f, bg="#0a1128", padx=20, pady=20)
        info.pack(fill="both", expand=True)
        
        tk.Label(info, text=f"Player: {self.user_Name}", 
                font=("Arial", 16), fg="#fefcfb", bg="#0a1128").pack(pady=5)
        tk.Label(info, text=f"Level: {self.level.capitalize()} | Category: {self.selected_category}", 
                font=("Arial", 14), fg="#fefcfb", bg="#0a1128").pack(pady=5)
        tk.Label(info, text=f"Final Score: {self.score}", 
                font=("Arial", 18, "bold"), fg="#3c6e71", bg="#0a1128").pack(pady=20)
        
        buttons = tk.Frame(f, bg="#0a1128")
        buttons.pack(pady=20)
        
        tk.Button(buttons, text="Play Again", font=("Arial", 14), bg="#3c6e71", fg="#fefcfb",
                 command=self.frame_select_level).pack(side="left", padx=10)
        tk.Button(buttons, text="View Scores", font=("Arial", 14), bg="#034078", fg="#fefcfb",
                 command=self.view_scores).pack(side="left", padx=10)
        tk.Button(buttons, text="Home", font=("Arial", 14), bg="#2c698d", fg="#fefcfb",
                 command=self.frame_welcome).pack(side="left", padx=10)
        tk.Button(buttons, text="Quit", font=("Arial", 14), bg="#d62828", fg="#fefcfb",
                 command=self.mast.destroy).pack(side="left", padx=10)

    def view_scores(self):
        self.clear_window()
        f = tk.Frame(self.mast, bg="#0a1128")
        f.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)
        
        tk.Label(f, text="High Scores", font=("Arial", 24, "bold"),
                fg="#fefcfb", bg="#1282a2").pack(pady=20, fill="x")
        
        tabs = tk.Frame(f, bg="#0a1128")
        tabs.pack(fill="x", padx=20)
        
        colors = {"easy": "#3c6e71", "medium": "#f77f00", "hard": "#d62828"}
        content = tk.Frame(f, bg="#0a1128")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        for lvl in ["easy", "medium", "hard"]:
            tk.Button(tabs, text=lvl.capitalize(), font=("Arial", 14), bg=colors[lvl], fg="#fefcfb",
                     command=lambda l=lvl: self.show_scores(l, content)).pack(side="left", padx=10)
        
        self.show_scores("easy", content)
        
        bottom = tk.Frame(f, bg="#0a1128")
        bottom.pack(side="bottom", fill="x", pady=10)
        
        tk.Button(bottom, text="Back", font=("Arial", 14), bg="#034078", fg="#fefcfb",
                 command=self.frame_welcome).pack(side="left", padx=20, pady=10)
        tk.Button(bottom, text="Reset Scores", font=("Arial", 14), bg="#d62828", fg="#fefcfb",
                 command=self.reset_scores).pack(side="right", padx=20, pady=10)

    def show_scores(self, level, content):
        for w in content.winfo_children(): w.destroy()
        
        scores = self.score_manager.get_scores(level)
        
        header = tk.Frame(content, bg="#2c698d")
        header.pack(fill="x", pady=5)
        
        cols = [("Rank", 10), ("Player", 20), ("Score", 10)]
        for i, (text, width) in enumerate(cols):
            tk.Label(header, text=text, font=("Arial", 14, "bold"), 
                    fg="#fefcfb", bg="#2c698d", width=width).grid(row=0, column=i, padx=5, pady=5)
        
        list_frame = tk.Frame(content, bg="#0a1128")
        list_frame.pack(fill="both", expand=True)
        
        if not scores:
            tk.Label(list_frame, text="No scores yet!", 
                    font=("Arial", 14), fg="#fefcfb", bg="#0a1128").pack(pady=20)
        else:
            for i, entry in enumerate(scores[:10]):
                bg = "#034078" if i % 2 == 0 else "#0a1128"
                row = tk.Frame(list_frame, bg=bg)
                row.pack(fill="x", pady=1)
                
                data = [(f"{i+1}", 10), (entry["user"], 20), (str(entry["score"]), 10)]
                for j, (text, width) in enumerate(data):
                    tk.Label(row, text=text, font=("Arial", 14), 
                            fg="#fefcfb", bg=bg, width=width).grid(row=0, column=j, padx=5, pady=5)

    def reset_scores(self):
            self.score_manager.reset_scores()
            self.view_scores()