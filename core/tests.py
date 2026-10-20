
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import CalendarEvent


class CalendarEventTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="student1",
            password="TestPassword123!"
        )
        self.other_user = User.objects.create_user(
            username="student2",
            password="TestPassword123!"
        )

        self.start = timezone.now() + timedelta(days=1)
        self.end = self.start + timedelta(hours=2)

        self.event = CalendarEvent.objects.create(
            student=self.user,
            title="Study for CS408",
            event_type="academic",
            starts_at=self.start,
            ends_at=self.end,
            notes="Review Django",
        )

    def test_calendar_requires_login(self):
        response = self.client.get(reverse("calendar"))
        self.assertEqual(response.status_code, 302)

    def test_calendar_displays_own_events(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("calendar"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Study for CS408")

    def test_calendar_hides_other_students_events(self):
        self.client.force_login(self.other_user)

        response = self.client.get(reverse("calendar"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Study for CS408")

    def test_add_event(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("calendar_add"), {
            "title": "New Assignment",
            "event_type": "academic",
            "starts_at": "2026-10-22T10:00",
            "ends_at": "2026-10-23T11:00",
            "notes": "Finish assignment",
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            CalendarEvent.objects.filter(
                student=self.user,
                title="New Assignment"
            ).exists()
        )

    def test_edit_event(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("calendar_edit", args=[self.event.id]),
            {
                "title": "Updated Study Session",
                "event_type": "academic",
                "starts_at": "2026-10-22T10:00",
                "ends_at": "2026-10-23T11:00",
                "notes": "Updated notes",
            }
        )

        self.assertEqual(response.status_code, 302)

        self.event.refresh_from_db()
        self.assertEqual(
            self.event.title,
            "Updated Study Session"
        )

    def test_cannot_edit_another_students_event(self):
        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse("calendar_edit", args=[self.event.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_event(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("calendar_delete", args=[self.event.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            CalendarEvent.objects.filter(
                id=self.event.id
            ).exists()
        )

    def test_cannot_delete_another_students_event(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse("calendar_delete", args=[self.event.id])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            CalendarEvent.objects.filter(
                id=self.event.id
            ).exists()
        )

    def test_delete_requires_post(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("calendar_delete", args=[self.event.id])
        )

        self.assertEqual(response.status_code, 405)
