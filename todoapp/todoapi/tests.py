from django.test import TestCase
from .models import TodoItem 
from rest_framework import test, status
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

class ApiTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='Dan')
        self.user2 = User.objects.create(username='Daniel')

        self.client1 = test.APIClient()
        self.client1.force_authenticate(user=self.user1)
        self.client2 = test.APIClient()
        self.client2.force_authenticate(user=self.user2)

        self.item_to_complete = TodoItem(title='Test item for marking as complete', owner=self.user1)
        self.item_to_complete.save()
        self.item_to_edit = TodoItem(title='Test item for editing', owner=self.user1)
        self.item_to_edit.save()
        self.item_to_delete = TodoItem(title='Test item for deleting', owner=self.user1)
        self.item_to_delete.save()
        

    def test_api_list_authorization(self):

        res = self.client2.get(
            reverse('listitems')
        )
        print(len(res.data))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_authentication(self):
        unauthenticated_client = test.APIClient()
        res = unauthenticated_client.get(
            reverse('listitems')
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_item_creation(self):
        before_count = TodoItem.objects.count()
        res = self.client1.post(
            reverse('createitem'),
            {'title': 'Add a todo item through the API', 'user': self.user1.id}
        )
        after_count = TodoItem.objects.count()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(before_count + 1,after_count)
    
    def test_api_mark_complete(self):
        before_status = TodoItem.objects.get(pk=self.item_to_complete.id).complete
        res = self.client1.put(
            reverse('edit', kwargs={'pk': self.item_to_complete.id}),
            {'title': self.item_to_complete.title, 'complete':True}
        )
        after_status = TodoItem.objects.get(pk=self.item_to_complete.id).complete
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(before_status,False)
        self.assertEqual(after_status,True)

    def test_api_edit_authorization(self):
        title_before = TodoItem.objects.get(pk=self.item_to_complete.id).title
        res = self.client2.put(
            reverse('edit', kwargs={'pk': self.item_to_edit.id}),
            {'title': 'New Title'}
        )
        title_after = TodoItem.objects.get(pk=self.item_to_complete.id).title
        self.assertEqual(title_before,title_after)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_api_delete_authorization(self):
        before_count = TodoItem.objects.count()
        res = self.client2.delete(
            reverse('edit', kwargs={'pk': self.item_to_delete.id}),
            follow=True
        )
        after_count = TodoItem.objects.count()
        self.assertEqual(res.status_code,status.HTTP_403_FORBIDDEN)
        self.assertEqual(before_count, after_count)

    def test_api_deletion(self):
        before_count = TodoItem.objects.count()
        res = self.client1.delete(
            reverse('edit', kwargs={'pk': self.item_to_delete.id}),
            follow=True
        )
        after_count = TodoItem.objects.count()
        self.assertEqual(res.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count - 1, after_count)