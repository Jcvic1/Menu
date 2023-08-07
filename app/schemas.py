from typing import List
from pydantic import BaseModel

# Dish Schema


class DishBase(BaseModel):
    title: str
    description: str
    price: str


class DishCreate(DishBase):
    pass


class DishUpdate(DishBase):
    pass


class Dish(DishBase):
    id: str
    submenu_id: str

    class Config:
        orm_mode = True


# SubMenu Schema


class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuCreate(SubMenuBase):
    pass


class SubMenuUpdate(SubMenuBase):
    pass


class SubMenu(SubMenuBase):
    id: str
    menu_id: str
    dishes: List[Dish] = []  # type: ignore

    class Config:
        orm_mode = True


class SubMenuReponse(SubMenu):
    dishes_count: int


# Menu Schema


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


class Menu(MenuBase):
    id: str
    submenus: List[SubMenu] = []  # type: ignore

    class Config:
        orm_mode = True


class MenuReponse(Menu):
    submenus_count: int
    dishes_count: int
