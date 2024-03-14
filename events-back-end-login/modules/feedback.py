from . import db

# 24.02.24
# Mir Shukhman
#Definig&Creating Feedback table in db
class Feedback(db.Model):
    __tablename__ = 'Feedback'
    
    FeedbackID = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    RegistrationID = db.Column(db.BigInteger, db.ForeignKey('Registrations.RegistrationID'), nullable=False)
    Raiting = db.Column(db.Integer)
    Comment = db.Column(db.String(1000))
    SubmittionDateTime = db.Column(db.DateTime, nullable=False)
    
    

    



    