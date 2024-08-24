from sqlalchemy.orm import joinedload
from sqlalchemy import func, case
from models import Restaurant, Review
from database import db_session
from typing import List

class RestaurantRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    async def get_restaurants_async(self) -> List[Restaurant]:
        subquery = (
            self.db_session.query(
                Review.restaurant_id,
                func.coalesce(func.avg(Review.rating), 0).label('rating')
            )
            .group_by(Review.restaurant_id)
            .subquery()
        )

        query = (
            self.db_session.query(Restaurant)
            .outerjoin(subquery, Restaurant.id == subquery.c.restaurant_id)
            .options(joinedload(Restaurant.reviews))
            .with_entities(
                Restaurant.id,
                Restaurant.name,
                Restaurant.address,
                Restaurant.description,
                func.coalesce(subquery.c.rating, 0).label('rating')
            )
            .all()
        )

        return query

    async def get_restaurants_with_rating_async(self, rating: int) -> List[Restaurant]:
        query = (
            self.db_session.query(Restaurant)
            .join(Review)
            .filter(Review.rating == rating)
            .distinct()
            .all()
        )

        return query

    async def get_restaurants_for_user_async(self, user_id: str) -> List[Restaurant]:
        subquery = (
            self.db_session.query(
                Review.restaurant_id,
                func.coalesce(func.avg(Review.rating), 0).label('rating')
            )
            .group_by(Review.restaurant_id)
            .subquery()
        )

        query = (
            self.db_session.query(Restaurant)
            .filter(Restaurant.user_id == user_id)
            .outerjoin(subquery, Restaurant.id == subquery.c.restaurant_id)
            .options(joinedload(Restaurant.reviews))
            .with_entities(
                Restaurant.id,
                Restaurant.name,
                Restaurant.address,
                Restaurant.description,
                func.coalesce(subquery.c.rating, 0).label('rating')
            )
            .all()
        )

        return query

    async def get_restaurant_with_name(self, name: str) -> Restaurant:
        restaurant = (
            self.db_session.query(Restaurant)
            .filter(Restaurant.name == name)
            .first()
        )

        return restaurant
