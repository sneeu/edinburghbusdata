import csv
from xml.etree.ElementTree import ElementTree


def main():
    tree = ElementTree()
    tree.parse('stop_route.xml')
    markers = tree.find('markers')
    stops = markers.getiterator('busStop')
    for stop in stops:
        sms = stop.find('sms').text
        name = stop.find('nom').text
        x = stop.find('x').text
        y = stop.find('y').text
        services = ','.join([service.find('mnemo').text for service in stop.find('services').getiterator('service')])
        print sms, name, x, y, services


if __name__ == '__main__':
    main()
