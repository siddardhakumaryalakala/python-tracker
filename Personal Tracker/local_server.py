import http.server
import json
import os
import sys
import threading
import time
import webbrowser
from datetime import date, datetime
import requests

# Port configuration
DEFAULT_PORT = 5000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
HTML_FILE = os.path.join(BASE_DIR, "index.html")

# Fallback to personal tractor.html if index.html is missing
if not os.path.exists(HTML_FILE) and os.path.exists(os.path.join(BASE_DIR, "personal tractor.html")):
    HTML_FILE = os.path.join(BASE_DIR, "personal tractor.html")

# Master 30-Day Roadmap Curriculum
ROADMAP_DATA = [
    {
        "week": "Week 1: Python Foundation",
        "badge": "Week 1",
        "desc": "Master Python syntax, data structures, and fundamental control flow (Days 1–7)",
        "days": [
            {
                "day": 1,
                "title": "Setup + Basics",
                "topics": ["Python installation & VS Code setup", "print() function & comments", "Syntax rules & execution flow"],
                "code": '# Day 1: First Python Program\nname = "Python Explorer"\nprint(f"Hello, {name}! Welcome to Day 1.")'
            },
            {
                "day": 2,
                "title": "Variables & Data Types",
                "topics": ["int, float, str, bool primitives", "Type casting & conversion", "type() and isinstance() functions"],
                "code": '# Day 2: Dynamic Typing\nage = 22\ngpa = 3.85\nis_active = True\nprint(type(age), type(gpa), type(is_active))'
            },
            {
                "day": 3,
                "title": "Operators",
                "topics": ["Arithmetic (+, -, *, /, //, %, **)", "Comparison (==, !=, >, <)", "Logical (and, or, not) & Bitwise"],
                "code": '# Day 3: Logical & Math\nx, y = 15, 4\nprint(f"Div: {x/y}, Floor: {x//y}, Mod: {x%y}, Exp: {x**2}")\nprint(x > 10 and y < 5)'
            },
            {
                "day": 4,
                "title": "Strings & Methods",
                "topics": ["Indexing & negative slicing [start:stop:step]", "String methods (strip, split, join, replace)", "f-strings & string formatting"],
                "code": '# Day 4: Slicing & Formatting\ntext = "  python mastery  "\nclean = text.strip().title()\nprint(f"{clean} -> First 6 chars: {clean[:6]}")'
            },
            {
                "day": 5,
                "title": "Lists & Operations",
                "topics": ["Creating, indexing & slicing lists", "append, extend, insert, pop, remove", "sort vs sorted & list concatenation"],
                "code": '# Day 5: Dynamic Lists\nskills = ["Python", "SQL", "Git"]\nskills.append("FastAPI")\nprint(f"Top skill: {skills[0]}, Total: {len(skills)}")'
            },
            {
                "day": 6,
                "title": "Tuples, Sets & Dictionaries",
                "topics": ["Tuples (immutability, packing/unpacking)", "Sets (uniqueness, union, intersection)", "Dictionaries (key-value, .get(), .items())"],
                "code": '# Day 6: Hash Maps & Sets\nuser = {"name": "Alex", "level": "Intermediate"}\nunique_tags = {"backend", "python", "backend"}\nprint(user.get("role", "Developer"), unique_tags)'
            },
            {
                "day": 7,
                "title": "Conditionals & Logic",
                "topics": ["if, elif, else branch execution", "Nested conditions & ternary operators", "Truthiness (None, 0, empty collections)"],
                "code": '# Day 7: Decision Making\nscore = 88\ngrade = "A" if score >= 90 else ("B" if score >= 80 else "C")\nprint(f"Score {score} -> Grade {grade}")'
            }
        ]
    },
    {
        "week": "Week 2: Problem Solving & Logic",
        "badge": "Week 2",
        "desc": "Build algorithmic logic using loops, functions, and comprehensions (Days 8–12)",
        "days": [
            {
                "day": 8,
                "title": "Loops (for & while)",
                "topics": ["for loops with range() & enumerate()", "while loops & condition testing", "break, continue, and else clauses"],
                "code": '# Day 8: Iteration with Enumerate\ntasks = ["Design", "Code", "Test"]\nfor idx, task in enumerate(tasks, start=1):\n    print(f"Step {idx}: {task}")'
            },
            {
                "day": 9,
                "title": "Loop Problem Solving",
                "topics": ["Pattern printing & pyramids", "Prime numbers check & sieve", "Factorial & Fibonacci sequences"],
                "code": '# Day 9: Fibonacci Generator\na, b = 0, 1\nfib = []\nfor _ in range(8):\n    fib.append(a)\n    a, b = b, a + b\nprint("Fibonacci:", fib)'
            },
            {
                "day": 10,
                "title": "Functions & Modularity",
                "topics": ["def syntax, parameters & return values", "Default arguments & keyword arguments", "Docstrings & pure functions"],
                "code": '# Day 10: Clean Functions\ndef calculate_roi(investment: float, returns: float) -> float:\n    """Calculates ROI percentage."""\n    return ((returns - investment) / investment) * 100\nprint(f"ROI: {calculate_roi(1000, 1450):.1f}%")'
            },
            {
                "day": 11,
                "title": "Advanced Functions & Scope",
                "topics": ["*args (variable positional) & **kwargs", "Anonymous lambda functions", "Variable scope (LEGB rule & global/nonlocal)"],
                "code": '# Day 11: Args & Kwargs\ndef build_profile(username, *skills, **details):\n    return {"user": username, "skills": list(skills), **details}\nprint(build_profile("alex", "Python", "SQL", city="Tokyo"))'
            },
            {
                "day": 12,
                "title": "Comprehensions",
                "topics": ["List comprehensions with if-else filtering", "Dictionary comprehensions", "Set & Generator expressions"],
                "code": '# Day 12: Pythonic Comprehensions\nnumbers = range(1, 11)\nev_squares = {x: x**2 for x in numbers if x % 2 == 0}\nprint("Even Squares Dict:", ev_squares)'
            }
        ]
    },
    {
        "week": "Week 3: Intermediate Python",
        "badge": "Week 3",
        "desc": "Explore file handling, exceptions, functional patterns, and generators (Days 13–18)",
        "days": [
            {
                "day": 13,
                "title": "Modules & Packages",
                "topics": ["importing built-in modules (math, os, sys)", "from module import function syntax", "__name__ == '__main__' convention"],
                "code": '# Day 13: Modular Architecture\nimport math\nfrom datetime import datetime\nprint(f"Pi: {math.pi:.4f} | Timestamp: {datetime.now().strftime(\'%H:%M:%S\')}")'
            },
            {
                "day": 14,
                "title": "Exception Handling",
                "topics": ["try, except blocks & catching specific errors", "else block (runs when no error occurs)", "finally block & custom raise exceptions"],
                "code": '# Day 14: Robust Error Handling\ntry:\n    val = int("42")\n    res = 100 / val\nexcept (ValueError, ZeroDivisionError) as err:\n    print(f"Caught: {err}")\nelse:\n    print(f"Success: {res}")\nfinally:\n    print("Cleanup completed.")'
            },
            {
                "day": 15,
                "title": "File Handling (I/O)",
                "topics": ["Reading & writing text files with context managers", "Parsing and dumping JSON data", "Reading & writing CSV files safely"],
                "code": '# Day 15: Safe File Context Manager\nimport json\ndata = {"goal": "Python Mastery", "status": "In Progress"}\nwith open("progress.json", "w") as f:\n    json.dump(data, f, indent=2)\nprint("JSON file persisted.")'
            },
            {
                "day": 16,
                "title": "Functional Programming",
                "topics": ["map() for element transformations", "filter() for predicate filtering", "functools.reduce() for aggregate reductions"],
                "code": '# Day 16: Functional Map & Filter\nprices = [12.5, 45.0, 9.99, 120.0]\nbudget_items = list(filter(lambda p: p < 50.0, prices))\ntaxed = list(map(lambda p: round(p * 1.1, 2), budget_items))\nprint("Taxed Budget Items:", taxed)'
            },
            {
                "day": 17,
                "title": "Iterators & Generators",
                "topics": ["Iterable vs Iterator protocols (iter(), next())", "Generator functions with yield", "Memory efficiency in large data streams"],
                "code": '# Day 17: Infinite/Stream Generator\ndef count_up(start=1):\n    num = start\n    while True:\n        yield num\n        num += 1\ngen = count_up(10)\nprint([next(gen), next(gen), next(gen)])'
            },
            {
                "day": 18,
                "title": "Decorators",
                "topics": ["Higher-order functions & closures", "Writing basic decorators with @syntax", "functools.wraps & timing decorator"],
                "code": '# Day 18: Function Execution Timer Decorator\nimport time\nfrom functools import wraps\ndef timer(func):\n    @wraps(func)\n    def wrapper(*a, **kw):\n        t0 = time.perf_counter()\n        res = func(*a, **kw)\n        print(f"{func.__name__} took {(time.perf_counter()-t0)*1000:.2f}ms")\n        return res\n    return wrapper'
            }
        ]
    },
    {
        "week": "Week 4: OOP & Real-World Engineering",
        "badge": "Week 4",
        "desc": "Master object-oriented programming, REST APIs, databases, and concurrency (Days 19–27)",
        "days": [
            {
                "day": 19,
                "title": "OOP Fundamentals",
                "topics": ["Classes, objects & instances", "__init__ constructor & self keyword", "Instance attributes & instance methods"],
                "code": '# Day 19: Classes & Methods\nclass Developer:\n    def __init__(self, name: str, language: str):\n        self.name = name\n        self.language = language\n    def introduce(self):\n        return f"Hi, I\'m {self.name}, writing {self.language}!"\ndev = Developer("Alex", "Python")\nprint(dev.introduce())'
            },
            {
                "day": 20,
                "title": "OOP Advanced Pillars",
                "topics": ["Inheritance & super() calls", "Polymorphism & method overriding", "Encapsulation (private/protected attributes)"],
                "code": '# Day 20: Inheritance & Polymorphism\nclass TechLead(Developer):\n    def __init__(self, name: str, team_size: int):\n        super().__init__(name, "Python Architecture")\n        self.team_size = team_size\nlead = TechLead("Sara", 5)\nprint(lead.introduce(), f"Managing {lead.team_size} devs.")'
            },
            {
                "day": 21,
                "title": "Mini Project: Student CRUD App",
                "topics": ["Designing a domain model class", "CRUD operations (Create, Read, Update, Delete)", "Console menu interface & state management"],
                "code": '# Day 21: In-Memory CRUD Model\nclass StudentDB:\n    def __init__(self):\n        self.records = {}\n    def add(self, sid, name):\n        self.records[sid] = name\n    def get(self, sid):\n        return self.records.get(sid, "Not found")\ndb = StudentDB()\ndb.add(101, "Alex")\nprint("Lookup 101:", db.get(101))'
            },
            {
                "day": 22,
                "title": "APIs & HTTP Requests",
                "topics": ["HTTP protocol (GET, POST, headers, status codes)", "Using the requests library", "Parsing JSON responses & handling error codes"],
                "code": '# Day 22: Consuming REST APIs\nimport requests\ntry:\n    resp = requests.get("https://api.github.com", timeout=5)\n    print("GitHub API Status:", resp.status_code)\nexcept Exception as err:\n    print("Network error:", err)'
            },
            {
                "day": 23,
                "title": "Web Scraping",
                "topics": ["BeautifulSoup4 setup & HTML parsing", "Selecting tags via find() & select() CSS queries", "Extracting attributes, text & handling pagination"],
                "code": '# Day 23: HTML Extraction with BeautifulSoup\nfrom bs4 import BeautifulSoup\nhtml = "<div class=\'course\'><h1>Python 30</h1></div>"\nsoup = BeautifulSoup(html, "html.parser")\nprint("Title:", soup.find("h1").text)'
            },
            {
                "day": 24,
                "title": "Python + SQLite Database",
                "topics": ["sqlite3 standard library connection", "Executing CREATE TABLE, INSERT, SELECT queries", "Parameterized queries preventing SQL injection"],
                "code": '# Day 24: Embedded SQL Database\nimport sqlite3\nconn = sqlite3.connect(":memory:")\ncur = conn.cursor()\ncur.execute("CREATE TABLE goals (id INT, name TEXT)")\ncur.execute("INSERT INTO goals VALUES (1, \'Master Python\')")\nprint("Queried:", cur.execute("SELECT * FROM goals").fetchall())\nconn.close()'
            },
            {
                "day": 25,
                "title": "Modern Python Features",
                "topics": ["Type hinting (typing module, Optional, Union)", "@dataclass decorator for clean data structures", "Custom context managers with contextlib"],
                "code": '# Day 25: Dataclasses & Types\nfrom dataclasses import dataclass\n@dataclass\nclass CourseDay:\n    day_num: int\n    title: str\n    completed: bool = False\ntoday = CourseDay(25, "Modern Python")\nprint(today)'
            },
            {
                "day": 26,
                "title": "Testing & Debugging",
                "topics": ["Writing tests with pytest or unittest", "Assertions & test discovery", "logging module (DEBUG, INFO, ERROR)"],
                "code": '# Day 26: Test Driven Verification\ndef add(a, b): return a + b\ndef test_add():\n    assert add(2, 3) == 5\n    assert add(-1, 1) == 0\ntest_add()\nprint("All test assertions passed successfully!")'
            },
            {
                "day": 27,
                "title": "Concurrency & Asyncio",
                "topics": ["Threading for I/O bound tasks", "Multiprocessing for CPU bound tasks", "async def & await event loop fundamentals"],
                "code": '# Day 27: Async/Await Concurrency\nimport asyncio\nasync def fetch_task(name, delay):\n    await asyncio.sleep(delay)\n    return f"Done: {name}"\nasync def main():\n    res = await asyncio.gather(fetch_task("A", 0.1), fetch_task("B", 0.1))\n    print(res)\nasyncio.run(main())'
            }
        ]
    },
    {
        "week": "Week 5: Data Analytics & Capstone",
        "badge": "Week 5",
        "desc": "Analyze data with NumPy & Pandas and build your end-to-end portfolio capstone (Days 28–30)",
        "days": [
            {
                "day": 28,
                "title": "NumPy & Pandas Essentials",
                "topics": ["NumPy ndarrays & vectorized arithmetic", "Pandas DataFrames & Series creation", "Filtering rows, groupby aggregations & sorting"],
                "code": '# Day 28: DataFrames & Analytics\n# import pandas as pd\n# df = pd.DataFrame({"day": [1, 2, 3], "hours": [1.0, 1.2, 1.5]})\n# print("Mean study hours:", df["hours"].mean())\nprint("NumPy & Pandas ready for data transformations.")'
            },
            {
                "day": 29,
                "title": "Data Visualization & EDA",
                "topics": ["Matplotlib line, bar, and scatter charts", "Seaborn statistical plots & color palettes", "Exploratory data analysis & formatting insights"],
                "code": '# Day 29: Plotting Pipeline\n# import matplotlib.pyplot as plt\n# plt.plot([1, 2, 3], [10, 25, 40], marker="o")\n# plt.title("Learning Momentum")\n# plt.show()\nprint("Charts and Visual analytics pipeline prepared.")'
            },
            {
                "day": 30,
                "title": "Capstone: Sales Analytics Pipeline",
                "topics": ["End-to-end pipeline: Raw CSV -> Clean -> SQLite", "Generate summary statistics & KPI metrics", "Automated executive summary report & presentation"],
                "code": '# Day 30: Capstone Project Architecture\nprint("🎉 Congratulations! Python 30-Day Mastery Achieved.")\nprint("Portfolio Capstone: End-to-End Analytics Pipeline Built.")'
            }
        ]
    }
]

