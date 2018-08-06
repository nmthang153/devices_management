from django.test import TestCase
from .models import devices, Project, order, supplement


class DeviceTest(TestCase):
    def setUp(self):
        devices.objects.create(
            code= 'test code',
            name = 'test name',
            type = 'test type',
            osType = 'test os',
            version = 'test ver',
            status = 'test stt'
        )
    def test_device_list_view(self):
        response = self.client.get('/listdevices/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'test code','test name', 'test os', 'test ver','test stt')
        self.assertTemplateUsed(response, 'device/listdevices.html')

    def test_device_edit_view(self):
        response = self.client.get('/edit/1')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'test code','test name', 'test os', 'test ver','test stt')
        self.assertTemplateUsed(response, 'device/edit.html')