from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from datetime import date, datetime



app = Flask(__name__)

# Define a route to render the index.html template
@app.route('/')
def home():
    p = get_people_data()
    
    return render_template('index.html', people=p)


@app.route('/submit')
def getSubmit():
    return render_template('submit.html')

# Define a route to handle form submissions
@app.route('/submit', methods=['POST'])
def submit():

    firstname = request.form['firstname']
    lastname = request.form['lastname']
    birthday = request.form['birthday']
    email = request.form['email']
    phone = request.form['phone']
    country = request.form['country']
    city = request.form['city']
    homeaddress = request.form['homeaddress']
    postalcode = request.form['postalcode']
    nationality = request.form['nationality']
    job = request.form['job']
    contactperson = request.form['contactperson']
    phonenumberContact = request.form['phonenumberContact']
    emailContact = request.form['emailContact']


    # Save the data to a DataFrame or perform any other processing
    # Save the data to a DataFrame or perform any other processing
    save_person_data(firstname, lastname, birthday, email, phone, country, city, homeaddress, postalcode,
                     nationality, job, contactperson, phonenumberContact, emailContact)


    return redirect(url_for('home'))


# Function to load patient data from data.csv
def load_patient_data():
    try:
        df = pd.read_csv('data.csv')
        # Format phone number
        df['phone'] = df['phone'].apply(format_phone_number)
        df['phonenumberContact'] = df['phonenumberContact'].apply(format_phone_number)
        return df
    except FileNotFoundError:
        return pd.DataFrame()

# Route to display patient data based on index
@app.route('/<int:id>')
def view_patient(id):
    df = load_patient_data()
    if not df.empty and 'id' in df.columns:
        patient = df[df['id'] == id].to_dict(orient='records')
        if patient:
            return render_template('patient.html', patient=patient[0])
    return 'Patient not found'

#1,Cherguelaine,Ayoub,2000-08-12,cherguelainea@gmail.com,554372377,Algeria,blida,"beni tamou,zaouia,rue kbayli 21",9054,algeria,student,mohamed cherguelaine,555686028,ayoubchergue09@gmail.com

# Endpoint for deleting a patient
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_patient(id):
    # Logic for deleting the patient with the given ID
    try:
        df = pd.read_csv('data.csv')
        df = df.drop(df[df['id'] == id].index)
        df.to_csv('data.csv', index=False)
    except FileNotFoundError:
        pass  # Handle the file not found error

    # Redirect to the home page after deletion
    return redirect('/')


# Function to calculate age based on the birthdate
def calculate_age(birthdate):
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
    today = date.today()
    age = today.year - birthdate.year
    if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
        age -= 1
    return age


def format_phone_number(phone_number):
    # Remove any non-digit characters from the phone number
    digits = ''.join(filter(str.isdigit, str(phone_number)))
    # Add a leading zero to the phone number
    formatted_number = '0' + digits

    return formatted_number


# Function to retrieve all people's data
def get_people_data():
    # Load data from the file or database
    # For example, if you have previously saved the data in a CSV file
    df = pd.read_csv('data.csv')

    # Format phone number
    df['phone'] = df['phone'].apply(format_phone_number)

    # Calculate age for each person
    df['age'] = df['birthday'].apply(calculate_age)
    # Convert DataFrame to a list of dictionaries
    people = df.to_dict('records')
    
    return people

# Function to save a person's data
# Function to save a person's data
def save_person_data(firstname, lastname, birthday, email, phone, country, city, homeaddress, postalcode,
                     nationality, job, contactperson, phonenumberContact, emailContact):
    # Generate ID for the new patient
    try:
        df = pd.read_csv('data.csv')
        last_id = df['id'].max()
        if pd.isna(last_id):
            new_id = 1
        else:
            new_id = int(last_id) + 1
    except FileNotFoundError:
        new_id = 1

    data = pd.DataFrame({
        'id': [new_id],
        'firstname': [firstname],
        'lastname': [lastname],
        'birthday': [birthday],
        'email': [email],
        'phone': [phone],
        'country': [country],
        'city': [city],
        'homeaddress': [homeaddress],
        'postalcode': [postalcode],
        'nationality': [nationality],
        'job': [job],
        'contactperson': [contactperson],
        'phonenumberContact': [phonenumberContact],
        'emailContact': [emailContact]
        # Add more fields as required
    })

    # Append the data to an existing DataFrame or create a new one
    try:
        df = pd.read_csv('data.csv')  # If you have an existing DataFrame
        df = pd.concat([df, data], ignore_index=True)
    except FileNotFoundError:
        df = data  # If you want to create a new DataFrame

    # Save the DataFrame to a file
    df.to_csv('data.csv', index=False)



# Run the application
if __name__ == '__main__':
    app.run()