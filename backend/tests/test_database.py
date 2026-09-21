from sqlalchemy import select
from config.database import SessionLocal
from models.order import Order


with SessionLocal() as session:

    statement = select(Order)

    orders = session.scalars(statement).all()

    for order in orders:

        print(
            order.order_id,
            order.status,
            order.product
        )



#  without ORM
# from sqlalchemy import text

# from config.database import engine


# with engine.connect() as connection:

#     result = connection.execute(
#         text("SELECT order_id, status, product FROM orders")
#     )

#     for row in result:
#         print(row)