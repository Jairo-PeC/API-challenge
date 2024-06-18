from flask import Flask, jsonify, request
import csv
from datetime import datetime
from employees_schema import init_db, insert_data
from pathlib import Path

app = Flask(__name__)

# Initialize the database
init_db()

# Endpoint to insert hired employees
@app.route('/employees_schema/insert/hired_employees', methods=['POST'])
def insert_hired_employees():
    try:
        path = (Path(__file__).parent / "../hired_employees.csv").resolve()
        print(path)
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile,  fieldnames=['id', "name", "datetime", "department_id", "job_id"])
            data = [(row['id'], row['name'], row['datetime'], row['department_id'], row['job_id']) for row in reader]
            
        # Convert datetime strings to ISO format
        data = [(row[0], row[1], row[2].replace('Z', '+00:00'), row[3], row[4]) for row in data]

        if insert_data('hired_employees', data):
            return jsonify({'message': 'Data inserted successfully'}), 201
        else:
            return jsonify({'error': 'Failed to insert data'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)


