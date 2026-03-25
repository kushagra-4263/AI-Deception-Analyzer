import time


class QuestionManager:
    def __init__(self):
        self.questions = [
            "What is your name?",
            "Where do you live?",
            "Did you cheat in an exam?"
        ]

        self.current_index = 0
        self.start_time = None
        self.duration = 5   # seconds per question

        self.active = False

    def start(self):
        self.current_index = 0
        self.start_time = time.time()
        self.active = True

    def get_current_question(self):
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def update(self):
        if not self.active:
            return

        if time.time() - self.start_time > self.duration:
            self.current_index += 1
            self.start_time = time.time()

            if self.current_index >= len(self.questions):
                self.active = False

    def is_active(self):
        return self.active