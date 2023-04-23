# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# import requests
# import json
# import re

import sqlite3
from typing import Dict, Any, Text, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionQueryPrice(Action):
    def name(self) -> Text:
        return "action_query_price"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Lấy mã sản phẩm từ intent
            product_id = tracker.latest_message['entities'][0]['value']

            # Tạo kết nối đến SQLite database
            connection = sqlite3.connect('./db/rasa_store.db')

            # Tạo một đối tượng cursor
            cursor = connection.cursor()
        
            # Thực hiện truy vấn để lấy giá cả của sản phẩm
            cursor.execute("SELECT NAME, PRICE FROM goods WHERE ID=?", (product_id,))

            # Lấy giá cả và trả về cho người dùng
            result = cursor.fetchone()
            if result:
                name, price = result
                dispatcher.utter_message(f"Sản phẩm {name} có mã {product_id} và giá là {price}")
            else:
                dispatcher.utter_message(f"Sản phẩm {product_id} không tồn tại trong hệ thống")
        except TypeError:
            # Trường hợp mã sản phẩm không tồn tại trong database
            dispatcher.utter_message(f"Sản phẩm không tồn tại trong hệ thống")
        
        # Đóng kết nối database
        connection.close()

        return [SlotSet("product_id", product_id)]
    
class ActionQueryAvailabilityAsked(Action):
    def name(self) -> Text:
        return "action_query_availability_asked"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Truy xuất mã sản phẩm từ slot
            product_id = tracker.get_slot("product_id")

            # Tạo kết nối đến SQLite database
            connection = sqlite3.connect('./db/rasa_store.db')

            # Tạo một đối tượng cursor
            cursor = connection.cursor()

            # Thực hiện truy vấn để lấy số lượng sản phẩm còn lại
            cursor.execute("SELECT COUNT FROM goods WHERE ID=?", (product_id,))

            # Lấy số lượng sản phẩm còn lại và trả về cho người dùng
            count = cursor.fetchone()[0]
            dispatcher.utter_message(f"Số lượng sản phẩm {product_id} còn lại là {count}")
        except TypeError:
            # Trường hợp mã sản phẩm không tồn tại trong database
            dispatcher.utter_message(f"Bạn muốn hỏi sản phẩm nào vậy?")
        connection.close()
        return []
    
class ActionQueryAvailability(Action):
    def name(self) -> Text:
        return "action_query_availability"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Lấy mã sản phẩm từ intent
            product_id = tracker.latest_message['entities'][0]['value']

            # Tạo kết nối đến SQLite database
            connection = sqlite3.connect('./db/rasa_store.db')

            # Tạo một đối tượng cursor
            cursor = connection.cursor()

            # Thực hiện truy vấn để lấy số lượng sản phẩm còn lại
            cursor.execute("SELECT NAME, COUNT FROM goods WHERE ID=?", (product_id,))

            # Lấy số lượng sản phẩm còn lại và trả về cho người dùng
            # Lấy giá cả và trả về cho người dùng
            result = cursor.fetchone()
            if result:
                name, count = result
                dispatcher.utter_message(f"Sản phẩm {name} có mã {product_id} và số lượng còn lại là {count}")
            else:
                dispatcher.utter_message(f"Sản phẩm {product_id} không tồn tại trong hệ thống")
        except TypeError:
            # Trường hợp mã sản phẩm không tồn tại trong database
            dispatcher.utter_message(f"Sản phẩm không tồn tại trong hệ thống")
        connection.close()
        return [SlotSet("product_id", product_id)]

class ActionQueryPriceAsked(Action):
    def name(self) -> Text:
        return "action_query_price_asked"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Truy xuất mã sản phẩm từ slot
            product_id = tracker.get_slot("product_id")

            # Tạo kết nối đến SQLite database
            connection = sqlite3.connect('./db/rasa_store.db')

            # Tạo một đối tượng cursor
            cursor = connection.cursor()

            # Thực hiện truy vấn để lấy số lượng sản phẩm còn lại
            cursor.execute("SELECT PRICE FROM goods WHERE ID=?", (product_id,))

            # Lấy số lượng sản phẩm còn lại và trả về cho người dùng
            price = cursor.fetchone()[0]
            dispatcher.utter_message(f"Giá sản phẩm {product_id} là {price}")
        except TypeError:
            # Trường hợp mã sản phẩm không tồn tại trong database
            dispatcher.utter_message(f"Bạn muốn hỏi sản phẩm nào vậy?")
        connection.close()
        return []

#theo ten---------------------------------------------------------------------------------------------------------------
class ActionQueryPriceByName(Action):
    def name(self) -> Text:
        return "action_query_price_by_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Lấy mã sản phẩm từ intent
            product_name = tracker.latest_message['entities'][0]['value']

            # Tạo kết nối đến SQLite database
            connection = sqlite3.connect('./db/rasa_store.db')

            # Tạo một đối tượng cursor
            cursor = connection.cursor()

            # Thực hiện truy vấn để lấy số lượng sản phẩm còn lại
            cursor.execute("SELECT ID, NAME, PRICE FROM goods WHERE NAME LIKE ?", (product_name,))

            # Lấy số lượng sản phẩm còn lại và trả về cho người dùng
            # Lấy giá cả và trả về cho người dùng
            result = cursor.fetchone()
            if result:
                product_id, name, price = result
                dispatcher.utter_message(f"Sản phẩm {name} có mã {product_id} và có giá là {price}")
                return [SlotSet("product_id", product_id)]
            else:
                dispatcher.utter_message(f"Không có sản phẩm nào có tên là  {product_name} trong hệ thống, hãy chắc chắn rằng bạn đã nhập đúng tên sản phẩm theo dạng viết IN HOA KHÔNG DẤU")
        except TypeError:
            # Trường hợp mã sản phẩm không tồn tại trong database
            dispatcher.utter_message(f"Không có sản phẩm nào tên như vậy trong hệ thống, hãy chắc chắn rằng bạn đã nhập đúng tên sản phẩm theo dạng viết IN HOA KHÔNG DẤU")
        connection.close()
        return []
    
class ActionQueryAvailabilityByName(Action):
    def name(self) -> Text:
        return "action_query_availability_by_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Lấy mã sản phẩm từ intent
            product_name = tracker.latest_message['entities'][0]['value']

            # Tạo kết nối đến SQLite database
            connection = sqlite3.connect('./db/rasa_store.db')

            # Tạo một đối tượng cursor
            cursor = connection.cursor()

            # Thực hiện truy vấn để lấy số lượng sản phẩm còn lại
            cursor.execute("SELECT ID, NAME, COUNT FROM goods WHERE NAME LIKE ?", (product_name,))

            # Lấy số lượng sản phẩm còn lại và trả về cho người dùng
            # Lấy giá cả và trả về cho người dùng
            result = cursor.fetchone()
            if result:
                id, name, count = result
                dispatcher.utter_message(f"Sản phẩm {name} có mã {id} và số lượng còn lại là {count}")
                return [SlotSet("product_id", id)]
            else:
                dispatcher.utter_message(f"Không có sản phẩm nào có tên là  {product_name} trong hệ thống, hãy chắc chắn rằng bạn đã nhập đúng tên sản phẩm theo dạng viết IN HOA KHÔNG DẤU")
        except TypeError:
            # Trường hợp mã sản phẩm không tồn tại trong database
            dispatcher.utter_message(f"Không có sản phẩm nào có tên như vậy trong hệ thống, hãy chắc chắn rằng bạn đã nhập đúng tên sản phẩm theo dạng viết IN HOA KHÔNG DẤU")
        connection.close()
        return []
