from sampl import app, db
from flask import request, abort

def main(port=5000, debug=False, host="127.0.0.1"):
    with app.app_context():
        db.create_all()
    app.run(port=port, debug=debug, host=host)

if __name__ == '__main__':
    main(port=8080, debug=True, host="0.0.0.0")
