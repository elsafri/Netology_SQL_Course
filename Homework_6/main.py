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
    if publisher.isdigit():
         query = session.query(Publisher, Book, Stock, Shop, Sale).\
             join(Book, Publisher.id == Book.id_publisher).\
             join(Stock, Book.id == Stock.id_book).\
             join(Shop, Stock.id_shop == Shop.id).\
             join(Sale, Stock.id == Sale.id_stock).\
             filter(Publisher.id == publisher).all()
         if query:
             for publisher, book, stock, shop, sale in query:
                 print(f'{book.title}|{shop.name}|{sale.price}|{sale.date_sale}')
         else:
             print(f'Издателя ({publisher}) нет в базе данных')
    else:
        query = session.query(Publisher, Book, Stock, Shop, Sale).\
            join(Book, Publisher.id == Book.id_publisher).\
            join(Stock, Book.id == Stock.id_book).\
            join(Shop, Stock.id_shop == Shop.id).\
            join(Sale, Stock.id == Sale.id_stock).\
            filter(Publisher.name == publisher).all()
        if query:
            for publisher, book, stock, shop, sale in query:
                print(f'{book.title}|{shop.name}|{sale.price}|{sale.date_sale}')
        else:
            print(f'Издателя ({publisher}) нет в базе данных')
session.close()


if __name__ == '__main__':
    add_data(data, publisher=Publisher, shop=Shop, book=Book, stock=Stock, sale=Sale)
    get_publisher_info(input(f'Введите имя или id издателя: '))
