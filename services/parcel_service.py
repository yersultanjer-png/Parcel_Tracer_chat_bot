from services.database import find_parcel_by_tracking, get_all_parcels


class Parcel:
    def __init__(self, tracking_number, sender, receiver, city, status):
        self.tracking_number = tracking_number
        self.sender = sender
        self.receiver = receiver
        self.city = city
        self.status = status
        self.parcel_type = 'base'

    def get_price(self):
        return 0

    def get_delivery_days(self):
        return 0

    def as_text(self):
        return (
            f'{self.tracking_number}: {self.sender} to {self.receiver}, '
            f'{self.city}, {self.status}, type: {self.parcel_type}'
        )


class StandardParcel(Parcel):
    def __init__(self, tracking_number, sender, receiver, city, status):
        super().__init__(tracking_number, sender, receiver, city, status)
        self.parcel_type = 'standard'

    def get_price(self):
        return 2000

    def get_delivery_days(self):
        return 5


class ExpressParcel(Parcel):
    def __init__(self, tracking_number, sender, receiver, city, status):
        super().__init__(tracking_number, sender, receiver, city, status)
        self.parcel_type = 'express'

    def get_price(self):
        return 3500

    def get_delivery_days(self):
        return 2


class ParcelService:
    def create_parcel(self, row):
        tracking_number, sender, receiver, city, status, parcel_type = row
        if parcel_type == 'express':
            return ExpressParcel(tracking_number, sender, receiver, city, status)
        return StandardParcel(tracking_number, sender, receiver, city, status)

    def get_parcel(self, tracking_number):
        row = find_parcel_by_tracking(tracking_number)
        if not row:
            return None
        return self.create_parcel(row)

    def get_parcels(self):
        rows = get_all_parcels()
        return [self.create_parcel(row) for row in rows]
