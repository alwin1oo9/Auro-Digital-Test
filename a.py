# get orders attribute

# parse xml
import xml.etree.ElementTree as ET
tree = ET.parse('temp.xml')
root = tree.getroot()

class Book:
    def __init__(self, name):
        self.name = name
        self.sell_book = [] #min heap
        self.buy_book = [] #max heap
books = {
}
time = 0
for child in root:
    # add time to each order
    child.attrib['Time'] = time
    book = child.attrib['book']
    price = float(child.attrib['price'])
    op = child.attrib['operation']
    vol = float(child.attrib['volume'])
    time += 1
    if book not in books:
        books[book] = Book(book)
    if child.tag == 'DeleteOrder':
        if child.attrib['operation'] == 'SELL':
            books[book].sell_book.remove(child.attrib['orderId'])
        else:
            books[book].buy_book.remove(child.attrib['orderId'])
    else:
        if child.attrib['operation'] == 'SELL':
            for order in books[book].buy_book:
                if float(order.attrib['price']) >= price:
                    if order.attrib['volume'] > vol:
                        order.attrib['volume'] -= vol
                        vol = 0
                    else:
                        vol -= int(order.attrib['volume'])
                        books[book].buy_book.remove(order)
                        # sort by price
                        books[book].buy_book.sort(key=lambda x: float(x.attrib['price']), reverse=True)
                else:
                    break
            if vol > 0:
                child.attrib['volume'] = vol
                books[book].sell_book.append(child)
                # sort by price
                books[book].sell_book.sort(key=lambda x: float(x.attrib['price']))
                break
        else:
            for order in books[book].sell_book:
                if float(order.attrib['price']) <= price:
                    if order.attrib['volume'] > vol:
                        order.attrib['volume'] -= vol
                        vol = 0
                    else:
                        vol -= int(order.attrib['volume'])
                        books[book].sell_book.remove(order)
                        # sort by price
                        books[book].sell_book.sort(key=lambda x: float(x.attrib['price']))
                else:
                    break
            if vol > 0:
                child.attrib['volume'] = vol
                books[book].buy_book.append(child)
                # sort by price
                books[book].buy_book.sort(key=lambda x: float(x.attrib['price']), reverse=True)
                break

    