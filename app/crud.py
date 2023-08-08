from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Dish, Menu, SubMenu
from app.validation import is_valid_dish, is_valid_menu, is_valid_submenu


class MenuCRUD:
    def create_item(
        self,
        db: Session,
        item_schema: Menu,
    ) -> Menu:
        db_item = Menu(**item_schema.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def read_item(
        self,
        db: Session,
        menu_id: int,
    ) -> Menu:
        valid_menu = is_valid_menu(db=db, menu_id=menu_id)
        if valid_menu:
            return valid_menu
        raise HTTPException(status_code=404, detail='menu not found')

    def read_items(
        self,
        db: Session,
        limit: int = 20,
        page: int = 1,
        search: str = '',
    ) -> List[Menu]:
        skip = (page - 1) * limit

        return (
            db.query(Menu)
            .filter(Menu.title.contains(search))
            .limit(limit)
            .offset(skip)
            .all()
        )

    def update_item(
        self, db: Session, item_schema: Menu, item_id: int, menu_id: int
    ) -> Menu:
        valid_menu = is_valid_menu(db=db, menu_id=menu_id)
        if valid_menu:
            update_data = item_schema.dict(exclude_unset=True)
            item_query = db.query(Menu).filter(Menu.id == menu_id)
            item_query.filter(Menu.id == item_id).update(
                update_data, synchronize_session=False
            )

            db.commit()
            db.refresh(valid_menu)
            return valid_menu
        raise HTTPException(status_code=404, detail='menu not found')

    def delete_item(
        self,
        db: Session,
        item_id: int,
        menu_id: int,
    ) -> None:
        valid_menu = is_valid_menu(db=db, menu_id=menu_id)
        if valid_menu:
            db.query(Menu).filter(Menu.id == item_id).delete(synchronize_session=False)

        db.commit()


class SubmenuCRUD:
    def create_item(
        self,
        db: Session,
        item_schema: SubMenu,
        menu_id: int,
    ) -> SubMenu:
        valid_menu = is_valid_menu(db=db, menu_id=menu_id)
        if valid_menu:
            db_item = SubMenu(**item_schema.dict(), menu_id=menu_id)
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return db_item
        raise HTTPException(status_code=404, detail='menu not found')

    def read_item(self, db: Session, menu_id: int, submenu_id: int) -> SubMenu:
        valid_submenu = is_valid_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
        if valid_submenu:
            return valid_submenu
        raise HTTPException(status_code=404, detail='submenu not found')

    def read_items(
        self,
        db: Session,
        limit: int = 20,
        page: int = 1,
        search: str = '',
    ) -> List[SubMenu]:
        skip = (page - 1) * limit

        return (
            db.query(SubMenu)
            .filter(SubMenu.title.contains(search))
            .limit(limit)
            .offset(skip)
            .all()
        )

    def update_item(
        self,
        db: Session,
        item_schema: SubMenu,
        item_id: int,
        menu_id: int,
        submenu_id: int,
    ) -> SubMenu:
        valid_submenu = is_valid_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
        if valid_submenu:
            update_data = item_schema.dict(exclude_unset=True)
            item_query = db.query(SubMenu).filter(SubMenu.id == submenu_id)
            item_query.filter(SubMenu.id == item_id).update(
                update_data, synchronize_session=False
            )

            db.commit()
            db.refresh(valid_submenu)
            return valid_submenu
        raise HTTPException(status_code=404, detail='submenu not found')

    def delete_item(
        self, db: Session, item_id: int, menu_id: int, submenu_id: int
    ) -> None:
        valid_submenu = is_valid_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
        if valid_submenu:
            db.query(SubMenu).filter(SubMenu.id == item_id).delete(
                synchronize_session=False
            )
            db.commit()


class DishCRUD:
    def create_item(
        self, db: Session, item_schema: Dish, menu_id: int, submenu_id: int
    ) -> Dish:
        if is_valid_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id):
            db_item = Dish(**item_schema.dict(), submenu_id=submenu_id)

            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return db_item
        raise HTTPException(status_code=404, detail='submenu not found')

    def read_item(
        self, db: Session, menu_id: int, submenu_id: int, dish_id: int
    ) -> Dish:
        valid_dish = is_valid_dish(
            db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
        )
        if valid_dish:
            return valid_dish
        raise HTTPException(status_code=404, detail='dish not found')

    # For current test

    def read_items(
        self,
        db: Session,
        limit: int = 20,
        page: int = 1,
        search: str = '',
    ) -> List[Dish]:
        skip = (page - 1) * limit
        return (
            db.query(Dish)
            .filter(Dish.title.contains(search))
            .limit(limit)
            .offset(skip)
            .all()
        )

    def update_item(
        self,
        db: Session,
        item_schema: Dish,
        item_id: int,
        menu_id: int,
        submenu_id: int,
        dish_id: int,
    ) -> Dish:
        valid_dish = is_valid_dish(
            db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
        )
        if valid_dish:
            update_data = item_schema.dict(exclude_unset=True)
            item_query = db.query(Dish).filter(Dish.id == dish_id)
            item_query.filter(Dish.id == item_id).update(
                update_data, synchronize_session=False
            )

            db.commit()
            db.refresh(valid_dish)
            return valid_dish
        raise HTTPException(status_code=404, detail='dish not found')

    def delete_item(
        self,
        db: Session,
        item_id: int,
        menu_id: int,
        submenu_id: int,
        dish_id: int,
    ) -> None:
        valid_dish = is_valid_dish(
            db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        if valid_dish:
            db.query(Dish).filter(Dish.id == item_id).delete(synchronize_session=False)

            db.commit()
