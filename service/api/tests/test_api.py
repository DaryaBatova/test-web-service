from unittest.mock import patch, Mock
from django.test import TestCase
from django.urls import reverse
import json
from copy import deepcopy

from api.models import Page
from api.serializers import PageSerializer
from api.process_url import parse_content_data, process_url


class PageSerializerTest(TestCase):
    """
    Testing the correctness of serialization and deserialization processes.
    """

    test_data = {'h1': 1, 'h2': 1, 'h3': 1, 'a': 'http://google.com, http://yandex.ru'}

    def test_data_serialization_is_correct(self):
        page = Page.objects.create(**self.test_data)
        serializer = PageSerializer(page)
        serialization_data = {'h1': 1, 'h2': 1, 'h3': 1, 'a': ['http://google.com', 'http://yandex.ru']}
        serialization_data['page_id'] = page.pk
        self.assertEqual(serializer.data, serialization_data)

    def test_data_serialization_is_correct_if_a_empty(self):
        data = deepcopy(self.test_data)
        data['a'] = ''
        page = Page.objects.create(**data)
        serializer = PageSerializer(page)
        serialization_data = {'h1': 1, 'h2': 1, 'h3': 1, 'a': []}
        serialization_data['page_id'] = page.pk
        self.assertEqual(serializer.data, serialization_data)

    def test_data_deserialization_is_correct(self):
        serializer = PageSerializer(data=self.test_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})
        page = serializer.save()
        self.assertEqual(Page.objects.count(), 1)
        self.assertEqual(page.h1, 1)
        self.assertEqual(page.h2, 1)
        self.assertEqual(page.h3, 1)
        self.assertEqual(page.a, 'http://google.com, http://yandex.ru')

    def test_data_deserialization_is_correct_if_a_empty(self):
        data = deepcopy(self.test_data)
        data['a'] = ''
        serializer = PageSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})
        page = serializer.save()
        self.assertEqual(Page.objects.count(), 1)
        self.assertEqual(page.h1, 1)
        self.assertEqual(page.h2, 1)
        self.assertEqual(page.h3, 1)
        self.assertEqual(page.a, '')

    def test_data_deserialization_is_correct_when_parsing(self):
        test_content = '<h1>True</h1><h2></h2><h3></h3><a href="http://google.com"><a href="#">'
        detail_page = parse_content_data(test_content)
        serializer = PageSerializer(data=detail_page)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})
        page = serializer.save()
        self.assertEqual(page.a, 'http://google.com, #')


class PageCreateTest(TestCase):
    """
    Testing the correctness of the formation of responses to POST requests.

    Basic test cases:
    - correct POST request
    - incorrect POST request with empty parameters
    - incorrect POST request with wrong parameters (no parameter 'url')
    - correct POST request, but having problems with the request to the page with the passed parameter 'url'
    - correct POST request with a parameter 'url' that has already been processed earlier
    """

    test_data = {'h1': 1, 'h2': 1, 'h3': 1, 'a': 'http://google.com'}
    test_url = 'http://google.com'

    def test_post_request_with_correct_url_and_without_url_connection_problems(self):
        with patch('requests.get') as mock_request_get:
            mock_result = mock_request_get.return_value
            mock_result.raise_for_status.return_value = None
            with patch('api.process_url.parse_content_data', return_value=self.test_data):
                response = self.client.post(reverse('create_page_detail'), data={'url': self.test_url})
                self.assertEqual(response.status_code, 201)
                self.assertEqual(Page.objects.count(), 1)
                response_body = json.loads(response.content.decode('utf8'))
                self.assertEqual(response_body, {'page_id': 1, 'h1': 1, 'h2': 1, 'h3': 1, 'a': ['http://google.com']})
                page = Page.objects.get(pk=1)
                self.assertEqual(page.url, self.test_url)

    def test_post_request_with_empty_params(self):
        response = self.client.post(reverse('create_page_detail'), data={})
        self.assertEqual(response.status_code, 400)
        response_body = json.loads(response.content.decode('utf8'))
        self.assertEqual(response_body['detail'], "Invalid parameters: {}. Expected: {'url': 'some_url'}")

    def test_post_request_with_wrong_params(self):
        response = self.client.post(reverse('create_page_detail'), data={'bad': 'value'})
        self.assertEqual(response.status_code, 400)
        response_body = json.loads(response.content.decode('utf8'))
        self.assertEqual(response_body['detail'],
                         "Invalid parameters: {'bad': ['value']}. Expected: {'url': 'some_url'}")

    def test_post_request_with_url_connection_problems(self):
        import requests
        with patch('requests.get') as mock_request_get:
            mock_result = mock_request_get.return_value
            mock_result.raise_for_status.side_effect = Mock(side_effect=requests.RequestException())
            response = self.client.post(reverse('create_page_detail'), data={'url': self.test_url})
            self.assertEqual(response.status_code, 400)
            response_body = json.loads(response.content.decode('utf8'))
            self.assertEqual(response_body['detail'],
                             f'An error occurred while trying to establish a connection with {self.test_url}')

    def test_post_request_with_already_occurring_url(self):
        page = Page.objects.create(url=self.test_url, h1=2, h2=2, h3=4, a='')
        self.assertEqual(Page.objects.count(), 1)
        with patch('requests.get') as mock_request_get:
            mock_result = mock_request_get.return_value
            mock_result.raise_for_status.return_value = None
            with patch('api.process_url.parse_content_data', return_value=self.test_data):
                response = self.client.post(reverse('create_page_detail'), data={'url': self.test_url})
                self.assertEqual(response.status_code, 201)
                self.assertEqual(Page.objects.count(), 1)
                response_body = json.loads(response.content.decode('utf8'))
                self.assertEqual(response_body, {'page_id': 1, 'h1': 1, 'h2': 1, 'h3': 1, 'a': ['http://google.com']})
                self.assertEqual(page.url, self.test_url)


class PageGetTest(TestCase):
    """
    Testing the correctness of the formation of responses to GET requests.

    Basic test cases:
    - correct GET request for an existing page
    - correct GET request for a non-existent page
    """

    test_data = {'h1': 1, 'h2': 1, 'h3': 1, 'a': 'http://google.com'}

    def test_get_request_exists_page(self):
        page = Page.objects.create(**self.test_data)
        response = self.client.get(reverse('get_page_detail', kwargs={'pk': page.pk}))
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content.decode('utf8'))
        self.assertEqual(response_body, {'page_id': 1, 'h1': 1, 'h2': 1, 'h3': 1, 'a': ['http://google.com']})

    def test_get_request_nonexistent_page(self):
        response = self.client.get(reverse('get_page_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)

