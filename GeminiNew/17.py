








import os
from flask import Flask, request, render_template_string, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)



app.config['SECRET_KEY'] = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digital_ledger.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)




limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


class LedgerEntry(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    visitor_action = db.Column(db.String(100), nullable=False)
    
    page_location = db.Column(db.String(200), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/record_action', methods=['POST'])
@limiter.limit("10 per minute") 
def record_action():
    
    action = request.form.get('action')
    page = request.form.get('page')

    
    if action and page:
        
        
        new_entry = LedgerEntry(
            visitor_action=str(action)[:100], 
            page_location=str(page)[:200]
        )
        db.session.add(new_entry)
        db.session.commit()
        return "Entry Recorded", 200
    
    return "Invalid Data", 400


@app.route('/view_ledger')
def view_ledger():
    
    
    all_rows = LedgerEntry.query.order_by(LedgerEntry.time_stamp.desc()).all()
    
    
    html_layout = 
    return render_template_string(html_layout, rows=all_rows)

if __name__ == '__main__':
    
    
    app.run(debug=False)