from django.contrib.auth.models import User

def login(client):
    user = User.objects.create(username='test')
    user.set_password('12345')
    user.save()
    client.login(username='test', password='12345')
