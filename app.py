from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# setup
app = Flask(__name__)
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

# route handler with decorator route binding
@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		task_content = request.form['content']

		if task_content == '':
			return redirect('/')

		new_task = Todo(content=task_content)
		
		try:
			db.session.add(new_task)
			db.session.commit()
			return redirect('/')
		except:
			return 'Its not good news'
	else:
		tasks = Todo.query.order_by(Todo.date_created).all()
		return render_template('index.html', tasks=tasks)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	task_to_update = Todo.query.get_or_404(id)
	
	if request.method == 'POST':
		task_to_update.content = request.form['content']

		try:
			db.session.commit()
			return redirect('/')
		except:
			return 'Its not good news'
	else:
		return render_template('update.html', task=task_to_update)

@app.route('/delete/<int:id>')
def delete(id):
	task_to_delete = Todo.query.get_or_404(id)
	
	try:
		db.session.delete(task_to_delete)
		db.session.commit()
		return redirect('/')
	except:
		return 'Its not good news'

# run script in debug mode for dev
if __name__ == "__main__":
	app.run(debug=True)
