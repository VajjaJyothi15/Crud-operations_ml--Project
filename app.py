from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DB_FILE = "DB.json"

# --------------------------
# Load data from file
# --------------------------
def load_data():
    if not os.path.exists(DB_FILE):
        return []

    try:
        with open(DB_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        return []

# --------------------------
# Save data to file
# --------------------------
def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --------------------------
# Home (READ)
# --------------------------
@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

# --------------------------
# CREATE
# --------------------------
@app.route('/add', methods=['GET', 'POST'])
def add():
    data = load_data()

    if request.method == 'POST':
        new_id = 1 if len(data) == 0 else data[-1]["id"] + 1

        new_user = {
            "id": new_id,
            "name": request.form['name'],
            "age": request.form['age'],
            "gender": request.form['gender']
        }

        data.append(new_user)
        save_data(data)

        return redirect('/')

    return render_template('add.html')

# --------------------------
# UPDATE
# --------------------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    data = load_data()

    user = next((item for item in data if item["id"] == id), None)

    if request.method == 'POST':
        user["name"] = request.form['name']
        user["age"] = request.form['age']
        user["gender"] = request.form['gender']

        save_data(data)
        return redirect('/')

    return render_template('edit.html', user=user)

# --------------------------
# DELETE
# --------------------------
@app.route('/delete/<int:id>')
def delete(id):
    data = load_data()

    data = [item for item in data if item["id"] != id]

    save_data(data)
    return redirect('/')

# --------------------------
# RUN
# --------------------------
if __name__ == '__main__':
    app.run(debug=True)