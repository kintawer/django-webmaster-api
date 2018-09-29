from .models import Table

# context = [{'domain': 'domain',
#             'fatal': 'fatal',
#             'critical': 'critical',
#             'possible_problem': 'possible_problem',
#             'recommendation': 'recommendation',
#             'sitemap_date': 'sitemap_date',
#             'sitemap_url_count': 'sitemap_url_count',
#             'searchable_date': 'searchable_date',
#             'searchable_count': 'searchable_count'
#             }]

# def insert_to_db(context):
#     for item in context:
#         Table.objects.create(domain=item['domain'],
#                              fatal=item['fatal'],
#                              critical=item['critical'],
#                              possible_problem=item['possible_problem'],
#                              recommendation=item['recommendation'],
#                              sitemap_date=item['sitemap_date'],
#                              sitemap_url_count=item['sitemap_url_count'],
#                              searchable_date=item['searchable_date'],
#                              searchable_count=item['searchable_count'])
