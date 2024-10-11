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
        author=Author.query.filter_by(name=name).first()
        if len(name) == 0:
            raise ValueError("All authors must have a name.")
        if author is not None:
            raise ValueError("No two authors can have the same name.")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and len(phone_number) != 10:
            raise ValueError("Author phone numbers must be exactly ten digits.")
        if phone_number and not phone_number.isdigit():
            raise ValueError("Author phone numbers must be numeric.")
        return phone_number


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
    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Post title is sufficiently clickbait-y and must contain one of the following: (Won't Believe, Secret, Top, Guess)")
        return title

    @validates('content') 
    def validate_content(self, key, content):
        if content and len(content) < 250:
            raise ValueError("Post content is at least 250 characters long.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Post summary is a maximum of 250 characters.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category!='Fiction' and category!='Non-Fiction':
            raise ValueError('Post category is either Fiction or Non-Fiction.')
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
