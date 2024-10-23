from hyoprj import db

class Rank(db.Model):
    id = db.Column(db.String(40),primary_key=True)
    userid = db.Column(db.String(10),nullable=False)
    usertype = db.Column(db.String(1),nullable=False)  #1이면 휴대폰 , 2이면 효문화
    score = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)