import pytest
from app import create_app
from modules import db
from modules.event_categories import EventCategories
from modules.event_images import EventImages
from modules.events import Events
from modules.feedback import Feedback
from modules.registrations import Registrations
from modules.users import Users
from modules.repository import Repository

@pytest.fixture
def test_app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
        
@pytest.fixture
def client(test_app):
    return test_app.test_client()

@pytest.fixture
def database_session(test_app):
    with test_app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()
        
@pytest.fixture
def repository(test_app):
    with test_app.app_context():
        yield Repository(Users)


def test_repository_get_by_id(database_session,repository):
    # Arrange
    user_data = {
        'Username': 'test_user',
        'PasswordHash': 'test_password',
        'Email': 'test@example.com',
        'FullName': 'aa'
    }
    user = Users(**user_data)
    database_session.add(user)
    database_session.commit()

    # Act
    result = repository.get_by_id(user.UserID)

    # Assert
    assert result == user


def test_repository_get_all(database_session,repository):
    # Arrange
    users_data = [
        {'Username': 'user1', 'PasswordHash': 'pass1', 'Email': 'user1@example.com', 'FullName': 'aa'},
        {'Username': 'user2', 'PasswordHash': 'pass2', 'Email': 'user2@example.com', 'FullName': 'bb'}
    ]
    users = [Users(**data) for data in users_data]
    database_session.add_all(users)
    database_session.commit()

    # Act
    result = repository.get_all()

    # Assert
    assert result == users
    

def test_repository_add(repository):
    # Arrange
    user_data = {'Username': 'test_user', 'PasswordHash': 'test_password', 'Email': 'test@example.com', 'FullName': 'aa'}
    user = Users(**user_data)

    # Act
    result = repository.add(user)

    # Assert
    assert result is True
    assert Users.query.filter_by(Username='test_user').first() == user


def test_repository_update(repository):
    # Arrange
    user_data = {'Username': 'test_user', 'PasswordHash': 'test_password', 'Email': 'test@example.com', 'FullName': 'bb'}
    user = Users(**user_data)
    repository.add(user)

    updated_data = {'Username': 'updated_user'}

    # Act
    result = repository.update(user.UserID, updated_data)

    # Assert
    assert result is True
    assert Users.query.get(user.UserID).Username == 'updated_user'


def test_repository_remove(repository):
    # Arrange
    user_data = {'Username': 'test_user', 'PasswordHash': 'test_password', 'Email': 'test@example.com', 'FullName': 'bb'}
    user = Users(**user_data)
    repository.add(user)

    # Act
    result = repository.remove(user.UserID)

    # Assert
    assert result is True
    assert Users.query.get(user.UserID) is None