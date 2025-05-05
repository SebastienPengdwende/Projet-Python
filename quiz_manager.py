#quiz_manager.py
import json
import random
class QuizManager:
    def __init__(self):
        self.questions = {lvl: self._load(lvl) for lvl in ["easy", "medium", "hard"]}
        self.user_answers = {}
        self.session = {}
    def _load(self, level):
        with open(f"data/questions/{level}.json", 'r', encoding='utf-8') as f:
            return [{**q, "original_category": cat} for cat, lst in json.load(f).items() for q in lst]
    def get_categories(self, level):
        return {q["original_category"] for q in self.questions.get(level, [])}
    def get_questions(self, level, category=None, count=10):
        pool = [q for q in self.questions[level] if not category or q["original_category"] == category]
        selected = random.sample(pool, min(count, len(pool)))
        self.session[f"{level}_{category}"] = selected
        return selected
    def check_answer(self, user, question, index):
        qid = str(question["id"])
        self.user_answers.setdefault(user, [])
        if qid in self.user_answers[user]: return False
        if question.get("answer") == index:
            self.user_answers[user].append(qid)
            return True
        return False
    def reset_session(self, user=None):
        if user: self.user_answers[user] = []
        self.session.clear()