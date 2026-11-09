from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import StudySessionForm
from .models import CalendarEvent, StudySession


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

class StudySessionModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            password='TestPassword123!'
        )

    def test_create_study_session(self):
        session = StudySession.objects.create(
            student=self.user,
            subject='CS408',
            study_date=date(2026, 11, 2),
            duration_minutes=60,
            notes='Worked on Campus Compass'
        )

        self.assertEqual(session.subject, 'CS408')
        self.assertEqual(session.duration_minutes, 60)
        self.assertEqual(session.student, self.user)

    def test_invalid_duration(self):
        form = StudySessionForm(data={
            'subject': 'CS408',
            'study_date': '2026-11-02',
            'duration_minutes': 0,
            'notes': ''
        })

        self.assertFalse(form.is_valid())


class StudySessionViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='student1',
            password='TestPassword123!'
        )
        self.other_user = User.objects.create_user(
            username='student2',
            password='TestPassword123!'
        )

        self.client.force_login(self.user)

        self.session = StudySession.objects.create(
            student=self.user,
            subject='CS408',
            study_date=timezone.localdate(),
            duration_minutes=60
        )

    def test_study_log_page_loads(self):
        response = self.client.get(reverse('study'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CS408')

    def test_add_study_session(self):
        response = self.client.post(reverse('study_add'), {
            'subject': 'CS354',
            'study_date': '2026-11-02',
            'duration_minutes': 45,
            'notes': 'Studied interpreters'
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            StudySession.objects.filter(
                student=self.user,
                subject='CS354'
            ).exists()
        )

    def test_edit_study_session(self):
        response = self.client.post(
            reverse('study_edit', args=[self.session.id]),
            {
                'subject': 'CS408',
                'study_date': '2026-11-02',
                'duration_minutes': 90,
                'notes': 'Updated session'
            }
        )

        self.assertEqual(response.status_code, 302)
        self.session.refresh_from_db()
        self.assertEqual(self.session.duration_minutes, 90)

    def test_delete_study_session(self):
        response = self.client.post(
            reverse('study_delete', args=[self.session.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            StudySession.objects.filter(
                id=self.session.id
            ).exists()
        )

    def test_cannot_edit_another_students_session(self):
        other_session = StudySession.objects.create(
            student=self.other_user,
            subject='Private Study Session',
            study_date=date(2026, 11, 2),
            duration_minutes=30
        )

        response = self.client.get(
            reverse('study_edit', args=[other_session.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_weekly_total(self):
        today = timezone.localdate()
        monday = today - timedelta(days=today.weekday())

        self.session.study_date = monday
        self.session.save()

        StudySession.objects.create(
            student=self.user,
            subject='CS354',
            study_date=monday,
            duration_minutes=30
        )

        response = self.client.get(reverse('study'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['weekly_minutes'],
            90
        )
        self.assertEqual(
            response.context['weekly_hours'],
            1.5
        )

from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Expense


class BudgetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='budgetuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otherbudgetuser',
            password='testpass123'
        )
        self.client.force_login(self.user)

    def test_budget_page_loads(self):
        response = self.client.get(reverse('budget'))
        self.assertEqual(response.status_code, 200)

    def test_add_expense(self):
        response = self.client.post(reverse('budget_add'), {
            'amount': '25.50',
            'category': 'Food',
            'expense_date': '2026-11-08',
            'description': 'Groceries',
        })

        self.assertRedirects(response, reverse('budget'))
        self.assertTrue(
            Expense.objects.filter(
                student=self.user,
                amount=Decimal('25.50')
            ).exists()
        )

    def test_edit_expense(self):
        expense = Expense.objects.create(
            student=self.user,
            amount=Decimal('25.50'),
            category='Food',
            expense_date=date(2026, 11, 8),
            description='Groceries'
        )

        response = self.client.post(
            reverse('budget_edit', args=[expense.id]),
            {
                'amount': '30.00',
                'category': 'Food',
                'expense_date': '2026-11-08',
                'description': 'Groceries',
            }
        )

        self.assertRedirects(response, reverse('budget'))
        expense.refresh_from_db()
        self.assertEqual(expense.amount, Decimal('30.00'))

    def test_delete_expense(self):
        expense = Expense.objects.create(
            student=self.user,
            amount=Decimal('25.50'),
            category='Food',
            expense_date=date(2026, 11, 8),
            description='Groceries'
        )

        response = self.client.post(
            reverse('budget_delete', args=[expense.id])
        )

        self.assertRedirects(response, reverse('budget'))
        self.assertFalse(
            Expense.objects.filter(id=expense.id).exists()
        )

    def test_monthly_and_category_totals(self):
        Expense.objects.create(
            student=self.user,
            amount=Decimal('25.50'),
            category='Food',
            expense_date=date(2026, 11, 8),
            description='Groceries'
        )
        Expense.objects.create(
            student=self.user,
            amount=Decimal('10.00'),
            category='Food',
            expense_date=date(2026, 11, 9),
            description='Lunch'
        )

        response = self.client.get(reverse('budget'))

        self.assertEqual(
            response.context['total'],
            Decimal('35.50')
        )
        self.assertEqual(
            list(response.context['monthly_totals'])[0]['total'],
            Decimal('35.50')
        )
        self.assertEqual(
            list(response.context['category_totals'])[0]['total'],
            Decimal('35.50')
        )

    def test_cannot_edit_another_users_expense(self):
        expense = Expense.objects.create(
            student=self.other_user,
            amount=Decimal('50.00'),
            category='Other',
            expense_date=date(2026, 11, 8),
            description='Private expense'
        )

        response = self.client.get(
            reverse('budget_edit', args=[expense.id])
        )
        self.assertEqual(response.status_code, 404)

    def test_cannot_delete_another_users_expense(self):
        expense = Expense.objects.create(
            student=self.other_user,
            amount=Decimal('50.00'),
            category='Other',
            expense_date=date(2026, 11, 8),
            description='Private expense'
        )

        response = self.client.post(
            reverse('budget_delete', args=[expense.id])
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Expense.objects.filter(id=expense.id).exists()
        )

    def test_other_users_expenses_are_hidden(self):
        Expense.objects.create(
            student=self.other_user,
            amount=Decimal('50.00'),
            category='Other',
            expense_date=date(2026, 11, 8),
            description='Private expense'
        )

        response = self.client.get(reverse('budget'))

        self.assertEqual(
            response.context['total'],
            Decimal('0.00')
        )
        self.assertEqual(
            len(response.context['expenses']),
            0
        )
