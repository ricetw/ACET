from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from werkzeug.security import generate_password_hash

from configs import SQL_Server
from models import Medical_Staff

from apis.web import web_bp

engine = create_engine(SQL_Server)
Session = sessionmaker(bind=engine)
dbsession = Session()

app = Flask(__name__, static_folder='static')
app.config.from_pyfile('./configs.py')

app.register_blueprint(web_bp, url_prefix='/web')

@app.route('/')
def home():
    sql = text('select * from Medical_Staff')
    row = dbsession.execute(sql).fetchall()
    print(row)
    return "OK"

if __name__ == '__main__':
    sql = text('select * from Medical_Staff where ms_id = :ms_id')
    data = [{"ms_id": "admin"}]
    row = dbsession.execute(sql, data).fetchall()
    if not row:
        dbsession.add(Medical_Staff(
            uid=uuid4(),
            name="admin",
            ms_id="admin",
            pwd=generate_password_hash("admin"),
            permissions=0
        ))
        dbsession.commit()
    app.run(debug=True)
