from app import create_app
from app.auth.user import User

app = create_app()

@app.login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

if __name__ == '__main__':
    app.run(debug=True)
