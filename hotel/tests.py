import datetime

from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup
from rest_framework import status
from datetime import date
from hotel.models import Room, OrderRoom
from django.contrib.auth.models import User


class TestOrder(TestCase):
    def test_render_html(self):
        response = self.client.get(reverse("Hotel:search-room"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        soup = BeautifulSoup(response.content.decode(), features="html.parser")
        form = soup.find("html").find("body").find("form")
        labels = form.find_all("label")
        self.assertEqual(labels[0].text, 'Start Date')
        self.assertEqual(labels[1].text, 'End Date')

    def test_search_free_rooms(self):
        price_for_day = 22.5
        Room.objects.create(
            capacity=1,
            price_for_day=price_for_day,
            description="test",
            number=201,
            image="room/img.jpg"
        )
        user = User.objects.create_user("test_username", "test@mail", "test_pwd")

        self.client.force_login(user)
        start_date = date(year=2022, month=1, day=1)
        end_date = date(year=2022, month=1, day=10)
        response = self.client.get(
            reverse("Hotel:search-room"),
            data={
                "start_date": start_date,
                "end_date": end_date
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        soup = BeautifulSoup(response.content.decode(), features="html.parser")
        prices = soup.find("html").find("body").find_all("h3", {"class": "price"})
        origin_price = price_for_day * (end_date - start_date).days
        self.assertEqual(prices[0].text.replace(",", ".")[:-1], f'Price: {origin_price}')
        start_date_html, end_date_html = soup.find_all("input")[2:]
        self.assertEqual(start_date_html.get("value"), start_date.strftime("%Y-%m-%d"))
        self.assertEqual(end_date_html.get("value"), end_date.strftime("%Y-%m-%d"))

        action = soup.find("form").get("action")
        room_id = action.split("/")[-2]
        self.assertEqual(OrderRoom.objects.count(), 0)
        response = self.client.post(
            reverse("Hotel:order-room", kwargs={"room_id": room_id}),
            data={
                "start_date": start_date,
                "end_date": end_date
            }
        )
        self.assertEqual(OrderRoom.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_permission_for_order(self):
        user = User.objects.create_user("test_username", "test@mail", "test_pwd")
        room = Room.objects.create(
            capacity=1,
            price_for_day=22.3,
            description="test",
            number=201,
            image="room/img.jpg"
        )
        self.client.force_login(user)
        response = self.client.post(
            reverse("Hotel:create-order-room"),
            data={
                "room": room.id,
                "start_date": datetime.datetime(year=2022, month=1, day=1, hour=1, minute=1),
                "end_date": datetime.datetime(year=2022, month=1, day=10, hour=2)
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                'room': room.id,
                'start_date': '2022-01-01T01:01:00+01:00',
                'end_date': '2022-01-10T02:00:00+01:00'
            }
        )
        frend_user = User.objects.create_user("frend user", "test@mail", "test_pwd")
        response = self.client.post(
            reverse("Hotel:share-order-room"),
            data={
                "permission": "view_orderroom",
                "user": frend_user.username,
                "object_pk": response.data['id'],
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # <QueryDict: {'permission': ['hotel.view_orderroom'], 'user': ['frend user'], 'object_pk': ['1']}>
        # multipart/form-data; boundary=BoUnDaRyStRiNg
        # {'permission': 'hotel.view_orderroom', 'user': 'frend user', 'object_pk': 1}
        # 'application/json'
        self.client.logout()
        self.client.force_login(frend_user)
        response = self.client.get(reverse("Hotel:list-ordered-room"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
