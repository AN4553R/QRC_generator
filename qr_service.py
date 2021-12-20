from app import create_app
from app import db
from app.models import User

app = create_app()
app.app_context().push()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


if __name__ == "__main__":
    db.create_all(app=app)
    app.run(port=3000, debug=True)
