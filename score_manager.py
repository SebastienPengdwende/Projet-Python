#score_manager.py
import json, os

class ScoreManager:
    def __init__(self, file_path="scores.json"):
        self.file_path = file_path
        self.scores = self._load()
    def _load(self):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    def _save(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.scores, f, ensure_ascii=False, indent=4)
        return True
    def update_score(self, user, level, score):
        score = int(score) 
        entry = next((u for u in self.scores[level] if u['user'] == user), None)
        if entry:
            entry['score'] = max(entry['score'], score)
        else:
            self.scores[level].append({'user': user, 'score': score})
        self.scores[level].sort(key=lambda x: x['score'], reverse=True)
        return self._save()
    def get_scores(self, level): return self.scores.get(level, [])
    def reset_scores(self): 
        self.scores = {lvl: [] for lvl in ["easy", "medium", "hard"]}
        return self._save()