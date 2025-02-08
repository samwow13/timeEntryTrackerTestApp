import json
from flask_login import UserMixin

class User(UserMixin):
    """
    User class for managing user authentication and data
    Inherits from UserMixin for Flask-Login functionality
    """
    
    def __init__(self, id, username, password_hash):
        """
        Initialize a new User instance
        
        Args:
            id (str): Unique user identifier
            username (str): User's username
            password_hash (str): Hashed password
        """
        self.id = id
        self.username = username
        self.password_hash = password_hash
    
    @staticmethod
    def get(user_id):
        """
        Retrieve a user from the JSON storage by their ID
        
        Args:
            user_id (str): The user's unique identifier
            
        Returns:
            User: User object if found, None otherwise
        """
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
                if user_id in users:
                    user_data = users[user_id]
                    return User(
                        id=user_id,
                        username=user_data['username'],
                        password_hash=user_data['password_hash']
                    )
        except FileNotFoundError:
            return None
        return None
    
    @staticmethod
    def get_by_username(username):
        """
        Retrieve a user from the JSON storage by their username
        
        Args:
            username (str): The username to search for
            
        Returns:
            User: User object if found, None otherwise
        """
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
                for user_id, user_data in users.items():
                    if user_data['username'] == username:
                        return User(
                            id=user_id,
                            username=user_data['username'],
                            password_hash=user_data['password_hash']
                        )
        except FileNotFoundError:
            return None
        return None
