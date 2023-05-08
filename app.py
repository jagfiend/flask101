from datetime import datetime
from flask import Flask, flash, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# setup
app = Flask(__name__)
app.secret_key = b'somethingsomethingdarkside' # need a session to use flashes and session needs a secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# model
class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(255), nullable=False)
	completed = db.Column(db.Boolean, default=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Task %r>' % self.id

# build the db
with app.app_context():
        db.create_all()

# route handlers with decorator route binding
@app.get('/')
def index():
	tasks = Todo.query.order_by(Todo.date_created).all()
	return render_template('index.html', tasks=tasks)
	
@app.post('/')
def create():
	task_content = request.form['content']

	if task_content == '':
		return redirect('/')

	new_task = Todo(content=task_content)
	
	try:
		db.session.add(new_task)
		db.session.commit()
		flash('New task added successfully', 'success')
	except:
		flash('There was a problem creating this task', 'error')

	return redirect('/')	
	
# adding post and put to update route to handle both http and html form submissions
@app.route('/update/<int:id>', methods=["POST", "PUT"])
def update(id):
	task_to_update = Todo.query.get_or_404(id)
	task_to_update.content = request.form['content']

	try:
		db.session.commit()
		flash('Task successfully updated', 'success')
	except:
		flash('There was a problem updating this task.', 'error')

	return redirect('/')

# adding post and delete to update route to handle both http and html form submissions	
@app.route('/delete/<int:id>', methods=["POST", "DELETE"])
def delete(id):
	task_to_delete = Todo.query.get_or_404(id)
	
	try:
		db.session.delete(task_to_delete)
		db.session.commit()
		flash('Task successfully deleted', 'success')
	except:
		flash('There was a problem deleting this task.', 'error')

	return redirect('/')

# run script in debug mode for dev
if __name__ == "__main__":
	app.run(debug=True)