# Flattened day lookup dictionary
DAY_LOOKUP = {}
for module in ROADMAP_DATA:
    for day_item in module["days"]:
        DAY_LOOKUP[day_item["day"]] = day_item

DEFAULT_CONFIG = {
    "ntfy_topic": "python-tracker",
    "start_date": "2026-10-20",
    "reminder_time": "09:00",
    "auto_remind": True,
    "completed_days": [],
    "last_notified_date": ""
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                merged = {**DEFAULT_CONFIG, **data}
                return merged
        except Exception:
            pass
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Could not save config: {e}")

def get_day_info(cfg):
    start_str = cfg.get("start_date", "2026-10-20")
    try:
        y, m, d = map(int, start_str.split("-"))
        start = date(y, m, d)
    except Exception:
        start = date(2026, 10, 20)

    today = date.today()
    day_num = (today - start).days + 1
    total_days = 30

    if day_num < 1:
        status_text = f"Starts in {abs(day_num - 1)} day(s)"
        active_day = 1
        is_active_window = False
    elif 1 <= day_num <= total_days:
        status_text = f"Day {day_num} of {total_days}"
        active_day = day_num
        is_active_window = True
    else:
        status_text = "Roadmap Completed"
        active_day = 30
        is_active_window = False

    current_item = DAY_LOOKUP.get(active_day, DAY_LOOKUP[1])
    return {
        "day_num": day_num,
        "active_day": active_day,
        "is_active_window": is_active_window,
        "status_text": status_text,
        "today_str": today.isoformat(),
        "start_date": start_str,
        "item": current_item
    }

def send_ntfy_alert(cfg, force_day=None):
    day_info = get_day_info(cfg)
    target_day = force_day if force_day is not None else day_info["day_num"]
    topic = cfg.get("ntfy_topic", "python-tracker").strip()

    if 1 <= target_day <= 30:
        item = DAY_LOOKUP.get(target_day, DAY_LOOKUP[1])
        topics_str = ", ".join(item["topics"])
        headline = f"Python Roadmap - Day {target_day} of 30: {item['title']}"
        message = (
            f"📌 Topic: {item['title']}\n"
            f"📝 Key Concepts: {topics_str}\n\n"
            f"⏱ 1-Hour Protocol:\n"
            f"• 15m: Learn Concept\n"
            f"• 25m: Code Yourself\n"
            f"• 15m: Practice Problems\n"
            f"• 5m: Notes & Review\n\n"
            f"Consistency beats talent. Let's get it done today!"
        )
        tags = ["snake", "books"]
    elif target_day > 30:
        headline = "🎉 Python Roadmap Completed!"
        message = "Congratulations! You completed the 30-day Python roadmap! Time to build projects and revise."
        tags = ["tada", "partying_face"]
    else:
        days_left = abs(target_day - 1)
        headline = f"⏳ Python Challenge Begins in {days_left} Day(s)!"
        message = "Get your VS Code and Python environment ready. Day 1 starts soon!"
        tags = ["hourglass", "rocket"]

    actions = []
    if 1 <= target_day <= 30:
        actions = [
            {
                "action": "http",
                "label": f"Mark Day {target_day} Done",
                "url": f"https://ntfy.sh/{topic}",
                "method": "POST",
                "body": f"DONE {target_day}"
            }
        ]

    payload = {
        "topic": topic,
        "title": headline,
        "message": message,
        "priority": 4,
        "tags": tags,
        "actions": actions
    }

    try:
        resp = requests.post("https://ntfy.sh", json=payload, timeout=10)
        if resp.status_code == 200:
            return True, f"Notification published to topic '{topic}'", topic
        else:
            return False, f"HTTP {resp.status_code}: {resp.text}", topic
    except Exception as e:
        return False, str(e), topic

# Inbound Phone Listener: Listens for "DONE" messages to auto-complete days
def ntfy_listener_loop():
    import re
    time.sleep(2)
    while True:
        try:
            cfg = load_config()
            topic = cfg.get("ntfy_topic", "python-tracker").strip()
            last_reset = cfg.get("last_reset", 0)
            since_param = f"?since={last_reset}" if last_reset > 0 else "?since=1h"
            stream_url = f"https://ntfy.sh/{topic}/json{since_param}"
            print(f" [INBOUND] Listening for phone 'DONE' commands on {stream_url}...")

            with requests.get(stream_url, stream=True, timeout=65) as stream_resp:
                for line in stream_resp.iter_lines():
                    if not line:
                        continue
                    try:
                        event = json.loads(line.decode("utf-8"))
                        if event.get("event") == "message":
                            raw_msg = event.get("message", "").strip()
                            title_text = event.get("title", "")

                            # Skip outbound bot notifications
                            if "Roadmap" in title_text or "Confirmed" in raw_msg or "Completed!" in title_text:
                                continue

                            clean_msg = raw_msg.upper().replace("!", "").replace(".", "").strip()
                            if clean_msg.startswith("DONE") or clean_msg.startswith("COMPLETE") or clean_msg == "FINISHED":
                                cfg = load_config()
                                ev_time = event.get("time", 0)
                                if ev_time and ev_time <= cfg.get("last_reset", 0):
                                    continue

                                day_info = get_day_info(cfg)
                                
                                # Check if a specific day was specified (e.g. "DONE 2" or "DONE DAY 3")
                                match = re.search(r'\d+', clean_msg)
                                target_day = int(match.group()) if match else day_info["active_day"]

                                completed = set(cfg.get("completed_days", []))
                                if target_day not in completed:
                                    completed.add(target_day)
                                    cfg["completed_days"] = sorted(list(completed))
                                    save_config(cfg)
                                    pct = round((len(completed) / 30) * 100)
                                    print(f" [INBOUND SUCCESS] Automatically marked Day {target_day} as COMPLETED from phone message!")

                                    # Send confirmation push back to phone
                                    item = DAY_LOOKUP.get(target_day, DAY_LOOKUP[1])
                                    confirm_payload = {
                                        "topic": topic,
                                        "title": f"Day {target_day} Marked Done!",
                                        "message": f"Confirmed: Day {target_day} ({item['title']}) is completed!\nProgress: {len(completed)}/30 days ({pct}%).",
                                        "priority": 4,
                                        "tags": ["white_check_mark", "tada"]
                                    }
                                    try:
                                        requests.post("https://ntfy.sh", json=confirm_payload, timeout=5)
                                    except Exception:
                                        pass
                    except Exception:
                        pass
        except Exception:
            time.sleep(5)

# Background Scheduler Thread
def scheduler_loop():
    while True:
        try:
            cfg = load_config()
            if cfg.get("auto_remind", True):
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                today_str = date.today().isoformat()
                reminder_time = cfg.get("reminder_time", "09:00")

                if current_time == reminder_time and cfg.get("last_notified_date") != today_str:
                    print(f"\n[SCHEDULER] Triggering scheduled alert for {current_time}...")
                    success, msg, topic = send_ntfy_alert(cfg)
                    if success:
                        print(f"[SCHEDULER] Alert sent successfully to '{topic}'.")
                        cfg["last_notified_date"] = today_str
                        save_config(cfg)
                    else:
                        print(f"[SCHEDULER] Failed to send alert: {msg}")
        except Exception as e:
            print(f"[SCHEDULER ERROR]: {e}")
        time.sleep(30)

# HTTP Request Handler
class TrackerRequestHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Mute normal GET spam in console, only log errors/important
        if "404" in format or "500" in format:
            super().log_message(format, *args)

    def send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = self.path.split("?")[0]

        if parsed in ("/", "/index.html"):
            if os.path.exists(HTML_FILE):
                with open(HTML_FILE, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "Frontend index.html not found")
            return

        if parsed == "/api/status":
            cfg = load_config()
            info = get_day_info(cfg)
            completed = cfg.get("completed_days", [])
            total_completed = len(completed)
            percentage = round((total_completed / 30) * 100)

            self.send_json({
                "config": cfg,
                "day_info": info,
                "progress": {
                    "completed_days": completed,
                    "total_completed": total_completed,
                    "percentage": percentage,
                    "remaining": 30 - total_completed
                }
            })
            return

        if parsed == "/api/roadmap":
            self.send_json({
                "roadmap": ROADMAP_DATA
            })
            return

        self.send_error(404, "Not Found")

    def do_POST(self):
        parsed = self.path.split("?")[0]
        content_len = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        
        try:
            body = json.loads(raw_body)
        except Exception:
            body = {}

        if parsed == "/api/settings":
            cfg = load_config()
            if "ntfy_topic" in body:
                cfg["ntfy_topic"] = str(body["ntfy_topic"]).strip()
            if "start_date" in body:
                cfg["start_date"] = str(body["start_date"]).strip()
            if "reminder_time" in body:
                cfg["reminder_time"] = str(body["reminder_time"]).strip()
            if "auto_remind" in body:
                cfg["auto_remind"] = bool(body["auto_remind"])

            save_config(cfg)
            self.send_json({"success": True, "config": cfg, "day_info": get_day_info(cfg)})
            return

        if parsed == "/api/progress":
            cfg = load_config()
            day = body.get("day")
            toggle = body.get("toggle", False)
            completed = set(cfg.get("completed_days", []))

            if day is not None:
                if toggle:
                    if day in completed:
                        completed.remove(day)
                    else:
                        completed.add(day)
                else:
                    if body.get("completed", False):
                        completed.add(day)
                    else:
                        completed.discard(day)

            if "completed_days" in body and isinstance(body["completed_days"], list):
                completed = set(body["completed_days"])

            if "last_reset" in body:
                cfg["last_reset"] = int(body["last_reset"])

            cfg["completed_days"] = sorted(list(completed))
            save_config(cfg)
            self.send_json({
                "success": True,
                "completed_days": cfg["completed_days"],
                "total_completed": len(cfg["completed_days"]),
                "percentage": round((len(cfg["completed_days"]) / 30) * 100)
            })
            return

        if parsed == "/api/send-alert":
            cfg = load_config()
            target_day = body.get("day")
            success, msg, topic = send_ntfy_alert(cfg, force_day=target_day)
            self.send_json({
                "success": success,
                "message": msg,
                "topic": topic
            })
            return

        self.send_error(404, "Not Found")

def start_server():
    cfg = load_config()
    port = DEFAULT_PORT

    # Attempt to bind to DEFAULT_PORT or fallback
    server = None
    for p in [DEFAULT_PORT, 5001, 8000, 8080]:
        try:
            server = http.server.ThreadingHTTPServer(("127.0.0.1", p), TrackerRequestHandler)
            port = p
            break
        except OSError:
            continue

    if not server:
        print("[FATAL] Could not bind server to any standard port (5000, 5001, 8000).")
        sys.exit(1)

    url = f"http://127.0.0.1:{port}"
    print("=" * 68)
    print(" [APP] Python 30-Day Mastery Tracker & Daily Push Alert Application")
    print("=" * 68)
    print(f" -> Dashboard URL : {url}")
    print(f" -> Push Channel  : https://ntfy.sh/{cfg.get('ntfy_topic')}")
    print(f" -> Daily Alert   : {cfg.get('reminder_time')} (Auto: {cfg.get('auto_remind')})")
    print(f" -> Phone Reply   : Text 'DONE' to auto-complete today's task")
    print(f" -> Start Date    : {cfg.get('start_date')}")
    print("=" * 68)
    print(" Press Ctrl+C in this terminal to stop the server.\n")

    # Start background scheduler
    sched_thread = threading.Thread(target=scheduler_loop, daemon=True)
    sched_thread.start()

    # Start background phone listener for 'DONE' replies
    listener_thread = threading.Thread(target=ntfy_listener_loop, daemon=True)
    listener_thread.start()

    # Automatically launch web browser
    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped gracefully.")
        server.server_close()

if __name__ == "__main__":
    start_server()
