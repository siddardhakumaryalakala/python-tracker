import datetime
import json
import os
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# Master 30-Day Python Roadmap
ROADMAP = {
    1: ("Setup + Basics", "Python, VS Code, print(), syntax"),
    2: ("Variables & Data Types", "int, float, str, bool, type conversion"),
    3: ("Operators", "arithmetic, comparison, logical, assignment"),
    4: ("Strings", "indexing, slicing, methods, formatting"),
    5: ("Lists", "create, update, slice, list methods"),
    6: ("Tuples, Sets & Dicts", "tuples, sets, dictionaries, key-value pairs"),
    7: ("Conditions", "if, elif, else, nested conditions"),
    8: ("Loops", "for, while, break, continue, pass"),
    9: ("Loop Problems", "patterns, prime numbers, factorial, Fibonacci"),
    10: ("Functions", "parameters, return values, arguments"),
    11: ("Advanced Functions", "*args, **kwargs, lambda, scope"),
    12: ("Comprehensions", "list/set/dict comprehensions"),
    13: ("Modules & Packages", "import, built-ins, custom modules"),
    14: ("Exception Handling", "try, except, else, finally, raise"),
    15: ("File Handling", "txt, csv, json, read/write modes"),
    16: ("map, filter, reduce", "functional programming, lambda expressions"),
    17: ("Iterators & Generators", "iter(), next(), yield keyword"),
    18: ("Decorators", "@decorator syntax, modifying functions"),
    19: ("OOP Basics", "classes, objects, constructor (__init__), methods"),
    20: ("OOP Advanced", "inheritance, polymorphism, encapsulation"),
    21: ("OOP Project", "Build a Student Management CRUD app"),
    22: ("APIs", "HTTP requests, GET/POST, JSON handling"),
    23: ("Web Scraping", "requests, BeautifulSoup, data extraction"),
    24: ("Python + SQL", "SQLite CRUD operations with Python"),
    25: ("Advanced Python", "type hints, dataclasses, context managers"),
    26: ("Testing & Debugging", "pytest, assertions, logging"),
    27: ("Concurrency", "threading, multiprocessing, async/await"),
    28: ("NumPy & Pandas", "DataFrames, Series, filtering, groupby"),
    29: ("Visualization", "matplotlib, seaborn, exploratory data analysis"),
    30: ("Capstone Project", "Sales Analytics Pipeline (CSV -> SQLite -> Visuals)")
}

def load_settings():
    topic = os.getenv("NTFY_TOPIC", "python-tracker")
    start_date = datetime.date(2026, 10, 20)

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                if "ntfy_topic" in cfg:
                    topic = cfg["ntfy_topic"]
                if "start_date" in cfg:
                    y, m, d = map(int, cfg["start_date"].split("-"))
                    start_date = datetime.date(y, m, d)
        except Exception as e:
            print(f"[WARN] Could not parse config.json, using defaults: {e}")

    return topic, start_date

def send_daily_alert():
    topic, start_date = load_settings()
    today = datetime.date.today()
    day_num = (today - start_date).days + 1

    actions = []

    if 1 <= day_num <= 30:
        title, topics = ROADMAP[day_num]
        headline = f"Python Roadmap - Day {day_num} of 30: {title}"
        message = (
            f"Topic: {title}\n"
            f"Key Concepts: {topics}\n\n"
            f"1-Hour Protocol:\n"
            f"- 15m: Learn Concept\n"
            f"- 25m: Code Yourself\n"
            f"- 15m: Practice Problems\n"
            f"- 5m: Notes & Review\n\n"
            f"Consistency beats talent. Let's get it done today!"
        )
        tags = ["snake", "books"]
        actions = [
            {
                "action": "http",
                "label": f"Mark Day {day_num} Done",
                "url": f"https://ntfy.sh/{topic}",
                "method": "POST",
                "body": f"DONE {day_num}"
            }
        ]
    elif day_num > 30:
        headline = "Roadmap Completed!"
        message = "Congratulations! You completed the 30-day Python roadmap! Time to build projects and revise."
        tags = ["tada", "partying_face"]
    else:
        days_left = abs(day_num - 1)
        headline = f"Python Challenge Begins in {days_left} Day(s)!"
        message = "Get your VS Code and Python environment ready. Day 1 starts tomorrow!"
        tags = ["hourglass", "rocket"]

    payload = {
        "topic": topic,
        "title": headline,
        "message": message,
        "priority": 4,
        "tags": tags,
        "actions": actions
    }

    try:
        response = requests.post("https://ntfy.sh", json=payload, timeout=15)
        if response.status_code == 200:
            print(f"[SUCCESS] Alert sent to topic '{topic}' for Day {day_num}!")
            print(f"Check notification at: https://ntfy.sh/{topic}")
            return True
        else:
            print(f"[FAILED] HTTP {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Could not send alert: {e}")
        return False

if __name__ == "__main__":
    success = send_daily_alert()
    if not success:
        exit(1)
