import sqlite3
import os
import subprocess
import sys

class SkillTracker:
    def __init__(self):
        self.db = sqlite3.connect("app.db")
        self.cr = self.db.cursor()
        self._create_table()

    def _create_table(self):

        self.db.execute("""
        create table if not exists users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name text UNIQUE
        )
    """)
        

        self.db.execute("""
        create table if not exists skills(
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name text,
            progress integer,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

        
    def clear(self):
    #Checks if the OS is Windows ('nt'), uses 'cls', otherwise uses 'clear
     subprocess.run('cls' if os.name == 'nt' else 'clear', shell = True)

    def check(self):
     """To confirm your wish to continue or leave"""
     while True:
         print('<>' * 20)
         ch = input("Do you want to restart the program ? (n/y) : ").strip().lower()
         self.clear()
         if ch and ch == 'y':
             return

         elif ch and ch == 'n':
             sys.exit()

         else:
             self.clear()
             print("Please Enter  only (n => NO) or (y => YES)")

    def save(self):
        """File for save orders and close this file in the end!"""
        self.db.commit()

    def get_input(self,prompt):
        """Get non-empty input from user"""
        while True:
            value = input(prompt).strip().capitalize()
            if value:
                return value
            print("Cannot be empty!")

    def get_progress(self):
        """Get valid progress number from user"""
        while True:
            prog = input("Enter your progress (0-100): ").strip()
            if prog.isdigit() and 0 <= int(prog) <= 100:
                return int(prog)
            print("Please enter a valid number between 0 and 100!")
            self.clear()

    def add(self):
        """To add skills"""
        user_name = self.get_input("Enter Your name : ")
        self.clear()

        name = self.get_input("Enter Your Skill name: ")
        self.clear()    

        prog = self.get_progress()
        self.clear()

        self.cr.execute("select user_id from users where user_name = ?", (user_name,))
        user = self.cr.fetchone()

        if user is None:
          self.cr.execute("insert into users(user_name) values(?)", (user_name,))
          user_id = self.cr.lastrowid
        else:
            user_id = user[0]

        self.cr.execute(
        "select * from skills where user_id = ? and name = ?",
        (user_id, name,)
        )

        result = self.cr.fetchone()

        if result is None:
          self.cr.execute("insert into skills(name, progress, user_id) values(?, ?, ?)", (name, prog, user_id))
          self.save()  

        else:
          print("Your Name Is Already exists!")

    def update(self):
        """To update progress of skills"""
        user_name = self.get_input("Enter Your name : ")
        self.clear()

        name = self.get_input("Enter Your Skill name: ")
        self.clear()    

        prog = self.get_progress()
        self.clear()


        self.cr.execute("select user_id from users where user_name = ?", (user_name,))
        user = self.cr.fetchone()

        if user is None:
           print("User not found!")
           return

        user_id = user[0]

        self.cr.execute(
         "update skills set progress = ? where user_id = ? and name = ?",
         (prog, user_id, name))

        if self.cr.rowcount > 0:
            self.save()
        else:
            print("Your Name or Skill Is Not exists!, Go to add for insert your skills :)")        

    def delete(self):
        """To delete users or skills"""
        print("What do you want to delete ?")
        print("-" * 50)
        print("'n' => One Skill")
        print("'u' => All Skill For Specific UserName")
        print("'a' => All Data ")
        print("-" * 50)
        op = input("Enter Your Choice : ").strip().lower()
        self.clear()


        if op and op == 'n':
            name = input("Enter Skill Name You Want Remove : ").strip().capitalize()
            self.clear()
            user_name = input("Enter the username of the user whose skill you want to remove : ").strip().capitalize()
            self.clear()

            self.cr.execute("select user_id from users where user_name = ?", (user_name,))
            user = self.cr.fetchone()

            if user is None:
                print("User not found!")
                return

            user_id = user[0]

            self.cr.execute("delete from skills where name = ? and user_id = ?", (name, user_id))
            self.save()

        elif op and op == 'u':
            user_name = input("Enter UserName You Want delete : ").strip().capitalize()
            
            self.cr.execute("select user_id from users where user_name = ?", (user_name,))
            user = self.cr.fetchone()

            if user is None:
                print("User not found!")
                return

            user_id = user[0]
            
            self.cr.execute("delete from skills where user_id = ?", (user_id,))
            self.save()

        elif op == 'a':
            self.cr.execute("select count(*) from skills")
            count = self.cr.fetchone()[0]
    
            if count > 0:
               self.cr.execute("delete from skills")
               self.cr.execute("delete from users")
               self.save()

               self.db = sqlite3.connect("app.db")
               self.cr = self.db.cursor()
            else:
                print("You don't have any data")


        else:
            print("Invalid Entering !!!")
            self.check()

    def show_data(self):
        """To display te data you want"""
        print("What are you want show ?")
        print("'a' => Show All Data")
        print("'s' => show data for  Specific UserName")
        print("'n' => show number of Users or skills saved")
        print("-" * 50)
        op = input("Enter Your Option : ").strip().lower()
        self.clear()

        if op == 'a':
            self.cr.execute("select users.user_name, users.user_id, skills.name, skills.progress from skills" \
            " join users on skills.user_id = users.user_id")
            All = self.cr.fetchall()
            for inf in All:
                print(f"UserName : {inf[0]}")
                print(f"UserID : {inf[1]}")
                print(f"Skill Name: {inf[2]}")
                print(f"progress : {inf[3]}%")
                print('_' * 50)

        elif op == 's':
            user_name = input("Enter UserName: ").strip().capitalize()
            self.clear()

            self.cr.execute("select user_id from users where user_name = ?", (user_name,))
            user = self.cr.fetchone()

            if user is None:
                print("User not found!")
                return

            user_id = user[0]

            self.cr.execute("select users.user_name, users.user_id, skills.name, skills.progress from skills" \
            " join users on skills.user_id = users.user_id where skills.user_id = ?", (user_id,))
            All = self.cr.fetchall()
            for inf in All:
                print(f"UserName : {inf[0]}")
                print(f"UserID : {inf[1]}")
                print(f"Skill Name: {inf[2]}")
                print(f"progress : {inf[3]}%")
                print('_' * 50)

        elif op == 'n':
            self.cr.execute("select count(*) from skills")
            All = self.cr.fetchone()[0]
            self.cr.execute("select count(distinct user_id) from skills")
            names = self.cr.fetchone()[0]
            print(f"Number Of Users : {names}")
            print(f"Number Of Skills : {All}")
            print('_' * 50)

        else:
            print("Invalid Entering !!!")
            self.check()    

    def quit(self):
        """To exit the program"""
        self.db.close()
        print("Your Operation Is Complete!")
        print("***************************" )
        print("Thanks For Use My Program :)")   
        print("^_~")  

    def play(self):
        print("What do you want to do ?")
        print("'a' => Add New Skill")
        print("'u' => Update Skill Progress")
        print("'d' => Delete A Skill")
        print("'s' => Show All Data")
        print("'q' => Quit The App")
        print("-" * 50)
        op = input("Chose Your Option: ").strip().lower()
        print("-" * 50)
        self.clear()


        if op == 'a':
            self.add()
            self.check()

        elif op == 'u':
            self.update()
            self.check()

        elif op == 'd':
            self.delete()
            self.check()

        elif op == 's':
            self.show_data()
            self.check()

        elif op == 'q':
            self.quit()
            self.check()

        else:
            print("Invalid Entering !!!")
            self.check()




if __name__ == "__main__":
    App = SkillTracker()
    while(True):
        App.play()
