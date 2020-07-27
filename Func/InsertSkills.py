import sqlite3

class InsertSkills:
    def addSkills(self):
        conn = sqlite3.connect("Result.db")
        c = conn.cursor()
        c.execute("SELECT keySkills FROM Result")
        row=c.fetchall()
        c.execute("INSERT INTO Skills (kSkills) VALUES (?,)",(row))
        conn.commit()
        c.close()
        conn.close()