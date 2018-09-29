from django.views.generic import ListView, View
from django.http import HttpResponse
from .models import Table
from .api import Data
from django.shortcuts import render, redirect

# Create your views here.


class DataList(ListView):
    queryset = Table.objects.all()
    context_object_name = 'data'
    template_name = 'data.html'

    def post(self, request):
        data = Data()
        work_time = data.get_data()
        return render(request, self.template_name, {'work_time': work_time, 'data': self.queryset})


class Operations(View):
    data = Data()
    user_ids = []
    for oauth_token in data.OAUTH_TOKENS:
        SESSION = data.auth(oauth_token)
        user_id = data.get_user_id(SESSION)
        user_ids.append(user_id)

    def get(self, request):

        return render(request, 'operations.html', {'user_ids': self.user_ids})

    def post(self, request):

        user_id = request.POST.get('user-id')
        SESSION = self.data.auth(self.data.OAUTH_TOKENS[self.data.user_ids.index(int(user_id))])
        # action_type = request.POST.get('user-id')
        urls = self.data.get_urls(user_id, SESSION)

        return render(request, 'operations.html', {'user_ids': self.user_ids, 'urls': urls})


class OperationDelete(Operations):

    def get(self, request):

        return redirect('/webmaster_api/operations/')

    def post(self, request):
        delete_urls = request.POST.get('delete-text')
        delete_urls = delete_urls.replace('.ru', '.ru/')
        delete_urls = delete_urls.split('\r\n')
        user_id = request.POST.get('user-id')
        SESSION = self.data.auth(self.data.OAUTH_TOKENS[self.data.user_ids.index(int(user_id))])

        r = SESSION.get(self.data.API_URL + '/user/' + str(user_id) + '/hosts/')
        c = r.json()
        hosts = c['hosts']
        host_ids = []
        for host in hosts:
            if host['ascii_host_url'] in delete_urls:
                host_ids.append(host['host_id'])

        for host_id in host_ids:
            path = '/user/' + str(user_id) + '/hosts/' + host_id
            # todo: убрать заглушку для удаления сайтов
            # response = SESSION.delete(self.data.API_URL + path)
        return render(request, 'delete.html', {'delete_urls': host_ids})


class OperationAdd(Operations):

    def get(self, request):

        return redirect('/webmaster_api/operations/')

    def post(self, request):
        add_urls = request.POST.get('add-text')
        add_urls = add_urls.replace('.ru', '.ru/')
        add_urls = add_urls.split('\r\n')
        user_id = request.POST.get('user-id')
        SESSION = self.data.auth(self.data.OAUTH_TOKENS[self.data.user_ids.index(int(user_id))])

        for url in add_urls:
            path = '/user/' + str(user_id) + '/hosts/'
            # todo: убрать заглушку для добавления сайтов
            # response = SESSION.post(self.data.API_URL + path, json={"host_url": url})

        return render(request, 'add.html', {'add_urls': add_urls})
