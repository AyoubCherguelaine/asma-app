from flask import Flask, render_template, request, redirect, url_for

import pandas as pd

app = Flask(__name__)

# Define a route to render the index.html template
@app.route('/')
def home():
    return render_template('index.html', people=get_people_data())


@app.route('/submit')
def getSubmit():
    return render_template('submit.html')

# Define a route to handle form submissions
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    # Add more fields as required

    # Save the data to a DataFrame or perform any other processing
    save_person_data(name, age)

    return redirect(url_for('home'))

# Function to retrieve all people's data
def get_people_data():
    # Load data from the file or database
    # For example, if you have previously saved the data in a CSV file
    df = pd.read_csv('data.csv')

    # Convert DataFrame to a list of dictionaries
    people = df.to_dict('records')

    return people

# Function to save a person's data
def save_person_data(name, age):
    data = pd.DataFrame({
        'Name': [name],
        'Age': [age]
        # Add more fields as required
    })

    # Append the data to an existing DataFrame or create a new one
    df = pd.read_csv('data.csv')  # If you have an existing DataFrame
    df = pd.concat([df, data], ignore_index=True)
    #df = data  # If you want to create a new DataFrame

    # Save the DataFrame to a file
    df.to_csv('data.csv', index=False)

# Run the application
if __name__ == '__main__':
    app.run()