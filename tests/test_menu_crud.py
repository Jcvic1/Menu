import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.database import Base, engine
from app.main import app

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine)

Base.metadata.create_all(bind=engine)


# Use a pytest fixture to create a clean database for each test
@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)

prefix = 'api/v1'


# MENU CRUD


menu_data = {'title': 'Sample Menu 1', 'description': 'Menu Description 1'}

menu_datas = [
    {'title': 'Sample Menu 1', 'description': 'Menu Description 1'},
    {'title': 'Sample Menu 2', 'description': 'Menu Description 2'},
    {'title': 'Sample Menu 3', 'description': 'Menu Description 3'},
    {'title': 'Sample Menu 4', 'description': 'Menu Description 4'},
    {'title': 'Sample Menu 5', 'description': 'Menu Description 5'},
]

update_menu_datas = [
    {'title': 'Sample Menu Update 1',
     'description': 'Menu Description Update 1'
     },
    {'title': 'Sample Menu Update 2',
     'description': 'Menu Description Update 2'
     },
    {'title': 'Sample Menu Update 3',
     'description': 'Menu Description Update 3'
     },
    {'title': 'Sample Menu 4',
     'description': 'Menu Description 4'
     },
    {'title': 'Sample Menu 5',
     'description': 'Menu Description 5'
     },
]


# def get_menu_id():
#     response = client.get(f'{prefix}/menus/')
#     assert response.status_code == 200
#     menu_list = response.json()

#     return menu_list[0]['id']


# def test_create_menu():
#     response = client.post(f'{prefix}/menus/', json=menu_data)
#     assert response.status_code == 201
#     assert response.json()['title'] == menu_data['title']
#     assert 'id' in response.json()

#     menu_id = get_menu_id()

#     response = client.delete(f'{prefix}/menus/{menu_id}')


# def test_read_menus():
#     for menu_data in menu_datas:
#         response = client.post(f'{prefix}/menus/', json=menu_data)
#         assert response.status_code == 201
#         assert 'id' in response.json()

#     response = client.get(f'{prefix}/menus/')
#     assert response.status_code == 200
#     menu_list = response.json()
#     assert isinstance(menu_list, list)

#     titles = [menu['title'] for menu in menu_list]

#     expected_titles = [menu_data['title'] for menu_data in menu_datas]
#     assert titles == expected_titles

#     for menu in menu_list:
#         response = client.delete(f"{prefix}/menus/{menu['id']}")


# def test_read_menu():
#     response = client.post(f'{prefix}/menus/', json=menu_data)
#     assert response.status_code == 201
#     assert response.json()['title'] == menu_data['title']
#     assert 'id' in response.json()

#     response = client.get(f'{prefix}/menus/')
#     assert response.status_code == 200
#     menu_list = response.json()
#     menu_id = menu_list[0]['id']
#     title = menu_list[0]['title']

#     response = client.get(f'{prefix}/menus/{menu_id}')
#     assert response.status_code == 200
#     assert response.json()['title'] == title

#     response = client.delete(f'{prefix}/menus/{menu_id}')


# def test_update_menu():
#     for update_menu_data in update_menu_datas:
#         response = client.post(f'{prefix}/menus/', json=update_menu_data)
#         assert response.status_code == 201
#         assert 'id' in response.json()

#     response = client.get(f'{prefix}/menus/')
#     assert response.status_code == 200
#     menu_list = response.json()
#     assert isinstance(menu_list, list)

#     titles = [menu['title'] for menu in menu_list]

#     expected_titles = [
#         update_menu_data['title'] for update_menu_data in update_menu_datas
#     ]
#     assert titles == expected_titles

#     for menu in menu_list:
#         response = client.delete(f"{prefix}/menus/{menu['id']}")


# def test_delete_menu():
#     response = client.post(f'{prefix}/menus/', json=menu_data)
#     assert response.status_code == 201
#     assert response.json()['title'] == menu_data['title']
#     assert 'id' in response.json()

#     menu_id = get_menu_id()

#     response = client.delete(f'{prefix}/menus/{menu_id}')

#     response = client.get(f'{prefix}/menus/{menu_id}')
#     assert response.status_code == 404


def get_menu_id():
    response = client.get(app.url_path_for('get_menus'))
    assert response.status_code == 200
    menu_list = response.json()
    return menu_list[0]['id']


def test_create_menu():
    response = client.post(app.url_path_for('post_menu'), json=menu_data)
    assert response.status_code == 201
    assert response.json()['title'] == menu_data['title']
    assert 'id' in response.json()
    menu_id = response.json()['id']

    response = client.delete(app.url_path_for('delete_menu', menu_id=menu_id))
    assert response.status_code == 200


def test_read_menus():
    for menu_data in menu_datas:
        response = client.post(app.url_path_for('post_menu'), json=menu_data)
        assert response.status_code == 201
        assert 'id' in response.json()

    response = client.get(app.url_path_for('get_menus'))
    assert response.status_code == 200
    menu_list = response.json()
    assert isinstance(menu_list, list)

    titles = [menu['title'] for menu in menu_list]
    expected_titles = [menu_data['title'] for menu_data in menu_datas]
    assert titles == expected_titles

    for menu in menu_list:
        response = client.delete(app.url_path_for('delete_menu', menu_id=menu['id']))
        assert response.status_code == 200


def test_read_menu():
    response = client.post(app.url_path_for('post_menu'), json=menu_data)
    assert response.status_code == 201
    assert response.json()['title'] == menu_data['title']
    assert 'id' in response.json()

    response = client.get(app.url_path_for('get_menus'))
    assert response.status_code == 200
    menu_list = response.json()
    menu_id = menu_list[0]['id']
    title = menu_list[0]['title']

    response = client.get(app.url_path_for('get_menu', menu_id=menu_id))
    assert response.status_code == 200
    assert response.json()['title'] == title

    response = client.delete(app.url_path_for('delete_menu', menu_id=menu_id))
    assert response.status_code == 200


def test_update_menu():
    for update_menu_data in update_menu_datas:
        response = client.post(app.url_path_for('post_menu'), json=update_menu_data)
        assert response.status_code == 201
        assert 'id' in response.json()

    response = client.get(app.url_path_for('get_menus'))
    assert response.status_code == 200
    menu_list = response.json()
    assert isinstance(menu_list, list)

    titles = [menu['title'] for menu in menu_list]
    expected_titles = [
        update_menu_data['title'] for update_menu_data in update_menu_datas
    ]
    assert titles == expected_titles

    for menu in menu_list:
        response = client.delete(app.url_path_for('delete_menu', menu_id=menu['id']))
        assert response.status_code == 200


def test_delete_menu():
    response = client.post(app.url_path_for('post_menu'), json=menu_data)
    assert response.status_code == 201
    assert response.json()['title'] == menu_data['title']
    assert 'id' in response.json()

    menu_id = get_menu_id()

    response = client.delete(app.url_path_for('delete_menu', menu_id=menu_id))
    assert response.status_code == 200

    response = client.get(app.url_path_for('get_menu', menu_id=menu_id))
    assert response.status_code == 404
