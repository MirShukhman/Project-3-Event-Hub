from . import db

# 24.02.24
# Mir Shukhman
#Definig&Creating Users table in db
class Users(db.Model):
    __tablename__ = 'Users'
    
    UserID = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(50), nullable=False, unique=True)
    PasswordHash = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(50), nullable=False, unique=True)
    FullName = db.Column(db.String(100), nullable=False) 
    ProfileDescription=db.Column(db.String(1000)) 
    CreatedAt=db.Column(db.DateTime)
    IsActive = db.Column(db.Boolean, default=True)
    IsMasterUser = db.Column(db.Boolean, default=False)


    