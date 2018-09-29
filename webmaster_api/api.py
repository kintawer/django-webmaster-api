import json
import requests
from dateutil import parser
from .models import Table
import time
from threading import Thread


class Data:

    def __init__(self):
        self.OAUTH_TOKENS = ['OAUTH_TOKEN_1', 'OAUTH_TOKEN_2']
        self.API_URL = 'https://api.webmaster.yandex.net/v3.1'
        self.user_ids = []

        for OAUTH_TOKEN in self.OAUTH_TOKENS:
            SESSION = self.auth(OAUTH_TOKEN)
            self.user_ids.append(self.get_user_id(SESSION))

    def auth(self, OAUTH_TOKEN):
        """
        Auth for SESSION with oauth_token
        :param OAUTH_TOKEN: access token
        :return: SESSION with AUTH_HEADER with oauth_token
        """
        AUTH_HEADER = {
            'Authorization': 'OAuth %s' % OAUTH_TOKEN
        }
        SESSION = requests.Session()
        SESSION.headers.update(AUTH_HEADER)
        return SESSION

    def get_user_id(self, SESSION):
        """
        Return user_id on SESSION
        :param SESSION: with oath_token
        :return:
        """
        r = SESSION.get(self.API_URL + '/user/')
        c = json.loads(r.text)
        return c['user_id']

    def get_urls(self, user_id, SESSION):
        """
        Return list of urls on user_id
        :param user_id: before use it, get user_id
        :param SESSION: with oath_token
        :return:
        """
        r = SESSION.get(self.API_URL + '/user/' + str(user_id) + '/hosts/')
        c = r.json()
        hosts = c['hosts']
        urls = []
        for host in hosts:
            urls.append(host['ascii_host_url'])
        return urls

    def get_host_ids(self, user_id, SESSION):
        """
        Return list of host_ids
        :param user_id: before use it, get user_id
        :param SESSION: with oath_token
        :return:
        """
        r = SESSION.get(self.API_URL + '/user/' + str(user_id) + '/hosts/')
        c = r.json()
        hosts = c['hosts']
        host_ids = []
        for host in hosts:
            host_ids.append(host['host_id'])

        return host_ids

    def get_problems(self, user_id, host_id, SESSION, info):
        """
        Get problems on sites
        :param user_id: get_user_id()
        :param host_id: get_host_ids()
        :param SESSION: with oath_token
        :return: dict {'NAME_PROBLEM': 'int(count)'}
        """
        def count_problem(content, problem_name):
            try:
                site_problems = content['site_problems']
                count = site_problems[problem_name]
            except:
                count = 0
            return count

        path = '/user/' + str(user_id) + '/hosts/' + host_id + '/summary/'
        response = SESSION.get(self.API_URL + path)
        content = response.json()
        fatal = count_problem(content, 'FATAL')
        critical = count_problem(content, 'CRITICAL')
        possible_problem = count_problem(content, 'POSSIBLE_PROBLEM')
        recommendation = count_problem(content, 'RECOMMENDATION')
        problems = {'FATAL': fatal, 'CRITICAL': critical,
                    'POSSIBLE_PROBLEM': possible_problem, 'RECOMMENDATION': recommendation}
        info['FATAL'] = fatal
        info['CRITICAL'] = critical
        info['POSSIBLE_PROBLEM'] = possible_problem
        info['RECOMMENDATION'] = recommendation
        return print('get_problems')

    def get_sitemap(self, user_id, host_id, SESSION, info):
        '''
        Get sitemap_date and url_count
        :param user_id: get_user_id()
        :param host_id: get_host_ids()
        :param SESSION: with oath_token
        :return: sitemap_date, url_count
        '''
        path = '/user/' + str(user_id) + '/hosts/' + host_id + '/sitemaps/'
        response = SESSION.get(self.API_URL + path)
        content = json.loads(response.text)

        sitemap_date = None
        sitemap_url_count = 0
        for sitemap in content['sitemaps']:
            if 'sitemap.xml' in sitemap['sitemap_url']:
                sitemap_date = sitemap['last_access_date']
                if sitemap_date is not None:
                    sitemap_date = parser.parse(sitemap_date)
                    # sitemap_date = sitemap_date.strftime("%Y-%m-%d %H:%M")
                sitemap_url_count = sitemap['urls_count']
                # print("Последняя дата проверки sitemap: " + sitemap_date[:10])
                break
        info['sitemap_date'] = sitemap_date
        info['sitemap_url_count'] = sitemap_url_count
        return print('get_sitemap')

    def get_searchable(self, user_id, host_id, SESSION, info):
        '''
        Get date searchable check and count url
        :param user_id: get_user_id()
        :param host_id: get_host_ids()
        :param SESSION: with oath_token
        :return: searchable_date, searchable_count
        '''
        path = '/user/' + str(user_id) + "/hosts/" + host_id + "/indexing-history/?indexing_indicator=SEARCHABLE"
        response = SESSION.get(self.API_URL + path)
        content = response.json()
        position = len(content['indicators']['SEARCHABLE']) - 1
        info1 = content['indicators']['SEARCHABLE'][position]
        searchable_date = info1['date']
        searchable_date = parser.parse(searchable_date)
        # searchable_date = searchable_date.strftime("%Y-%m-%d %H:%M")
        searchable_count = info1['value']
        info['searchable_date'] = searchable_date
        info['searchable_count'] = searchable_count
        return print('get_searchable')

    def get_data(self):
        start_time = time.time()
        for OAUTH_TOKEN in self.OAUTH_TOKENS:

            SESSION = self.auth(OAUTH_TOKEN)
            user_id = self.get_user_id(SESSION)
            host_ids = self.get_host_ids(user_id, SESSION)  # https:abakan.rozarioflowers.ru:443

            # test
            # host_ids = []
            #
            # with open('test.txt', 'r') as f:
            #     for line in f:
            #         host_ids.append(line.strip())

            for host_id in host_ids:
                domain = host_id[6:].split('.')[0]

                info = {}
                # Get full information about domain with 3 threads
                t1 = Thread(target=self.get_problems, args=(user_id, host_id, SESSION, info))
                t2 = Thread(target=self.get_sitemap, args=(user_id, host_id, SESSION, info))
                t3 = Thread(target=self.get_searchable, args=(user_id, host_id, SESSION, info))

                t1.start()
                t2.start()
                t3.start()

                t1.join()
                t2.join()
                t3.join()

                try:
                    table = Table.objects.get(domain=domain)
                except Table.DoesNotExist:
                    table = None

                # update or create domain entry
                if table is None:
                    Table.objects.create(
                        domain=domain,
                        fatal=info['FATAL'],
                        critical=info['CRITICAL'],
                        possible_problem=info['POSSIBLE_PROBLEM'],
                        recommendation=info['RECOMMENDATION'],
                        sitemap_date=info['sitemap_date'],
                        sitemap_url_count=info['sitemap_url_count'],
                        searchable_date=info['searchable_date'],
                        searchable_count=info['searchable_count'])
                else:
                    table.fatal=info['FATAL']
                    table.critical=info['CRITICAL']
                    table.possible_problem=info['POSSIBLE_PROBLEM']
                    table.recommendation=info['RECOMMENDATION']
                    table.sitemap_date=info['sitemap_date']
                    table.sitemap_url_count=info['sitemap_url_count']
                    table.searchable_date=info['searchable_date']
                    table.searchable_count=info['searchable_count']
                    table.save()

        return 'time complete: ', str(time.time() - start_time)