# This is the code for a flask minimal app
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_folder="./static")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# To initialize database [removed /tmp/ to avoid making it inside a folder]
    # Both mysql and sqlite databases can be used for this to create database, here sqlite has been used since it is easy to use
    # sqlite:////tmp/test.db
    # mysql://username:password@server/db
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
        # Determines what we need to see/print when an object of this class is returned

@app.route('/', methods=['GET','POST'])
def hello_world():
    db.create_all()
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        # db.create_all()
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
        
        # print("post")
        # Initially this will not output anything, need to pass the methods list in the route too
        # After writing methods=['GET','POST'] above, it will output post in terminal
        # print(request.form['title'])
            # This will catch the value in the input box with 'name' attribute as title and print in the terminal
    
    # todo = Todo(title = "First Todo", desc = "First description")
    # db.create_all()
    # db.session.add(todo)
    # db.session.commit()
    # allTodo = Todo.query.all()
        # We basically created an instance, and this will insert data in database everytime someone visits index.html 
    return render_template('index.html', allTodo=allTodo)
    # allTodo=allTodo -> after doing this, i can use allTodo in index.html
    # render_template is used with return keyword only

@app.route('/show')
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    # Now whenever we will visit /show page, this query will execute the repr function and print all instances of todos
    return "showing all todos in terminal"
    # [1 - First Todo, 2 - First Todo, 3 - First Todo, 4 - First Todo, 5 - First Todo]
    # This is the output returned in the terminal
    
@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    # // basically update/1 pe hi rhke mai update/1 pe post request maar rha hu to update the data with the new record
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        # We fetched the old todo
        todo.title = title
        todo.desc = desc
        # We updated the old todo with the new values
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

    
@app.route('/delete/<int:sno>') # Way to define a parameter
def delete(sno):
    todo_delete = Todo.query.filter_by(sno=sno).first()
    # Did .first() to identify the first record that we want to delete
    # this will bring us the required query as per the parameter we have passed
    db.session.delete(todo_delete)
    db.session.commit()
    # print(allTodo)
    return redirect("/")
    # This will redirect the page to home page after this function gets exceuted
    

if __name__ == '__main__':
    app.run(debug=True)