from sqlalchemy import select, text
from sqlalchemy.sql.functions import func

from db.repositories.base import AbstractRepository
from models import Dish, Menu, Submenu


class DataRepository(AbstractRepository):
    async def dump_data(self) -> dict:
        json_dishes_subquery = (
            select(
                Dish.submenu_id,
                func.json_agg(
                    func.json_build_object(
                        "dish",
                        func.json_build_object(
                            "title",
                            Dish.title,
                            "description",
                            Dish.description,
                            "price",
                            Dish.price,
                        ),
                    )
                ).label("dishes"),
            )
            .group_by(Dish.submenu_id)
            .subquery()
        )

        json_submenus_subquery = (
            select(
                Submenu.menu_id,
                func.json_agg(
                    func.json_build_object(
                        "submenu",
                        func.json_build_object(
                            "title",
                            Submenu.title,
                            "description",
                            Submenu.description,
                        ),
                        "dishes",
                        func.coalesce(
                            json_dishes_subquery.c.dishes, text("'[]'::json")
                        ),
                    )
                ).label("submenus"),
            )
            .join(
                json_dishes_subquery,
                Submenu.id == json_dishes_subquery.c.submenu_id,
                isouter=True,
            )
            .group_by(Submenu.menu_id)
            .subquery()
        )

        json_menus_subquery = select(
            func.json_agg(
                func.json_build_object(
                    "menu",
                    func.json_build_object(
                        "title",
                        Menu.title,
                        "description",
                        Menu.description,
                    ),
                    "submenus",
                    func.coalesce(
                        json_submenus_subquery.c.submenus, text("'[]'::json")
                    ),
                )
            ).label("menus")
        ).join(
            json_submenus_subquery,
            Menu.id == json_submenus_subquery.c.menu_id,
            isouter=True,
        )
        results = await self.session.execute(json_menus_subquery)
        response = dict(results.one())
        return response
