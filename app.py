from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from werkzeug.security import generate_password_hash

from configs import SQL_Server
from models import Medical_Staff

from apis.web import web_bp
from apis.mobile import mobile_bp

engine = create_engine(SQL_Server)
Session = sessionmaker(bind=engine)
dbsession = Session()

app = Flask(__name__, static_folder='static')
app.config.from_pyfile('./configs.py')

app.register_blueprint(web_bp, url_prefix='/web')
app.register_blueprint(mobile_bp)

@app.route('/')
def home():
    sql = text('select * from Medical_Staff')
    row = dbsession.execute(sql).fetchall()
    print(row)
    return "OK"

if __name__ == '__main__':
    row = dbsession.query(Medical_Staff).filter(Medical_Staff.ms_id=="admin").all()
    if not row:
        dbsession.add(Medical_Staff(
            uid=uuid4(),
            name="admin",
            ms_id="admin",
            pwd=generate_password_hash("admin"),
            permissions=0
        ))
        dbsession.commit()
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('server.crt', 'server.key'))
