# !/usr/bin/env python
# encoding: utf-8
from django.contrib.gis.geos import Polygon

from django.test import TestCase

from seed.landing.models import SEEDUser as User

from seed.models.properties import PropertyState

from seed.test_helpers.fake import FakePropertyStateFactory

from seed.utils.geocode import bounding_box_wkt
from seed.utils.organizations import create_organization
from seed.utils.ubid import (
    centroid_wkt,
    decode_ubids,
)


class UbidSpecificWktMethods(TestCase):
    def setUp(self):
        user_details = {
            'username': 'test_user@demo.com',
            'password': 'test_pass',
        }
        self.user = User.objects.create_superuser(
            email='test_user@demo.com', **user_details
        )
        self.org, _, _ = create_organization(self.user)
        self.org.save()

        self.property_state_factory = FakePropertyStateFactory(organization=self.org)

    def test_centroid_wkt_takes_a_state_and_returns_the_WKT_string_or_None(self):
        property_details = self.property_state_factory.get_details()
        property_details['organization_id'] = self.org.id

        no_centroid_property = PropertyState(**property_details)
        no_centroid_property.save()

        property_details['centroid'] = 'POLYGON ((0 0, 4 0, 4 4, 0 4, 0 0))'

        centroid_property = PropertyState(**property_details)
        centroid_property.save()

        no_centroid_record = PropertyState.objects.get(pk=no_centroid_property.id)
        geocoded_record = PropertyState.objects.get(pk=centroid_property.id)

        self.assertIsNone(no_centroid_record.centroid)
        self.assertIsNone(centroid_wkt(no_centroid_record))

        self.assertIsInstance(geocoded_record.centroid, Polygon)
        self.assertEqual('POLYGON ((0 0, 4 0, 4 4, 0 4, 0 0))', centroid_wkt(centroid_property))


class UbidUtilMethods(TestCase):
    def setUp(self):
        user_details = {
            'username': 'test_user@demo.com',
            'password': 'test_pass',
        }
        self.user = User.objects.create_superuser(
            email='test_user@demo.com', **user_details
        )
        self.org, _, _ = create_organization(self.user)
        self.org.save()

        self.property_state_factory = FakePropertyStateFactory(organization=self.org)

    def test_decode_ubids_is_successful_when_valid_UBID_provided(self):
        property_details = self.property_state_factory.get_details()
        property_details['organization_id'] = self.org.id
        property_details['ubid'] = '86HJPCWQ+2VV-1-3-2-3'

        property = PropertyState(**property_details)
        property.save()
        properties = PropertyState.objects.filter(pk=property.id)

        decode_ubids(properties)
        refreshed_property = PropertyState.objects.get(pk=property.id)
        property_bounding_box_wkt = (
            "POLYGON ((-87.56021875000002 41.74504999999999, "
            "-87.56021875000002 41.74514999999997, "
            "-87.56043749999996 41.74514999999997, "
            "-87.56043749999996 41.74504999999999, "
            "-87.56021875000002 41.74504999999999))"
        )
        property_centroid_wkt = (
            "POLYGON ((-87.56031249999999 41.74509999999998, "
            "-87.56031249999999 41.74512499999997, "
            "-87.56034374999999 41.74512499999997, "
            "-87.56034374999999 41.74509999999998, "
            "-87.56031249999999 41.74509999999998))"
        )
        self.assertEqual(property_bounding_box_wkt, bounding_box_wkt(refreshed_property))
        self.assertEqual(property_centroid_wkt, centroid_wkt(refreshed_property))
        self.assertEqual(refreshed_property.latitude, 41.7451)
        self.assertEqual(refreshed_property.longitude, -87.560328125)

    def test_decode_ubids_does_nothing_if_no_UBID_provided(self):
        property_details = self.property_state_factory.get_details()
        property_details['organization_id'] = self.org.id

        property = PropertyState(**property_details)
        property.save()
        properties = PropertyState.objects.filter(pk=property.id)

        decode_ubids(properties)
        refreshed_property = PropertyState.objects.get(pk=property.id)

        self.assertIsNone(bounding_box_wkt(refreshed_property))
        self.assertIsNone(centroid_wkt(refreshed_property))

    def test_decode_ubids_is_successful_when_v2_format_C_NW_SE_UBID_provided(self):
        property_details = self.property_state_factory.get_details()
        property_details['organization_id'] = self.org.id
        property_details['ubid'] = '849VQJH6+95J-849VQJH5+VGW-849VQJG6+XV8'

        property = PropertyState(**property_details)
        property.save()
        properties = PropertyState.objects.filter(pk=property.id)

        decode_ubids(properties)
        refreshed_property = PropertyState.objects.get(pk=property.id)
        property_bounding_box_wkt = (
            "POLYGON ((-122.38778125 37.77740000000001, "
            "-122.38778125 37.77975000000001, "
            "-122.3911875 37.77975000000001, "
            "-122.3911875 37.77740000000001, "
            "-122.38778125 37.77740000000001))"
        )
        property_centroid_wkt = (
            "POLYGON ((-122.38959375 37.77845, "
            "-122.38959375 37.778475, "
            "-122.389625 37.778475, "
            "-122.389625 37.77845, "
            "-122.38959375 37.77845))"
        )
        self.assertEqual(property_bounding_box_wkt, bounding_box_wkt(refreshed_property))
        self.assertEqual(property_centroid_wkt, centroid_wkt(refreshed_property))
        self.assertEqual(refreshed_property.latitude, 37.778575)
        self.assertEqual(refreshed_property.longitude, -122.389484375)

    def test_decode_ubids_doesnt_throw_an_error_if_an_invalid_ubid_is_provided(self):
        property_details = self.property_state_factory.get_details()
        property_details['organization_id'] = self.org.id
        property_details['ubid'] = 'invalidubid'

        property = PropertyState(**property_details)
        property.save()
        properties = PropertyState.objects.filter(pk=property.id)

        decode_ubids(properties)

        refreshed_property = PropertyState.objects.get(pk=property.id)

        self.assertIsNone(bounding_box_wkt(refreshed_property))
        self.assertIsNone(centroid_wkt(refreshed_property))
