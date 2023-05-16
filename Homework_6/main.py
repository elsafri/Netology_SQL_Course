import json

import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Shop, Stock, Sale


DSN = 'postgresql://postgres:postgres@localhost:5432/bookstore'
engine = sq.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)


def add_data(data, **models):
    for info in data:
        model = models[info.get('model')]
        session.add(model(id=info.get('pk'), **info.get('fields')))
        session.commit()


def get_publisher_info(publisher):
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
        select_from(Shop).\
        join(Stock, Shop.id == Stock.id_shop).\
        join(Book, Stock.id_book == Book.id).\
        join(Publisher, Book.id_publisher == Publisher.id).\
        join(Sale, Stock.id == Sale.id_stock)
    if publisher.isdigit():
        query = query.filter(Publisher.id == publisher).all()

    else:
        query = query.filter(Publisher.name == publisher)
    for book_title, shop_name, sale_price, sale_date in query:
        print(f"{book_title: <40} | {shop_name: <10} | {sale_price: <8} | {sale_date.strftime('%d-%m-%Y')}")

session.close()


if __name__ == '__main__':
     add_data(data, publisher=Publisher, shop=Shop, book=Book, stock=Stock, sale=Sale)
    get_publisher_info(input(f'Введите имя или id издателя: '))
