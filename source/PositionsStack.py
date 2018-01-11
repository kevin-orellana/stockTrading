# Kevin F Orellana
# PositionsStack Class
# Notes:
#   - This stack class has the basic functions of a generic Stack class
#   - Each stack element is a list that contains
#       - the position state (1) if long, (0) if short
#       - the quantity of stock in the that specific position and price
#       - the price of the last position's stock

class PositionsStack:
    def __init__(self, symbol):
        self.symbol = symbol
        self.items = []
    def isEmpty(self):
        return self.items == []
    def push(self, position):
        self.items.append(position)
    def pop(self):
        return self.items.pop()
    def peek(self):
        return self.items[len(self.items)-1]
    def size(self):
        return len(self.items)
    def openPositionsList(self):
        return self.items
    # if last position was a long, returns 1, else it returns 0 (short position)
    def lastPosition(self):
        return self.items[len(self.items)-1][0]

    # returns the price of previous stock
    def lastPrice(self):
        return float(self.items[len(self.items)-1][2])

    # returns the amount of stock remaining in the last position
    def lastPositionStockAmount(self):
        return float(self.items[len(self.items)-1][1])
    # updates the last position's stock amount to newAmount
    def updateLastPosStockAmount(self, newAmount):
        self.items[len(self.items) - 1][1] = newAmount
    def __str__(self):
        return str(self.symbol)

