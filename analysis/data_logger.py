import csv


class DataLogger:
    def __init__(self, filename="results.csv"):
        self.filename = filename

        # create file with header
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Question", "Deception Score"])

    def log(self, question, score):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([question, score])