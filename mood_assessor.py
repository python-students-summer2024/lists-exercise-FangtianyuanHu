import datetime
import os


DIRECTORY = 'records'
FILE_PATH = os.path.join(DIRECTORY, 'mood_diary.txt')
MOOD_MAP = {
    "happy": 2,
    "relaxed": 1,
    "apathetic": 0,
    "sad": -1,
    "angry": -2
}
REVERSE_MOOD_MAP = {2: "happy", 1: "relaxed", 0: "apathetic", -1: "sad", -2: "angry"}

def prompt_for_mood():
    while True:
        user_input = input("Please enter your current mood: ").strip().lower()
        if user_input in MOOD_MAP:
            return MOOD_MAP[user_input]
        print("Invalid input. Please try again.")

def read_mood_data():
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
    if not os.path.exists(FILE_PATH):
        return []
    file = open(FILE_PATH, 'r')
    entries = file.readlines()
    file.close()
    return [entry.strip() for entry in entries]

def write_mood_data(mood_entries):
    file = open(FILE_PATH, 'w')
    for entry in mood_entries:
        file.write(entry + '\n')
    file.close()

def record_mood(mood_score):
    today_date = str(datetime.date.today())
    mood_entries = read_mood_data()

    for entry in mood_entries:
        if today_date in entry:
            print("Sorry, you have already logged your mood today.")
            return False

    mood_entries.append(f"{today_date},{mood_score}")
    write_mood_data(mood_entries)
    return True

def evaluate_mood():
    mood_entries = read_mood_data()
    if len(mood_entries) < 7:
        return

    recent_moods = [int(entry.split(',')[1]) for entry in mood_entries[-7:]]
    average_mood_value = round(sum(recent_moods) / 7)
    average_mood = REVERSE_MOOD_MAP.get(average_mood_value, "apathetic")

    count_happy = recent_moods.count(2)
    count_sad = recent_moods.count(-1)
    count_apathetic = recent_moods.count(0)

    if count_happy >= 5:
        diagnosis = "manic"
    elif count_sad >= 4:
        diagnosis = "depressive"
    elif count_apathetic >= 6:
        diagnosis = "schizoid"
    else:
        diagnosis = average_mood

    print(f"Your diagnosis: {diagnosis}!")

def assess_mood():
    mood_score = prompt_for_mood()
    if record_mood(mood_score):
        evaluate_mood()
