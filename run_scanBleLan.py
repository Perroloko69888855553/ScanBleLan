from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import json, os
import scanner_ble

app = Flask(__name__)
Bootstrap(app)


json_file = json.load(open(os.path.dirname(__file__) + "/config/conf.json", 'r'))
db_data = json_file["db_data"][0]

scanner_ble.escaneoBLE()
# change to name of your database; add path if necessary
#db_name = 'sockmarket.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + db_data["user"] + ':' + db_data["pass"] + '@' + db_data["host"] + "/" + db_data["db_name"]

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)


# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and data type
class Device(db.Model):
    __tablename__ = 'devices'
    address = db.Column(db.String(255), primary_key=True, nullable = False)
    name = db.Column(db.String(255), nullable = True)
    description = db.Column(db.String(255), nullable = True)
    date_scan = db.Column(db.DateTime, nullable = False)

# NOTHING BELOW THIS LINE NEEDS TO CHANGE
# this route will test the database connection and nothing more

@app.route('/')
def index():
    # get a list of unique values in the style column
    devices = Device.query.filter().all()
    return render_template('index.html', devices=devices)

#@app.route('/')
#def index():
    #try:
     #   devices = Device.query.filter().all()
      #  return render_template('index.html', devices = devices )
    #except Exception as e:
        # e holds description of the error
     #   error_text = "<p>The error:<br>" + str(e) + "</p>"
      #  hed = '<h1>Something is broken.</h1>'
       # return hed + error_text

if __name__ == '__main__':
      app.run(debug=True)