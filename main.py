from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'hi'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(750))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/newpost', methods=['POST','GET'])
def newpost():
    if request.method == 'POST':
        new_title = request.form['blog-title']
        new_body = request.form['blog-body']
        
        if len(new_title)==0 and len(new_body)==0:
            flash('title and body are left blank')
            return redirect ('/newpost')
            
        elif len(new_title)==0:
            flash('title is left blank')
            return redirect ('/newpost')

        elif len(new_body)==0:
            flash('body is left blank')
            return redirect ('/newpost')

        else:
            new_blog = Blog(new_title, new_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect ('/blog?id={}'.format(new_blog.id)) 

    return render_template('newpost.html', Title='New Post')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')
    
    if blog_id == None:
        blogs = Blog.query.all()
        return render_template('blog.html', Title='Blogs', blogs=blogs)
    else:
        blog_posts = Blog.query.get(blog_id)
        return render_template('singlepost.html', Title='Single Blog', blog_posts=blog_posts)

@app.route('/')
def index():
    return render_template('base.html')

if __name__=='__main__':
    app.run()

    

    