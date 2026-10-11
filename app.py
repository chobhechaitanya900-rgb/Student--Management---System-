from flask import Flask, request, redirect, render_template_stringimport sqlite3
import os
app = Flask(__name__)
DATABASE = "students.db"
HTML = """<!DOCTYPE html><html><head> <title>Student Management System</title> 
<meta name="viewport" content="width=device-width, initial-scale=1">
 <style> body { margin: 0; font-family: Arial, sans-serif; background: #f1f5f9;
 color: #1e293b; }
 header { background: #172554; color: white; padding: 22px; text-align: center;
 }
 header h1 { margin: 0 0 8px; }
 .container { max-width: 1000px; margin: 25px auto; padding: 15px; }
 .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 
1fr)); gap: 15px; }
 .card, .panel { background: white; padding: 20px; border-radius: 12px; 
box-shadow: 0 2px 8px #00000012; margin-bottom: 20px; }
 .card h2 { color: #2563eb; margin-bottom: 5px; }
 input { box-sizing: border-box; width: 100%; padding: 12px; margin: 7px 0 
12px; border: 1px solid #cbd5e1; border-radius: 7px; }
 button { background: #2563eb; color: white; border: 0; padding: 11px 17px; 
border-radius: 7px; cursor: pointer; }
 .delete { background: #dc2626; }
 .search { display: flex; gap: 8px; }
 .search input { flex: 1; }
 .table-wrap { overflow-x: auto; }
 table { width: 100%; border-collapse: collapse; background: white; }
 th, td { text-align: left; padding: 12px; border-bottom: 1px solid #e2e8f0; }
 th { background: #eff6ff; }
 footer { text-align: center; padding: 20px; color: #64748b; } </style></head>
<body>
<header> <h1>Student Management System</h1> <p>Navsahyadri College of 
Engineering</p> <p>Data Structure Mini Project</p></header>
<div class="container">
 <div class="cards"> <div class="card"> <p>Total Students</p> <h2>{{ 
students|length }}</h2> </div>
 <div class="card"> <p>Project Subject</p> <h2>Data Structure</h2> </div>
 <div class="card"> <p>Developed By</p> <h2>Chaitanya Chobhe</h2> </div> </div>
 <div class="panel"> <h2>Add New Student</h2>
 <form action="/add" method="POST"> <label>Roll Number</label> <input 
type="number" name="roll" required>
 <label>Student Name</label> <input type="text" name="name" required>
 <label>Course</label> <input type="text" name="course" required>
 <label>Email</label> <input type="email" name="email">
 <button type="submit">Add Student</button> </form> </div>
 <div class="panel"> <h2>Search Students</h2>
 <form action="/" method="GET" class="search"> <input type="text" name="q" 
placeholder="Search name or roll number" value="{{ query }}"> <button 
type="submit">Search</button> </form> </div>
 <div class="panel"> <h2>Student Records</h2>
 <div class="table-wrap"> <table> <tr> <th>Roll No.</th> <th>Name</th> 
<th>Course</th> <th>Email</th> <th>Action</th> </tr>
 {% for student in students %} <tr> <td>{{ student[0] }}</td> <td>{{ 
student[1] }}</td> <td>{{ student[2] }}</td> <td>{{ student[3] }}</td> <td> 
<form action="/delete/{{ student[0] }}" method="POST" onsubmit="return 
confirm('Delete this student?')"> <button class="delete" type="submit"> Delete 
</button> </form> </td> </tr> {% else %} <tr> <td colspan="5">No student 
records found.</td> </tr> {% endfor %} </table> </div> </div>
</div>
<footer> Student Management System | Project By Chaitanya Chobhe</footer>
</body></html>"""

def get_db(): connection = sqlite3.connect(DATABASE) connection.execute(""" 
CREATE TABLE IF NOT EXISTS students ( roll INTEGER PRIMARY KEY, name TEXT NOT 
NULL, course TEXT NOT NULL, email TEXT ) """) return connection

@app.route("/")def home(): query = request.args.get("q", "").strip()
 with get_db() as connection: if query: students = connection.execute(""" 
SELECT roll, name, course, email FROM students WHERE CAST(roll AS TEXT) LIKE ? 
OR name LIKE ? ORDER BY roll """, (f"%{query}%", f"%{query}%")).fetchall() else:
 students = connection.execute(""" SELECT roll, name, course, email FROM 
students ORDER BY roll """).fetchall()
 return render_template_string( HTML, students=students, query=query )

@app.route("/add", methods=["POST"])def add_student(): roll = 
request.form["roll"] name = request.form["name"].strip() course = 
request.form["course"].strip() email = request.form.get("email", "").strip()
 if not name or not course: return "Name and course are required.", 400
 try: with get_db() as connection: connection.execute(""" INSERT INTO students 
(roll, name, course, email) VALUES (?, ?, ?, ?) """, (roll, name, course, 
email)) except sqlite3.IntegrityError: return "This roll number already exists. 
Go back and try again.", 400
 return redirect("/")

@app.route("/delete/<int:roll>", methods=["POST"])def delete_student(roll): 
with get_db() as connection: connection.execute( "DELETE FROM students WHERE 
roll = ?", (roll,) )
 return redirect("/")

if __name__ == "__main__": port = int(os.environ.get("PORT", 5000)) 
app.run(host="0.0.0.0", port=port, debug=False)