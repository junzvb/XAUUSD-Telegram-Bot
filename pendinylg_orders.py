class PendingOrders:
    def __init__(self):
        self.orders = []

    def add_order(self, signal):
        if signal not in self.orders:
            self.orders.append(signal)

    def get_orders(self):
        return self.orders

    def clear_orders(self):
        self.orders = []

pending_orders = PendingOrders()
