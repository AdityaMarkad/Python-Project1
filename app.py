from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

EVENT_FILE = "events.json"

def load_events():
    try:
        with open(EVENT_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_events(events):
    with open(EVENT_FILE, "w") as f:
        json.dump(events, f, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create_event():
    events = load_events()
    if request.method == "POST":
        event_id = request.form["event_id"]
        if event_id in events:
            return "Event ID already exists!"

        events[event_id] = {
            "name": request.form["name"],
            "date": request.form["date"],
            "venue": request.form["venue"],
            "participants": []
        }

        save_events(events)
        return redirect("/")
    return render_template("create_event.html")

@app.route("/register", methods=["GET", "POST"])
def register_participant():
    events = load_events()
    if request.method == "POST":
        event_id = request.form["event_id"]
        if event_id not in events:
            return "Event not found!"

        events[event_id]["participants"].append({
            "name": request.form["name"],
            "email": request.form["email"]
        })

        save_events(events)
        return redirect("/")
    return render_template("register.html")

@app.route("/events")
def view_events():
    events = load_events()
    return render_template("view_events.html", events=events)

@app.route("/report/<event_id>")
def report(event_id):
    events = load_events()
    if event_id not in events:
        return "Event Not Found"
    return render_template("report.html", event=events[event_id], event_id=event_id)

if __name__ == "__main__":
    app.run(debug=True)
