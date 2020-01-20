from search import get_academics
from search import get_search_query
from search import get_top_level_topics

from flask import Flask, request, redirect, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'subsubtopic' in request.form:
            topic = request.form['subsubtopic']
        elif 'subtopic' in request.form:
            topic = request.form['subtopic']
        else:
            topic = request.form['topic']

        query = request.form['query']
        academics = get_academics(topic)
        search_query = get_search_query(query, academics)
        return redirect(f'https://www.google.com/search?q={search_query}')

    fields = get_top_level_topics()
    return render_template('index.html', fields=fields)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
