import json
import os
import requests
from typing import Dict, Any

MENU = [
    {"id": "1", "name": "Классический бургер", "price": 350},
    {"id": "2", "name": "Чизбургер", "price": 400},
    {"id": "3", "name": "Двойной бургер", "price": 500},
    {"id": "4", "name": "Вегетарианский бургер", "price": 380},
]

def send_message(chat_id: int, text: str, reply_markup: Dict = None) -> None:
    """Отправка сообщения в Telegram"""
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    
    requests.post(url, json=data)

def get_menu_keyboard() -> Dict:
    """Создание клавиатуры с меню"""
    keyboard = []
    for item in MENU:
        keyboard.append([{
            'text': f"{item['name']} - {item['price']}₽",
            'callback_data': f"order_{item['id']}"
        }])
    
    return {'inline_keyboard': keyboard}

def handle_start(chat_id: int) -> None:
    """Обработка команды /start"""
    text = "🍔 <b>Добро пожаловать в Пит Стоп Бургер!</b>\n\nВыберите бургер из меню:"
    send_message(chat_id, text, get_menu_keyboard())

def handle_order(chat_id: int, item_id: str, username: str = None) -> None:
    """Обработка заказа"""
    item = next((x for x in MENU if x['id'] == item_id), None)
    if not item:
        return
    
    # Подтверждение клиенту
    text = f"✅ <b>Заказ принят!</b>\n\n{item['name']} - {item['price']}₽\n\nМы свяжемся с вами в ближайшее время."
    send_message(chat_id, text)
    
    # Уведомление админу
    admin_chat_id = os.environ.get('TELEGRAM_ADMIN_CHAT_ID')
    if admin_chat_id:
        admin_text = f"🔔 <b>Новый заказ!</b>\n\n"
        admin_text += f"Товар: {item['name']}\n"
        admin_text += f"Цена: {item['price']}₽\n"
        admin_text += f"От: @{username if username else 'аноним'}\n"
        admin_text += f"Chat ID: {chat_id}"
        send_message(int(admin_chat_id), admin_text)

def handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    """Обработчик webhook запросов от Telegram"""
    
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': ''
        }
    
    try:
        body = json.loads(event.get('body', '{}'))
        
        # Обработка текстовых команд
        if 'message' in body:
            message = body['message']
            chat_id = message['chat']['id']
            text = message.get('text', '')
            
            if text == '/start':
                handle_start(chat_id)
        
        # Обработка нажатий на кнопки
        elif 'callback_query' in body:
            query = body['callback_query']
            chat_id = query['message']['chat']['id']
            data = query['data']
            username = query['from'].get('username')
            
            if data.startswith('order_'):
                item_id = data.replace('order_', '')
                handle_order(chat_id, item_id, username)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'ok': True})
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
