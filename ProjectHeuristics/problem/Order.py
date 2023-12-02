"""
AMMM Bakery order
Gianluca Graziadei
"""


class Order(object):

    def __init__(self, order_id, profit, length, min_deliver, max_deliver, surface):
        self._profit = profit
        self._length = length
        self._min_deliver = min_deliver
        self._max_deliver = max_deliver
        self._surface = surface
        self._order_id = order_id
        self.starting_slot = None

    def getId(self):
        return self._order_id

    def getProfit(self):
        return self._profit

    def getLength(self):
        return self._length

    def getMinDeliver(self):
        return self._min_deliver

    def getMaxDeliver(self):
        return self._max_deliver

    def getSurface(self):
        return self._surface

    def setProfit(self, profit):
        self._profit = profit

    def setLength(self, length):
        self._length = length

    def setMinDeliver(self, min_deliver):
        self._min_deliver = min_deliver

    def setMaxDeliver(self, max_deliver):
        self._max_deliver = max_deliver

    def setSurface(self, surface):
        self._surface = surface

    def __str__(self):
        return "order_id: %d (profit: %f, length: %d, min_deliver: %d, max_deliver: %d, surface: %f)" % (
        self._order_id, self._profit, self._length, self._min_deliver, self._max_deliver, self._surface)
