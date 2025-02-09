from dataclasses import dataclass


@dataclass
class Trade:
    side: str
    price: float
    quantity: float

@dataclass
class Position:
    quantity: float
    avg_price: float

    def update(self, trade: Trade):
        assert trade.quantity > 0.0
        self.avg_price = ((self.quantity * self.avg_price + trade.quantity * trade.price) /
                          (self.quantity + trade.quantity))
        self.quantity += trade.quantity

    def get_pnl(self, price: float) -> float:
        return self.quantity * (price - self.avg_price)

# def test_update_position():
#     p = Position(0.0, 0.0)
#     p.update(Trade("buy", 100.0, 1.0))
#
#     assert p.avg_price == 100.0
#     assert p.quantity == 1.0
#
#     p.update(Trade("buy", 200.0, 1.0))
#
#     assert p.avg_price == 150.0
#     assert p.quantity == 2.0

class Account:

    def __init__(self, balance: float):
        self.balance = balance
        self.long = Position(0.0, 0.0)
        self.short = Position(0.0, 0.0)
        self.margin = 0.0

    def execute(self, trade: Trade):
        if trade.side == "buy":
            self.long.update(trade)
            self.balance -= trade.quantity * trade.price
        else:
            self.short.update(trade)
            self.margin += trade.quantity * trade.price

    def close(self, price: float):
        self.balance += (self.long.quantity - self.short.quantity) * price
        self.balance += self.margin
        self.margin = 0.0

    def get_unrealized_pnl(self, price: float):
        return self.long.get_pnl(price) - self.short.get_pnl(price)


trades = [
    Trade("buy", 650.0, 1.0),
    Trade("sell", 640.0, 0.25),
    Trade("sell", 620.0, 0.25)
]

acc = Account(10000.0)


def get_pnl_according_to_prices(trades: list[Trade], prices: list[float]):
    for trade in trades:
        acc.execute(trade)
    for price in prices:
        pnl = acc.get_unrealized_pnl(price)
        print(f"pnl after close the trades at {price} is: ", pnl)

if __name__ == '__main__':
    get_pnl_according_to_prices(trades, [600.0, 500.0, 400.0, 660.0, 700.0])