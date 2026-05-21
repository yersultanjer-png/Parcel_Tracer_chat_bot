import re
from services.parcel_service import ParcelService


class ChatBotEngine:
    def __init__(self):
        self.parcel_service = ParcelService()
        self.simple_commands = {
            'hello': self.say_hello,
            'hi': self.say_hello,
            'help': self.show_help,
            'what can you do': self.show_help,
            'cities': self.show_cities,
            'prices': self.show_prices,
            'delivery time': self.show_delivery_time,
            'faq': self.show_faq,
            'contacts': self.show_contacts,
            'all parcels': self.show_all_parcels,
            'history': self.show_history_hint,
            'clear': self.show_clear_hint,
            'thanks': self.say_you_are_welcome,
            'thank you': self.say_you_are_welcome,
            'bye': self.say_goodbye
        }

    def get_response(self, message):
        if not message:
            return 'Error: empty input. Please type a command or a question.'

        text = message.lower().strip()

        if text.startswith('track '):
            return self.track_parcel(message[6:].strip().upper())

        if text.startswith('status '):
            return self.track_parcel(message[7:].strip().upper())

        if text.startswith('price '):
            return self.get_price_info(message[6:].strip().lower())

        if text.startswith('time '):
            return self.get_time_info(message[5:].strip().lower())

        if text.startswith('city '):
            return self.check_city(message[5:].strip())

        if re.fullmatch(r'kzt\d{8}', text):
            return self.track_parcel(text.upper())

        if text in self.simple_commands:
            return self.simple_commands[text]()

        return 'Unknown command. Type "help" to see available requests.'

    def say_hello(self):
        return 'Hello! I am Parcel Support Chatbot. I can help with tracking numbers, prices, delivery times, and parcel information.'

    def show_help(self):
        return (
            'Available commands: hello, help, cities, prices, delivery time, faq, contacts, '
            'all parcels, track KZT12345678, status KZT12345678, price standard, '
            'price express, time standard, time express, city Almaty, clear.'
        )

    def show_cities(self):
        return 'Available delivery cities: Almaty, Astana, Shymkent, Karaganda, Aktobe, Taraz.'

    def show_prices(self):
        return 'Current delivery prices: standard - 2000 KZT, express - 3500 KZT.'

    def show_delivery_time(self):
        return 'Estimated delivery time: standard - 5 days, express - 2 days.'

    def show_faq(self):
        return 'FAQ: use a tracking number to track a parcel; use price standard or price express to check shipping cost.'

    def show_contacts(self):
        return 'Support contacts: +7 700 123 45 67, email: support@parcelbot.kz.'

    def show_all_parcels(self):
        parcels = self.parcel_service.get_parcels()
        if not parcels:
            return 'There is no parcel data in the database.'
        return ' | '.join(parcel.as_text() for parcel in parcels)

    def show_history_hint(self):
        return 'Chat history is stored in the SQLite database and displayed in the chat window.'

    def show_clear_hint(self):
        return 'To clear the chat history, click the "Clear History" button below the chat.'

    def say_you_are_welcome(self):
        return 'You are welcome!'

    def say_goodbye(self):
        return 'Goodbye! Have a nice day.'

    def track_parcel(self, tracking_number):
        if not re.fullmatch(r'KZT\d{8}', tracking_number):
            return 'Invalid tracking number. Please use this format: KZT12345678.'

        parcel = self.parcel_service.get_parcel(tracking_number)
        if not parcel:
            return 'Parcel not found. Please check the tracking number and try again.'

        return (
            f'Parcel found. Status: {parcel.status}. Type: {parcel.parcel_type}. '
            f'Price: {parcel.get_price()} KZT. Estimated delivery time: {parcel.get_delivery_days()} days.'
        )

    def get_price_info(self, parcel_type):
        if parcel_type == 'standard':
            return 'Standard delivery price is 2000 KZT.'
        if parcel_type == 'express':
            return 'Express delivery price is 3500 KZT.'
        return 'Unknown delivery type. Please use standard or express.'

    def get_time_info(self, parcel_type):
        if parcel_type == 'standard':
            return 'Standard delivery time is 5 days.'
        if parcel_type == 'express':
            return 'Express delivery time is 2 days.'
        return 'Unknown delivery type. Please use standard or express.'

    def check_city(self, city):
        if not city:
            return 'City name is missing.'

        available_cities = ['almaty', 'astana', 'shymkent', 'karaganda', 'aktobe', 'taraz']
        if city.lower() in available_cities:
            return f'Yes, delivery to {city} is available.'
        return f'Sorry, delivery to {city} is not available yet.'
