from . import db

# 24.02.24
# Mir Shukhman
#Definig&Creating Registrations table in db
class Registrations(db.Model):
    __tablename__ = 'Registrations'
    
    RegistrationID = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    EventID= db.Column(db.BigInteger, db.ForeignKey('Events.EventID'), nullable=False)
    UserID =  db.Column(db.BigInteger, db.ForeignKey('Users.UserID'), nullable=False)
    RegistrationDateTime = db.Column(db.DateTime, nullable=False)
    Status = db.Column(db.String(50))
    

    



    