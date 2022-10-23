from ast import Delete
from typing import List
from scheme import Goods, Positions, Orders
from run import session
from datetime import datetime

import logging
import os.path
from time import sleep
from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime as dt

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials_service.json')
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)


def parse_goods(rows) -> List[Goods]:
    goods = []
    for row in rows:
        if not row:
            continue
        try:
            good = Goods()
            good.owner = row[0]
            good.brand = row[1]
            good.category = row[2]
            good.article = row[5]
            good.sku = int(row[6])
            good.price = float(row[9].strip('₽').replace(' ', '').replace('\xa0', ''))
            good.price_after_spp = float(row[9].strip('₽').replace('\xa0', ''))
            good.created_at = datetime.now()
            good.updated_at = datetime.now()
            goods.append(good)
        except Exception as e:
            logging.error(e)
    return goods


def update_goods(goods: List[Goods]):
    for good in goods:
        if session.query(Goods).filter_by(sku=good.sku).first() is None:
            session.add(good)
        else:
            update_good = session.query(Goods).filter_by(sku=good.sku).first()
            update_good.owner = good.owner
            update_good.brand = good.brand
            update_good.category = good.category
            update_good.article = good.article
            update_good.price = good.price
            update_good.price_after_spp = good.price_after_spp
            update_good.updated_at = datetime.now()
    session.commit()


def parse_positions(rows) -> List[Positions]:
    positions = []
    for row in rows[3:]:
        if not row:
            continue
        try:
            for day in range(1, datetime.now().day + 1):
                position_for_place = 17 + (day - 1) * 6
                position = Positions()
                position.position = int(row[position_for_place].strip('+'))
                position.sku = int(row[6])
                position.query = row[4]
                position.date = datetime.now().replace(day=day)
                position.created_at = datetime.now()
                position.updated_at = datetime.now()
                positions.append(position)
        except Exception as e:
            logging.error(e)
    return positions


def update_positions(positions: List[Positions]):
    for position in positions:
        position_from_db = session.query(Positions).filter_by(
            sku=position.sku, date=position.date, query=position.query).first()
        if position_from_db is None:
            session.add(position)
        else:
            position_from_db.updated_at = datetime.now()
            if position_from_db.position != position.position:
                position_from_db.position = position.position
    session.commit()


def get_rows_from_google_sheet(range_name, spreadsheet_id):
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=range_name, majorDimension='ROWS').execute()
    values = result.get('values', [])
    return values


def parse_orders(rows) -> List[Orders]:
    orders = []
    for row in rows:
        if not row:
            continue
        try:
            for day in range(1, datetime.now().day + 1):
                position_for_place = 15 + (day - 1) * 6
                order = Orders()
                order.sku = int(row[6])
                order.barcode = 'В разработке'
                order.date = datetime.now().replace(day=day).date()
                order.created_at = datetime.now()
                order.updated_at = datetime.now()
                try:
                    order.fbs_count = int(row[position_for_place-1])
                except:
                    order.fbs_count = 0
                try:
                    print(int(row[position_for_place]))
                    order.fbo_count = int(row[position_for_place])
                except:
                    order.fbo_count = 0
                orders.append(order)
        except Exception as e:
            logging.error(e, exc_info=True)
    return orders


def update_orders(orders: List[Orders]):
    for order in orders:
        order_from_db = session.query(Orders).filter_by(sku=int(order.sku), date=order.date).first()
        # print(order_from_db.date)
        # print(order_from_db)
        if order_from_db is None:
            session.add(order)
        else:
            order_from_db.updated_at = datetime.now()
            if order_from_db.fbs_count != order.fbs_count:
                order_from_db.fbs_count = order.fbs_count
            if order_from_db.fbo_count != order.fbo_count:
                order_from_db.fbo_count = order.fbo_count
    session.commit()


rows = get_rows_from_google_sheet('10.2022', '1LMqyN5w81xnRfvNf0CE75ozH7zMcTLhvYiNjTxHDURo')
update_goods(goods=parse_goods(rows))
update_positions(positions=parse_positions(rows))
update_orders(orders=parse_orders(rows))
