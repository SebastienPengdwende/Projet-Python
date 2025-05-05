#difficulty.py
class DifficultyManager:
    SETTINGS = {
        "easy": {"time_per_question": 30, "score_per_question": 1},
        "medium": {"time_per_question": 20, "score_per_question": 2},
        "hard": {"time_per_question": 15, "score_per_question": 3},
    }

    def get_settings(self, level): return self.SETTINGS[level]
    def get_time(self, level): return self.get_settings(level)["time_per_question"]
    def get_score(self, level): return self.get_settings(level)["score_per_question"]
    def calculate_final_score(self, level, correct, bonus=0): return correct * self.get_score(level) + bonus

difficulty_manager = DifficultyManager()
def get_difficulty_settings(level): return difficulty_manager.get_settings(level)