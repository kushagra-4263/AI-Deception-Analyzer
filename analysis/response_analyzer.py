class ResponseAnalyzer:

    def __init__(self):
        self.scores = []

    def add_score(self, score):
        self.scores.append(score)

    def get_final_score(self):

        if len(self.scores) == 0:
            return 0

        # 🔥 KEY FIX
        return max(self.scores)

    def reset(self):
        self.scores = []