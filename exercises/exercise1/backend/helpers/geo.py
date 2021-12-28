from math import sin, cos, sqrt, pi, radians, asin
import requests


class GeoHelper(object):
    GOOGLE_API_KEY = "AIzaSyByN1mrOTMKPAt1-7Est9AJpOtSxG7Vki8"

    @staticmethod
    def get(url, result_format="text", headers=None, **kargs):
        r = requests.get(url, headers=headers, **kargs)
        if result_format == "json":
            return r.json()
        elif result_format == "text":
            return r.text
        else:
            return r.content

    @staticmethod
    def to_rad(degrees):
        return degrees * pi / 180

    @staticmethod
    def geo_distance(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        d_lon = lon2 - lon1
        d_lat = lat2 - lat1
        a = sin(d_lat/2)**2 + cos(lat1) * cos(lat2) * sin(d_lon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6371 * c
        return km

    @staticmethod
    def point_inside_polygon(y, x, poly):
        # poly must be an array of (lat, lng)
        n = len(poly)
        inside = False

        p1x, p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        x_ints = 0
                        if p1y != p2y:
                            x_ints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= x_ints:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    @staticmethod
    def get_address_data(address):
        address = address.replace(" ", "+")
        req = GeoHelper.get(
            "https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}".format(
                address,
                GeoHelper.GOOGLE_API_KEY
            ),
            "json"
        )
        return req

    @staticmethod
    def get_address_lat_lng(address):
        data = GeoHelper.get_address_data(address)
        if 'status' in data and data['status'] == "OK":
            return data["results"][0]["geometry"]['location']['lat'], data["results"][0]["geometry"]['location']['lng']
        return False, False
