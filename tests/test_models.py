from models.point_of_interest import PointOfInterest


def test_point_of_interest_validation():
    json = {'name': 'Școala auxiliară Bulboaca', 'country': 'Moldova', 'city': 'Anenii&#39; Noi',
            'address': 'Republica Moldova, Anenii Noi, s. Bulboaca', 'categories': 'Accommodation,Medical',
            'description': 'Capacity: 38', 'organizations': 'Domomoga Moldova', 'lat': '46.884741399999996',
            'lng': '29.3123414'}
    point = PointOfInterest(**json)

    assert point.categories == ['Accommodation', 'Medical']
    assert point.organizations == ['Domomoga Moldova']
    assert point.city == "Anenii' Noi"
