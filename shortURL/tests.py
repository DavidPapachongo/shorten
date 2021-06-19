from django.http import response
from rest_framework.test import APITestCase
from shortURL.models import UrlModel, ClickModel
import json
header = {'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}


class AccountLink(APITestCase):

    def test_create_link(self):
        request_data = {
            'link': 'http://localhost'
        }
        response = self.client.post('/link/', request_data, format='json')
        assert response.status_code == 201
        data = json.loads(response.content)
        assert data.get('link') == 'http://localhost'
        assert data.get('id') is not None


    def test_try_create_link_with_empty_string(self):
        request_data = {
            'link': ''
        }
        response = self.client.post('/link/', request_data, format='json')
        assert response.status_code == 400
        data = json.loads(response.content)
        assert data["link"] == ['This field may not be blank.']


    def test_try_create_link_with_wrong_string(self):
        request_data = {
            'link': 'la casita en el arbol (◕ᴗ◕✿)'
        }
        response = self.client.post('/link/', request_data, format='json')
        assert response.status_code == 400
        data = json.loads(response.content)
        assert data["link"] == ['Enter a valid URL.']
        
class AccountLinkDetail(APITestCase):

    def test_get_link_by_id(self):
        link = UrlModel.objects.create(**{
            'link': 'http://localhost'
        })
        
        response = self.client.get('/link/{}/'.format(link.id), format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["id"] == link.id
        assert data["link"] == link.link
        assert data["clicks_counter"] == 0


    def test_get_link_by_id_after_redirect(self):
        link = UrlModel.objects.create(**{
            'link': 'http://localhost'
        })

        response = self.client.get(link.shorten_link(), format='json', **header)
        response = self.client.get('/link/{}/'.format(link.id), format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["id"] == link.id
        assert data["link"] == link.link
        assert data["clicks_counter"] == 1 


    def test_try_get_not_existent_link_by_id(self):
        response = self.client.get('/link/-1/', format='json')
        assert response.status_code == 404


    def test_delete_link_by_id(self):
        link = UrlModel.objects.create(**{
            'link': 'http://localhost'
        })
        response = self.client.get('/link/{}/'.format(link.id), format='json')
        assert response.status_code == 200

        response = self.client.delete('/link/{}/'.format(link.id), format='json')
        assert response.status_code == 204

        response = self.client.get('/link/{}/'.format(link.id), format='json')
        assert response.status_code == 404
        

    def test_put_link_by_id(self):
        link = UrlModel.objects.create(**{
            'link': 'http://localhost'
        })

        response = self.client.get('/link/{}/'.format(link.id), format='json')
        assert response.status_code == 200

        request_data = {
            'link': 'https://www.youtube.com/watch?v=3CgpG4GuZZ8&t=11s'
        }
        response = self.client.put('/link/{}/'.format(link.id),request_data, format='json')
        data = json.loads(response.content)
        assert response.status_code == 200
        assert data["link"] != link.link
        assert data["id"] == link.id
        assert data["link"] == 'https://www.youtube.com/watch?v=3CgpG4GuZZ8&t=11s'

class AccountRedirect(APITestCase):

    def test_redirect_url_by_id(self):
        link = UrlModel.objects.create(**{
            'link': 'http://localhost'
        })

        response = self.client.get(link.shorten_link(), format='json', **header)
        response = self.client.get(link.shorten_link(), format='json', **header)
        assert response.status_code == 302
        assert response.url == link.link

        clicks = ClickModel.objects.filter(url_id=link.id)
        assert len(clicks) == 2
        assert clicks[0].url_id  == link.id 


    def test_try_redirect_url_by_non_existent_id(self):
        response = self.client.get('/link/redirect/-1/', format='json')
        assert response.status_code == 404 


    def test_try_redirect_without_header(self):
        link = UrlModel.objects.create(**{
            'link': 'http://localhost'
        })
        response = self.client.get(link.shorten_link(), format='json' )
        assert response.status_code == 302 

        
class AccountClicks(APITestCase):
    
    def test_list_clicks(self):
        link = UrlModel.objects.create(**{
            'link': 'http://localhost'
        })

        response = self.client.get(link.shorten_link(),format='json',**header)
        response = self.client.get(link.shorten_link(),format='json',**header)
        response = self.client.get(link.shorten_link(),format='json',**header)
        assert response.status_code == 302

        response = self.client.get('/link/clicksList/', format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data) == 3

class AccountLinkClicks(APITestCase):
    def test_clicks_by_link_id(self):
        link = UrlModel.objects.create(**{
            'link': 'http://localhost'
        })

        link_2 = UrlModel.objects.create(**{
            'link': 'http://localhost'
        })

        response = self.client.get(link_2.shorten_link(), format='json',**header)
        response = self.client.get(link_2.shorten_link(), format='json',**header)
        response = self.client.get(link_2.shorten_link(), format='json',**header)
        response = self.client.get(link.shorten_link(), format='json',**header)
        assert response.status_code == 302
        
        response = self.client.get('/link/clicks/',{'link_id': '{}'.format(link_2.id)}, format='json')
        assert response.status_code == 200

        data = json.loads(response.content)
        for click in data:
            assert click["url_id"] == link_2.id

        
    def test_try_clicks_by_not_exist_link_id(self):
        link = UrlModel.objects.create(**{
            'link': 'http://localhost'
        })

        link_2 = UrlModel.objects.create(**{
            'link': 'http://localhost'
        })

        response = self.client.get(link_2.shorten_link(), format='json',**header)
        response = self.client.get(link_2.shorten_link(), format='json',**header)
        response = self.client.get(link_2.shorten_link(), format='json',**header)
        response = self.client.get(link.shorten_link(), format='json',**header)
        assert response.status_code == 302
        
        response = self.client.get('/link/clicks/',{'link_id': -1}, format='json')
        assert response.status_code == 200

        data = json.loads(response.content)
        assert data == []

class AccountUserAgent(APITestCase):
    def test_regular_user_agent(self):
        header = {'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

        link = UrlModel.objects.create(**{
            'link': 'http://localhost'
        })

        response = self.client.get(link.shorten_link(), format='json',**header)
        assert response.status_code == 302

        response = self.client.get('/link/clicks/',{'link_id': '{}'.format(link.id)}, format='json')
        assert response.status_code == 200

        data = json.loads(response.content)
        assert data[0]['user_agent'] == header['HTTP_USER_AGENT']
        assert data[0]['browser'] == 'Chrome'
    

    def test_try_empty_user_agent_string(self):
        header = {'HTTP_USER_AGENT': ''}

        link = UrlModel.objects.create(**{
            'link': 'http://localhost'
        })

        response = self.client.get(link.shorten_link(), format='json',**header)
        assert response.status_code == 302

        response = self.client.get('/link/clicks/',{'link_id': '{}'.format(link.id)}, format='json')
        assert response.status_code == 200

        data = json.loads(response.content)
        assert data[0]['user_agent'] == ''
        assert data[0]['browser'] == None

    def test_try_null_user_agent(self):
        header = {'HTTP_USER_AGENT': None}

        link = UrlModel.objects.create(**{
            'link': 'http://localhost'
        })

        response = self.client.get(link.shorten_link(), format='json',**header)
        assert response.status_code == 302

        response = self.client.get('/link/clicks/',{'link_id': '{}'.format(link.id)}, format='json')
        assert response.status_code == 200

        data = json.loads(response.content)
        assert data[0]['user_agent'] == None
        assert data[0]['browser'] == None
        

        
      




