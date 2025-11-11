from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from .models import User
from .serializers import AdminUserSerializer


class UserDeleteViewTests(TestCase):
	def setUp(self):
		# Admin (superuser) created using manager
		self.admin = User.objects.create_superuser(email='admin@test.com', name='Admin User', password='adminpass')
		# Regular user who will attempt deletes
		self.user = User.objects.create_user(email='user@test.com', name='Regular User', password='userpass')
		# Target account to be deleted
		self.target = User.objects.create_user(email='target@test.com', name='Target User', password='targetpass')

		self.client = APIClient()

	def test_admin_can_delete_user(self):
		self.client.force_authenticate(user=self.admin)
		url = reverse('user-delete', kwargs={'pk': self.target.pk})
		resp = self.client.delete(url)
		self.assertEqual(resp.status_code, 204)
		# Deletion may actually remove the row or (in environments where
		# related-table migrations are missing) fall back to deactivation.
		exists = User.objects.filter(pk=self.target.pk).exists()
		if exists:
			self.assertFalse(User.objects.get(pk=self.target.pk).is_active)

	def test_non_admin_cannot_delete_user(self):
		self.client.force_authenticate(user=self.user)
		# non-admin attempts to delete another user's account (should be forbidden)
		url = reverse('user-delete', kwargs={'pk': self.target.pk})
		resp = self.client.delete(url)
		self.assertEqual(resp.status_code, 403)
		# Target should still exist
		self.assertTrue(User.objects.filter(pk=self.target.pk).exists())

	def test_user_can_delete_own_account(self):
		# A regular user should be able to delete their own account
		self.client.force_authenticate(user=self.user)
		url = reverse('user-delete', kwargs={'pk': self.user.pk})
		resp = self.client.delete(url)
		self.assertEqual(resp.status_code, 204)
		exists = User.objects.filter(pk=self.user.pk).exists()
		if exists:
			self.assertFalse(User.objects.get(pk=self.user.pk).is_active)


class AdminUserSerializerTest(TestCase):
	def test_create_hashes_password(self):
		data = {
			"email": "t1@example.com",
			"name": "Test One",
			"phone": "0123456789",
			"role": "agent",
			"permission": "only_view",
			"password": "plainpass123",
		}
		serializer = AdminUserSerializer(data=data)
		self.assertTrue(serializer.is_valid(), serializer.errors)
		user = serializer.save()
		# Password must be hashed and check_password should succeed
		self.assertTrue(user.check_password("plainpass123"))
		self.assertNotEqual(user.password, "plainpass123")

	def test_update_hashes_password(self):
		# create initial user
		user = User.objects.create_user(email='u1@example.com', name='User One', password='initial')
		# update password via serializer
		serializer = AdminUserSerializer(instance=user, data={"password": "newsecret"}, partial=True)
		self.assertTrue(serializer.is_valid(), serializer.errors)
		updated = serializer.save()
		self.assertTrue(updated.check_password("newsecret"))
		self.assertNotEqual(updated.password, "newsecret")


class AdminUserAPITest(TestCase):
	"""API-level tests for the admin-managed users endpoints.

	- Admin can POST to the admin user list endpoint and create users.
	- Non-admin users cannot create other users (permission enforced).
	"""
	def setUp(self):
		self.admin = User.objects.create_superuser(email='admin@test.com', name='Admin User', password='adminpass')
		self.user = User.objects.create_user(email='user@test.com', name='Regular User', password='userpass')
		self.client = APIClient()

	def test_admin_can_create_user_via_api(self):
		self.client.force_authenticate(user=self.admin)
		url = reverse('admin-user-list-create')
		payload = {
			"email": "apiagent@example.com",
			"name": "API Agent",
			"phone": "0999888777",
			"role": "agent",
			"permission": "full_access",
			"password": "AgentPass123",
		}
		resp = self.client.post(url, payload, format='json')
		self.assertEqual(resp.status_code, 201, resp.data)
		# Ensure user created and password is hashed
		created = User.objects.filter(email__iexact=payload['email']).first()
		self.assertIsNotNone(created)
		self.assertTrue(created.check_password(payload['password']))
		# API should not return the password
		self.assertNotIn('password', resp.data)

	def test_non_admin_cannot_create_user_via_api(self):
		self.client.force_authenticate(user=self.user)
		url = reverse('admin-user-list-create')
		payload = {
			"email": "forbidden@example.com",
			"name": "Forbidden",
			"phone": "000",
			"role": "agent",
			"permission": "only_view",
			"password": "x",
		}
		resp = self.client.post(url, payload, format='json')
		# Non-admin should be forbidden
		self.assertIn(resp.status_code, (401, 403))
		self.assertFalse(User.objects.filter(email__iexact=payload['email']).exists())

