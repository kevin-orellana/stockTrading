# Kevin F Orellana
# Trader Class
# Notes:
#   - This Trader class holds
#       - a string variable for Trader name
#       - a dictionary of 'symbol'-PositionsStack key-value pairs
#   - Trader class has functions:
#       - trade(data_list)
#           - proccesses and returns a list of various variables
#       - openShort(symbolStack, quantity, price)
#           - pushes a short position onto 'symbol'-specific PositionsStack
#       - openLong(symbolStack, quantity, price)
#       - closeShort(symbolStack, quantity, price)
#           - closes a previous short position and can recursively
#             call itself to continue closing proceeding short positions
#       - closeLong(symbolStack, quantity, price)
from PositionsStack import *
class Trader:
    def __init__(self, name):
        self.name = name  # trader name
        self.open_positions = {}  # contains symbol-PositionsStack key-value pairs

    #  processes and returns a data list with updated realization amount
    def trade(self, data):
        #  parsing data
        if data[4] == "QTY":
            return data
        date = data[0]
        date_and_time = data[1]
        action = data[2]
        symbol = data[3]
        quantity = float(data[4])
        price = float(data[5])
        if (action == "BUY"):
            action = int(1)  # if action == 1, trader is buying stock
        else:
            action = int(0)  # if action == 0, trader is selling stock

        # If 'symbol' is NOT in active portfolio, create a symbol-PositionsStack entry and
        # add the position
        if not (symbol in self.open_positions):
            stack = PositionsStack(symbol)  # creates empty stack for 'symbol'
            if action:  # if action is to start a LONG position
                self.openLong(stack, quantity, price)
            else:  # if action is to start SHORT position
                self.openShort(stack, quantity, price)

            self.open_positions[symbol] = stack  # adds symbol-stack entry to Trader hash table
            return self.excelData(date, date_and_time, action, symbol, quantity, price)

        # If 'symbol' IS in active portfolio, the block below opens a new or closes the last position
        elif symbol in self.open_positions:
            r = 0.0
            stack = self.open_positions.get(symbol)
            #  opening a Long or Short position
            if stack.isEmpty():
                if action:
                    self.openLong(stack, quantity, price)
                else:
                    self.openShort(stack, quantity, price)
                return self.excelData(date, date_and_time, action, symbol, quantity, price)
            last_position = stack.lastPosition()
            if action == last_position:  # if trade does NOT work to close a position
               if action:
                   self.openLong(stack, quantity, price)
               else:
                   self.openShort(stack, quantity, price)
               return self.excelData(date, date_and_time, action, symbol, quantity, price)

            else:
                if last_position:  # if last_position was a LONG position
                    r = self.closeLong(stack, quantity, price)
                elif (last_position == 0):  # if last_position was a SHORT position
                    r = self.closeShort(stack, quantity, price)
            return self.excelDataRealized(date, date_and_time, action, symbol, quantity, price, r)

    # opens a long position by pushing a "buying" state onto PositionsStack
    def openLong(self, stack, quantity, price):
        stack.push([1, quantity, price])

    # opens a short position by pushing a "selling" state onto PositionsStack
    def openShort(self, stack, quantity, price):
        stack.push([0, quantity, price])

    # closeShort returns the realization amount when a trade has been determined to work to
    # close a position in the trade() function
    def closeShort(self, stack, quantity, price):
        realization = 0.0
        deltaStock = float(quantity)
        prevStock = float(stack.lastPositionStockAmount())
        prevPrice = stack.lastPrice()
        # if there will be remaining stock after working to close a short position
        if (prevStock > deltaStock):
            realization = (prevPrice - price) * (deltaStock)
            newLastPosStockAmount = prevStock - deltaStock
            stack.updateLastPosStockAmount(newLastPosStockAmount)
            return realization
        # if there is not enough previous-stock after working to close a short position
        elif (prevStock < deltaStock):
            leftover = deltaStock - prevStock
            realization = (prevPrice - price) * float(prevStock)
            stack.pop() # last position, which was a short, is now closed.
            if (stack.isEmpty()):
                newLastPos = 1  # new last position is buying
            else:
                newLastPos = stack.lastPosition()
            if (newLastPos == 1):
                # create a new long position
                self.openLong(stack, leftover, price)
                # return 0.0
                return realization
            elif (newLastPos == 0):
                realization += self.closeShort(stack, leftover, price)
                return realization
        elif (prevStock == deltaStock):
            realization += (prevPrice - price) * prevStock
            stack.pop()
            return realization
        else:
            print("ERROR WITH: ")
            print(stack, quantity, price)

    # closeShort returns the realization amount when a trade has been determined to work to
    #  close a position in the trade() function
    def closeLong(self, stack, quantity, price):
        realization = 0.0
        deltaStock = float(quantity)
        prevStock = float(stack.lastPositionStockAmount())
        prevPrice = stack.lastPrice()
        # if there will be remaining stock after working to close a long position
        if (prevStock > deltaStock):
            remStock = prevStock - deltaStock
            realization = (price - prevPrice) * float(deltaStock)
            stack.updateLastPosStockAmount(remStock)
            return realization
        # if there is not enough previous-stock after working to close a long position
        elif (prevStock < deltaStock):
            remStock = deltaStock - prevStock
            realization = (price - prevPrice) * float(prevStock)
            stack.pop()  # previous long position closed and removed from stack
            if (stack.isEmpty()):  # if stack empty, new last position = selling
                newLastPos = 0  # signals creation of a short position
            else:
                newLastPos = stack.lastPosition()
            if (newLastPos == 1):  # recursive call to continue closing a new, long position
                realization += self.closeLong(stack, remStock, price)
                return realization
            elif (newLastPos == 0):  # if new position is also a long position, push the remaining stock as a SHORT position
                self.openShort(stack, remStock, price)
                # stack.push([0, remStock, price])  # new short position created
                # print("realization: ", realization, "for symbol ", stack)
                return realization
        elif (prevStock == deltaStock):
            realization = (price - prevPrice) * float(deltaStock)
            stack.pop()
            return realization
        else:
            print("ERROR WITH: ")
            print(stack, quantity, price)

    # prints all the open positions the trader has
    def printPositionsList(self):
        print("printing open positions: ")
        for k, v in self.open_positions.items():
            print(k)
            print(v.openPositionsList())

    # returns list in data without any realized profit or loss
    def excelData(self, date, date_and_time, action, symbol, quantity, price):
        if (action == 1):
            action = "BUY"
        else:
            action = "SELL"
        return [date, date_and_time, str(action), symbol, str(quantity), str(price), str(0.0)]

    # returns list in data with realized profit or loss
    def excelDataRealized(self, date, date_and_time, action, symbol, quantity, price,realizedProfitLoss):
        if (action == 1):
            action = "BUY"
        else:
            action = "SELL"
        #  sets level of precision in profit/loss realization
        realizedProfitLoss = str(("%.4f" % realizedProfitLoss))
        # print(symbol, realizedProfitLoss)
        return [date, date_and_time, str(action), symbol, str(quantity), str(price), str(realizedProfitLoss)]
