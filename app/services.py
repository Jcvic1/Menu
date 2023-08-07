from fastapi import Depends
from sqlalchemy.orm import Session

from app import schemas
from app.crud import DishCRUD, MenuCRUD
from app.database import get_db
from app.models import Dish, Menu


class Notification:
    def send(self, notification):
        pass


class Discount:
    def discount_price(self, price):
        discount = 0.1
        return 1 - (discount * price)


class MenuService:
    def __init__(self, menu_crud: MenuCRUD = Depends(), dish_crud: DishCRUD = Depends()):
        self.menu_crud = menu_crud
        self.dish_crud = dish_crud
        self.notification = Notification()
        self.discount = Discount()

    def create_menu(
        self, item_schema: schemas.MenuCreate, db: Session = Depends(get_db)
    ) -> Menu:
        menu = self.menu_crud.create_item(
            db=db, item_schema=item_schema
        )

        return self.notification.send(menu)

    def get_dishes(
        self, menu_id: int, submenu_id: int, dish_id: int,
        db: Session = Depends(get_db)
    ) -> Dish:
        dish = self.dish_crud.read_item(
            db=db, submenu_id=submenu_id, menu_id=menu_id, dish_id=dish_id
        )

        return self.discount.discount_price(dish['price'])
