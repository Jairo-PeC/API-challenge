from flask import Flask, jsonify
import csv
from employees_schema import init_db, insert_data, get_db_connection
from pathlib import Path

app = Flask(__name__)

# Initialize the database
init_db()

# Endpoint to insert hired employees
@app.route('/employees_schema/insert/hired_employees', methods=['POST'])
def insert_hired_employees():
    try:
        path = (Path(__file__).parent / "../hired_employees.csv").resolve()
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=['id', "name", "datetime", "department_id", "job_id"])
            data = [(row['id'], row['name'], row['datetime'], row['department_id'], row['job_id']) for row in reader]
            
        # Convert datetime strings to ISO format
        data = [(row[0], row[1], row[2].replace('Z', '+00:00'), row[3], row[4]) for row in data]

        if insert_data('hired_employees', data):
            return jsonify({'message': 'Data from hired_employees inserted successfully'}), 201
        else:
            return jsonify({'error': 'Failed to insert data from hired_employees'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to insert departments
@app.route('/employees_schema/insert/departments', methods=['POST'])
def insert_departments():
    try:
        path = (Path(__file__).parent / "../departments.csv").resolve()
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=['id', "department"])
            data = [(row['id'], row['department']) for row in reader]

        if insert_data('departments', data):
            return jsonify({'message': 'Data from departments inserted successfully'}), 201
        else:
            return jsonify({'error': 'Failed to insert data from departments'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to find employees by quarter in 2021
@app.route('/employees_schema/insert/jobs', methods=['POST'])
def insert_jobs():
        try:
            path = (Path(__file__).parent / "../jobs.csv").resolve()
            with open(path, newline='') as csvfile:
                reader = csv.DictReader(csvfile, fieldnames=['id', "job"])
                data = [(row['id'], row['job']) for row in reader]

            if insert_data('jobs', data):
                return jsonify({'message': 'Data from jobs inserted successfully'}), 201
            else:
                return jsonify({'error': 'Failed to insert data from jobs'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Endpoint to view jobs by quarter
@app.route('/employees_schema/jobsByQuarter', methods=['GET'])
def jobsByQuarter():
        try:
            conn = get_db_connection()
            c = conn.cursor()
            #Ordered results are shown as intended without ORDER BY 
            query = """SELECT dep.department, job.job, 
            SUM(CASE WHEN strftime('%m', emp.datetime) <= '03' THEN 1 ELSE 0 END) AS Q1,
            SUM(CASE WHEN strftime('%m', emp.datetime) BETWEEN '04' AND '06' THEN 1 ELSE 0 END) AS Q2,
            SUM(CASE WHEN strftime('%m', emp.datetime) BETWEEN '07' AND '09' THEN 1 ELSE 0 END) AS Q3,
            SUM(CASE WHEN strftime('%m', emp.datetime) BETWEEN '10' AND '12' THEN 1 ELSE 0 END) AS Q4                    
                    FROM hired_employees emp
                    JOIN departments dep ON emp.department_id = dep.id
                    JOIN jobs job ON emp.job_id = job.id
                    WHERE strftime('%Y', emp.datetime) = '2021'
                    GROUP BY dep.department, job.job;
            """
            c.execute(query)
            records = c.fetchall()
            
            c.close()
            if len(records) > 0:
                return jsonify({'Jobs by quarter sent successfully': records}), 200
            else:
                return jsonify({'error': 'Could not retrieve data'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            if c:
                c.close()

# Endpoint to view jobs by quarter
@app.route('/employees_schema/departmentsAboveTheMean', methods=['GET'])
def departmentsAboveTheMean():
        try:
            conn = get_db_connection()
            c = conn.cursor()
            #Ordered results are shown as intended without ORDER BY 
            query = """WITH department_hired AS (
                            SELECT 
                                d.id AS department_id,
                                d.department,
                                COUNT(e.id) AS num_employees_hired
                            FROM 
                                hired_employees e
                            JOIN 
                                departments d ON e.department_id = d.id
                            WHERE 
                                strftime('%Y', e.datetime) = '2021'
                            GROUP BY 
                                d.id
                        ),
                        mean_hired AS (
                            SELECT 
                                AVG(num_employees_hired) AS mean_hired_2021
                            FROM 
                                department_hired
                        )

                        SELECT 
                            dh.department_id AS id,
                            dh.department AS name,
                            dh.num_employees_hired
                        FROM 
                            department_hired dh,
                            mean_hired mh
                        WHERE 
                            dh.num_employees_hired > mh.mean_hired_2021
                        ORDER BY 
                            dh.num_employees_hired DESC;

            """
            c.execute(query)
            records = c.fetchall()
            
            c.close()
            if len(records) > 0:
                return jsonify({'Hired employees by department above the mean sent successfully': records}), 200
            else:
                return jsonify({'error': 'Could not retrieve data'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            if c:
                c.close()

if __name__ == '__main__':
    app.run(debug=True)


