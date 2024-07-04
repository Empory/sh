from flask import Flask, request, redirect, render_template, flash
import sqlite3
import string
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choices(characters, k=6))
    return short_url

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        long_url = request.form['long_url']
        custom_short_url = request.form.get('custom_short_url', '')  # Use request.form.get to avoid KeyError
        
        conn = get_db_connection()
        if custom_short_url:
            short_url = custom_short_url
            # Check if the custom short URL already exists
            existing_url = conn.execute('SELECT * FROM urls WHERE short_url = ?', (short_url,)).fetchone()
            if existing_url:
                flash('Custom short URL already exists. Please choose another one.')
                return render_template('index.html')
        else:
            short_url = generate_short_url()
            while conn.execute('SELECT * FROM urls WHERE short_url = ?', (short_url,)).fetchone():
                short_url = generate_short_url()

        conn.execute('INSERT INTO urls (long_url, short_url) VALUES (?, ?)', (long_url, short_url))
        conn.commit()
        conn.close()
    return render_template('index.html', short_url=short_url)

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    conn = get_db_connection()
    url = conn.execute('SELECT long_url FROM urls WHERE short_url = ?', (short_url,)).fetchone()
    conn.close()
    if url is None:
        return "URL not found", 404
    return redirect(url['long_url'])

if __name__ == '__main__':
    app.run(debug=True)
