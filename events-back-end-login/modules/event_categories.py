from . import db

# 24.02.24
# Mir Shukhman
#Definig&Creating EventCategories table in db
class EventCategories(db.Model):
    __tablename__ = 'EventCategories'
    
    CategoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EventCategory = db.Column(db.String(50), nullable=False, unique=True)
    Description = db.Column(db.String(1000))
