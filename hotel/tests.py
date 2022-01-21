from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup
from rest_framework import status
from datetime import date
from hotel.models import Room, OrderRoom
from django.contrib.auth.models import User

# hello
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
# Create your tests here.
