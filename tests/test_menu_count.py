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

menu_data = {'title': 'Sample Menu 1', 'description': 'Menu Description 1'}

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


dish_datas = [
    {
        'title': 'Sample Dish 1',
        'description': 'Dish Description 1',
        'price': '1.50',
    },
    {
        'title': 'Sample Dish 2',
        'description': 'Dish Description 2',
        'price': '2.50',
    },
    {
        'title': 'Sample Dish 3',
        'description': 'Dish Description 3',
        'price': '3.50',
    },
    {
        'title': 'Sample Dish 4',
        'description': 'Dish Description 4',
        'price': '4.50',
    },
    {
        'title': 'Sample Dish 5',
        'description': 'Dish Description 5',
        'price': '5.50',
    },
]


def get_menu_id():
    response = client.get(app.url_path_for("get_menus"))
    assert response.status_code == 200
    menu_list = response.json()
    return menu_list[0]['id']


def get_submenu_id():
    menu_id = get_menu_id()
    response = client.get(app.url_path_for("get_submenus", menu_id=menu_id))
    assert response.status_code == 200
    submenu_list = response.json()
    return submenu_list[3]['id']


def test_count_submenus():
    response = client.post(app.url_path_for("post_menu"), json=menu_data)
    assert response.status_code == 201
    assert response.json()['title'] == menu_data['title']
    assert 'id' in response.json()

    menu_id = get_menu_id()

    for submenu_data in submenu_datas:
        response = client.post(app.url_path_for("post_submenu", menu_id=menu_id), json=submenu_data)
        assert response.status_code == 201
        assert response.json()['title'] == submenu_data['title']
        assert 'id' in response.json()

    response = client.get(app.url_path_for("get_menu", menu_id=menu_id))
    assert response.status_code == 200

    menu = response.json()

    submenu_count = len(menu['submenus'])

    assert submenu_count == len(submenu_datas)


def test_count_dishes():
    menu_id = get_menu_id()
    submenu_id = get_submenu_id()

    for dish_data in dish_datas:
        response = client.post(app.url_path_for("post_dish", menu_id=menu_id, submenu_id=submenu_id), json=dish_data)
        assert response.status_code == 201
        assert response.json()['title'] == dish_data['title']
        assert 'id' in response.json()

    response = client.get(app.url_path_for("get_menu", menu_id=menu_id))
    assert response.status_code == 200

    menu = response.json()

    dish_count = sum(len(submenu['dishes']) for submenu in menu['submenus'])

    assert dish_count == len(dish_datas)

    response = client.delete(app.url_path_for("delete_menu", menu_id=menu_id))
    assert response.status_code == 200
