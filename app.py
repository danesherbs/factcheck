from search import get_academics
from search import get_search_query
from search import get_top_level_topics
from search import get_child_topics

from flask import Flask, request, redirect, render_template

app = Flask(__name__)

topics = {
    "high": get_top_level_topics(),
    "medium": [],
    "low": [],
}

selected = {
    "high": "art",
}


@app.route("/", methods=["GET", "POST"])
def index():
    global topics
    global selected

    if request.method == "POST" and "subsubtopic" in request.form:
        subsubtopic = request.form["subsubtopic"]

        topics = {
            "high": topics["high"],
            "medium": topics["medium"],
            "low": topics["low"],
        }

        selected = {
            "high": selected["high"],
            "medium": selected["medium"],
            "low": subsubtopic,
        }

    elif request.method == "POST" and "subtopic" in request.form:
        subtopic = request.form["subtopic"]

        topics = {
            "high": topics["high"],
            "medium": topics["medium"],
            "low": get_child_topics(subtopic),
        }

        selected = {
            "high": selected["high"],
            "medium": subtopic,
        }

    elif request.method == "POST" and "topic" in request.form:
        topic = request.form["topic"]

        topics = {
            "high": topics["high"],
            "medium": get_child_topics(topic),
            "low": [],
        }

        selected = {
            "high": topic,
        }

    elif request.method == "POST" and "query" in request.form:
        query = request.form["query"]

        if "low" in selected:
            topic = selected["low"]
        elif "medium" in selected:
            topic = selected["medium"]
        else:
            topic = selected["high"]

        academics = get_academics(topic)
        search_query = get_search_query(query, academics)
        return redirect(f"https://www.google.com/search?q={search_query}")

    return render_template("index.html", topics=topics, selected=selected)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
