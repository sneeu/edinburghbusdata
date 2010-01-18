import csv
import glob
from xml.etree.ElementTree import ElementTree


SERVICE_MNEMONICS = '1,2,3,3A,4,5,7,8,10,11,12,14,15,15A,16,18,19,20,21,22,23,24,25,X25,26,X26,27,29,X29,30,31,X31,32,33,34,35,36,37,38,41,42,44,44A,45,47,X47,48,X48,49,61,67,69,100,109,N3,N8,N16,N22,N25,N26,N30,N31,N37,N44'


class BusStop(object):
    def __init__(self, sms, name, x, y):
        self.sms = sms
        self.name = name
        self.x = x
        self.y = y
        self.routes = []

    def __str__(self):
        return '"%s","%s","%s","%s",%s' % (self.sms, self.name, self.x, self.y, ','.join(self.routes), )

    def sql(self):
        r = [
            "INSERT INTO busstop (sms, name, x, y) VALUES ('%s', '%s', '%s', '%s');" % (self.sms, self.name, self.x, self.y, )
        ]
        for route in self.routes:
            r.append("INSERT INTO stop (sms, service) VALUES ('%s', '%s');" % (self.sms, route, ))

        return '\n'.join(r)


def main():
    stop_objs = {}

    for service in SERVICE_MNEMONICS.split(','):
        print "INSERT INTO service (mnemonics) VALUES ('%s');" % service

        tree = ElementTree()
        tree.parse('data/%s.xml' % service)

        markers = tree.find('markers')
        stops = markers.getiterator('busStop')
        for stop in stops:
            sms = stop.find('sms').text
            name = stop.find('nom').text
            x = stop.find('x').text
            y = stop.find('y').text

            stop_obj = stop_objs.get(sms, None)
            if stop_obj is None:
                stop_obj = BusStop(sms, name, x, y)
                stop_objs[sms] = stop_obj
            stop_obj.routes.append(service)

    for stop in stop_objs.values():
        print stop.sql()


if __name__ == '__main__':
    main()
