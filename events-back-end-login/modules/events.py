from . import db

# 24.02.24
# Mir Shukhman
#Definig&Creating Events table in db
class Events(db.Model):
    __tablename__ = 'Events'
    
    EventID = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(1000))
    Location = db.Column(db.String(300), nullable=False)
    EventDateTime = db.Column(db.DateTime, nullable=False)
    EventImage = db.Column(db.LargeBinary)
    OrganizerID =  db.Column(db.BigInteger, db.ForeignKey('Users.UserID'), nullable=False)
    CategoryID =  db.Column(db.Integer, db.ForeignKey('EventCategories.CategoryID'), nullable=False)
    IsPrivate= db.Column(db.Boolean, nullable=False)
    IsCanceled= db.Column(db.Boolean, default=False, nullable=False)
    



    