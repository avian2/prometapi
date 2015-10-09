# coding: utf-8

import json
import dicttoxml
from django.http import HttpResponse
from prometapi.models import Events, Burja, BurjaZnaki, Counters, ParkiriscaLPT
from prometapi.bicikeljproxy.models import BicikeljData
from prometapi.sos112.models import SOS112
from geoprocessing import get_coordtransform
from django.contrib.gis.geos import GEOSGeometry


class List:
    def __init__(self, model):
        self.model = model

    def __call__(self, request):
        e = self.model.objects.latest('timestamp')
        resp = HttpResponse(e.json_data, mimetype='application/json')
        resp['Access-Control-Allow-Origin'] = '*'
        return resp


events = List(Events)
burja = List(Burja)
burjaznaki = List(BurjaZnaki)
counters = List(Counters)
parkirisca_lpt = List(ParkiriscaLPT)
bicikelj = List(BicikeljData)
sos112 = List(SOS112)


def jsonresponse(func):
    def _inner(*args, **kwargs):
        request = args[0]
        format = request.get('format', 'json')
        data = func(*args, **kwargs)
        if format == 'xml':
            return HttpResponse(dicttoxml.dicttoxml(data), mimetype='application/xml')
        return HttpResponse(json.dumps(data, use_decimal=True, ensure_ascii=True), mimetype='application/json')
    return _inner


@jsonresponse
def gk_to_wgs84(request):

    coords = map(request.GET.get, ['x', 'y'])

    if not all(coords):
        return {
            'status': 'fail',
            'error': 'Missing coordinates x and y as GET parameters.'
        }

    try:
        coords = map(float, coords)
    except ValueError:
        return {
            'status': 'fail',
            'error': 'Coordinates should be floats.'
        }

    xl, xh, yl, yh = 372543, 631496, 34152, 197602
    if not (xl <= coords[0] <= xh and yl <= coords[1] <= yh):
        return {
            'status': 'fail',
            'error': 'Coordinates out of bounds: %d <= x <= %d and %d <= y <= %d.' % (xl, xh, yl, yh)
        }

    geotransform = get_coordtransform()
    point = GEOSGeometry('SRID=3787;POINT (%s %s)' % tuple(coords))
    point.transform(geotransform)
    transformed = (point.x, point.y)

    return {
        'status': 'ok',
        'gk': coords,
        'wgs84': transformed,
        'kml': point.kml,
    }
