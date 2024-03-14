from . import db

# 24.02.24
# Mir Shukhman
#Definig&Creating EventImages table in db
class EventImages(db.Model):
    __tablename__ = 'EventImages'
    
    ImageID = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    EventID= db.Column(db.BigInteger, db.ForeignKey('Events.EventID'), nullable=False)
    Image = db.Column(db.LargeBinary, nullable=False)
    UserID =  db.Column(db.BigInteger, db.ForeignKey('Users.UserID'), nullable=False)
    SubmittionDateTime = db.Column(db.DateTime, nullable=False)
    
    

    



    