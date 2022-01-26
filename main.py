from app import app
from db import mysql
import pymysql
from flask import request, jsonify


@app.route("/employees")
def Employees():
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select * from employee")
        rows = cursor.fetchall()
        response = jsonify(rows)
        response.status_code = 200
        cursor.close()
        connection.close()
    except Exception as e:
        print(e)
        response = jsonify('Failed to fetch Employees')
        response.status_code = 400
    finally:
        return response


@app.route('/employee/<int:id>')
def getEmployeeById(id):
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select * from employee where empId=%s", id)
        rows = cursor.fetchall()
        response = jsonify(rows)
        response.status_code = 200
        cursor.close()
        connection.close()
    except Exception as e:
        print(e)
        response = jsonify({"Employee": 'Employee not found on id'+id})
        response.status_code = 400
    finally:
        return response


@app.route('/addEmployee', methods=['POST'])
def addEmployee():
    try:
        _json = request.json
        print(_json)
        _name = _json['empName']
        _email = _json['empEmail']
        if _name and _email and request.method == 'POST':
            sql = "INSERT INTO employee(empName,empEmail)VALUES(%s,%s)"
            data = (_name, _email)
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute(sql, data)
            connection.commit()
            response = jsonify('Employee has been added in db Successfully')
            response.status_code = 200
            cursor.close()
            connection.close()
        else:
            response = jsonify('Body not fouond')
            response.status_code = 400
    except Exception as e:
        print(e)
        response = jsonify('Failed to Add Employee')
        response.status_code = 400

    finally:
        return response


@app.route('/delete/<int:id>', methods=['DELETE'])
def deleteEmployeebyId(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employee WHERE empId=%s", (id))
        conn.commit()
        response = jsonify('Employee deleted successfully!')
        response.status_code = 200
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)
        response = jsonify('Failed to Delete Employee')
        response.status_code = 400
    finally:
        return response


@app.route('/updateEmployee/<int:id>', methods=['PUT'])
def updateEmployee(id):
    try:
        _json = request.json
        _name = _json['empName']
        _email = _json['empEmail']
       
        if _name and _email and request.method == 'PUT':
            
            sql = (
                "UPDATE employee SET empName=%s, empEmail=%s WHERE empId=%s")
            data = (_name, _email, id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            response = jsonify(' Employee has been updated successfully!')
            response.status_code = 200
            cursor.close()
            conn.close()
        else:
            response = jsonify('Body not found for update')
            response.status_code = 400
    except Exception as e:
        print(e)
        response = jsonify('Faild to Update')
        response.status_code = 400
    finally:
        
        return response


@app.errorhandler(404)
def otherRoutes(error=None):
    response = jsonify({'status': 404, 'message': 'Not Found:'+request.url, })
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)
