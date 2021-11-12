from flask_sqlalchemy import SQLAlchemy
from Website import app

database = SQLAlchemy(app)

print("Init database...")
class ColorCombination(database.Model):
    __bind_key__ = 'color_combinations'

    num =  database.Column(database.INT(),primary_key=True,autoincrement=True )
    color_1 = database.Column(database.String(7),nullable=False)
    color_2 = database.Column(database.String(7),nullable=False)
    color_3 = database.Column(database.String(7),nullable=True)
    color_4 = database.Column(database.String(7),nullable=True)
    color_5 = database.Column(database.String(7),nullable=True)
    size = database.Column(database.SMALLINT(),nullable=False)

    def __repr__(self):
        return '<Color set #%d: %s,%s,%s,%s,%s [%d colors]>' % (self.num,self.color_1,self.color_2,self.color_3,self.color_4,self.color_5,self.size)

class Project(database.Model):
    __bind_key__ = 'main'

    name =  database.Column(database.Text, primary_key=True)
    description = database.Column(database.Text, default="Not found")
    image = database.Column(database.Text, nullable=False, default="not_found.png")
    link = database.Column(database.Text)

    def __repr__(self):
        return '<Project %s, translated: %s>' % (self.name, self.translated)

database.create_all(bind=['color_combinations','main'])

