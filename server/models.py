from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("name is required")
        author = db.session.query(Author.id).filter_by(name = name).first()
        if author is not None:
            raise ValueError("name must be unique")
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if len(number) != 10 or not number.isdigit():
            raise ValueError('Phone number must only be 10 digits long')
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        if len(content) != 250:
            raise ValueError("content has to be atleast 250 characters")
        return content

    @validates('summary')
    def validates_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("summary maximum limit is 250")
        return summary

    @validates('category')
    def validates_category(self, key, cate):
        if cate != 'Fiction' and cate != 'Non-Fiction':
            raise ValueError("Category must be either fiction or non-fiction")
        return cate

    @validates('title')
    def validates_title(self, key, title):
        arr = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(bait in title for bait in arr):
            raise ValueError("title must contain a click bait title")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
