from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Dish, Menu, SubMenu

# validate menu


def is_valid_menu(db: Session, menu_id: int):
    return db.query(Menu).filter(Menu.id == menu_id).first()


# validate submenu


def is_valid_submenu(
    db: Session, menu_id: int, submenu_id: int
):
    item_query = db.query(Menu).filter(Menu.id == menu_id).first()
    if not item_query:
        raise HTTPException(status_code=404, detail='menu not found')
    else:
        return db.query(SubMenu).filter(SubMenu.id == submenu_id).first()


# validate dish


def is_valid_dish(
    db: Session,
    menu_id: int,
    submenu_id: int,
    dish_id: int
):
    item_query = db.query(Menu).filter(Menu.id == menu_id).first()
    if not item_query:
        raise HTTPException(status_code=404, detail='menu not found')
    else:
        item_query = db.query(SubMenu).filter(SubMenu.id == submenu_id).first()
        if not item_query:
            raise HTTPException(status_code=404, detail='submenu not found')

        else:
            return db.query(Dish).filter(Dish.id == dish_id).first()
