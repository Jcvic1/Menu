import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.database import Base, engine
from app.main import app

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine)

# Drop all existing tables before each test
Base.metadata.drop_all(bind=engine)

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


# SUBMENU CRUD

menu_data = {'title': 'Sample Menu 1', 'description': 'Menu Description 1'}

submenu_data = {'title': 'Sample SubMenu 1',
                'description': 'SubMenu Description 1'}

submenu_datas = [
    {'title': 'Sample SubMenu 1',
     'description': 'SubMenu Description 1'
     },
    {'title': 'Sample SubMenu 2',
     'description': 'SubMenu Description 2'
     },
    {'title': 'Sample SubMenu 3',
     'description': 'SubMenu Description 3'
     },
    {'title': 'Sample SubMenu 4',
     'description': 'SubMenu Description 4'
     },
    {'title': 'Sample SubMenu 5',
     'description': 'SubMenu Description 5'
     },
]

update_submenu_datas = [
    {'title': 'Sample SubMenu Update 1',
     'description': 'SubMenu Description Update 1'
     },
    {'title': 'Sample SubMenu Update 2',
     'description': 'SubMenu Description Update 2'
     },
    {'title': 'Sample SubMenu Update 3',
     'description': 'SubMenu Description Update 3'
     },
    {'title': 'Sample SubMenu 4',
     'description': 'SubMenu Description 4'
     },
    {'title': 'Sample SubMenu 5',
     'description': 'SubMenu Description 5'
     },
]


def get_menu_id():
    response = client.get(app.url_path_for('get_menus'))
    assert response.status_code == 200
    menu_list = response.json()
    return menu_list[0]['id']


def test_create_submenu():
    response = client.post(app.url_path_for('post_menu'), json=menu_data)
    assert response.status_code == 201
    assert response.json()['title'] == menu_data['title']
    assert 'id' in response.json()

    menu_id = get_menu_id()

    response = client.post(
        app.url_path_for('post_submenu', menu_id=menu_id), json=submenu_data
    )
    assert response.status_code == 201
    assert response.json()['title'] == submenu_data['title']
    assert 'id' in response.json()

    response = client.get(app.url_path_for('get_submenus', menu_id=menu_id))
    assert response.status_code == 200
    submenu_list = response.json()
    submenu_id = submenu_list[0]['id']

    response = client.delete(
        app.url_path_for('delete_submenu', menu_id=menu_id, submenu_id=submenu_id)
    )
    assert response.status_code == 200


def test_read_submenus():
    menu_id = get_menu_id()

    for submenu_data in submenu_datas:
        response = client.post(
            app.url_path_for('post_submenu', menu_id=menu_id), json=submenu_data
        )
        assert response.status_code == 201
        assert 'id' in response.json()

    response = client.get(app.url_path_for('get_submenus', menu_id=menu_id))
    assert response.status_code == 200
    submenu_list = response.json()
    assert isinstance(submenu_list, list)

    titles = [submenu['title'] for submenu in submenu_list]
    expected_titles = [submenu_data['title'] for submenu_data in submenu_datas]
    assert titles == expected_titles

    for submenu in submenu_list:
        response = client.delete(
            app.url_path_for('delete_submenu', menu_id=menu_id, submenu_id=submenu['id'])
        )
        assert response.status_code == 200


def test_read_submenu():
    menu_id = get_menu_id()

    response = client.post(
        app.url_path_for('post_submenu', menu_id=menu_id), json=submenu_data
    )
    assert response.status_code == 201
    assert response.json()['title'] == submenu_data['title']
    assert 'id' in response.json()

    response = client.get(app.url_path_for('get_submenus', menu_id=menu_id))
    assert response.status_code == 200
    submenu_list = response.json()

    submenu_id = submenu_list[0]['id']
    title = submenu_list[0]['title']

    response = client.get(
        app.url_path_for('get_submenu', menu_id=menu_id, submenu_id=submenu_id)
    )
    assert response.status_code == 200
    assert response.json()['title'] == title

    response = client.delete(
        app.url_path_for('delete_submenu', menu_id=menu_id, submenu_id=submenu_id)
    )


def test_update_submenu():
    menu_id = get_menu_id()

    for update_submenu_data in update_submenu_datas:
        response = client.post(
            app.url_path_for('post_submenu', menu_id=menu_id), json=update_submenu_data
        )
        assert response.status_code == 201
        assert 'id' in response.json()

    response = client.get(app.url_path_for('get_submenus', menu_id=menu_id))
    assert response.status_code == 200
    submenu_list = response.json()
    assert isinstance(submenu_list, list)

    titles = [submenu['title'] for submenu in submenu_list]
    expected_titles = [
        update_submenu_data['title'] for update_submenu_data in update_submenu_datas
    ]
    assert titles == expected_titles

    for submenu in submenu_list:
        response = client.delete(
            app.url_path_for('delete_submenu', menu_id=menu_id, submenu_id=submenu['id'])
        )
        assert response.status_code == 200


def test_delete_submenu():
    menu_id = get_menu_id()

    response = client.post(
        app.url_path_for('post_submenu', menu_id=menu_id), json=submenu_data
    )
    assert response.status_code == 201
    assert response.json()['title'] == submenu_data['title']
    assert 'id' in response.json()

    response = client.get(app.url_path_for('get_submenus', menu_id=menu_id))
    assert response.status_code == 200
    submenu_list = response.json()

    submenu_id = submenu_list[0]['id']

    response = client.delete(
        app.url_path_for('delete_submenu', menu_id=menu_id, submenu_id=submenu_id)
    )
    assert response.status_code == 200

    response = client.get(
        app.url_path_for('get_submenu', menu_id=menu_id, submenu_id=submenu_id)
    )
    assert response.status_code == 404

    response = client.delete(app.url_path_for('delete_menu', menu_id=menu_id))
    assert response.status_code == 200

    response = client.get(app.url_path_for('get_menu', menu_id=menu_id))
    assert response.status_code == 404
