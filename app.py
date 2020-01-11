from search import get_academics, get_search_query
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        academics = get_academics(query)
        search_query = get_search_query(query, academics)
        return redirect(f'https://www.google.com/search?q={search_query}')

    return app.send_static_file('factcheck.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port= 8000, debug=True)