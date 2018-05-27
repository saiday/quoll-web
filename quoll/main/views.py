import json
from urllib.parse import urlparse
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from scrapyd_api import ScrapydAPI

# connect scrapyd service

scrapyd = ScrapydAPI('http://localhost:6800')


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        return False

    return True


def valid_site(site):
    valid_sites = ['indievox']
    if site in valid_sites:
        return True
    return False


@csrf_exempt
@require_http_methods(['POST', 'GET']) # only GET and POST
def crawl(request):
    if request.method == 'POST':
        site = request.POST.get('site', None)

        if not site:
            return HttpResponseBadRequest(json.dumps({'error': 'Missing site argument'}),
                                          content_type='application/json')
        if not valid_site(site):
            return HttpResponseBadRequest(json.dumps({'error': 'Unsupported site'}),
                                          content_type='application/json')
        unique_id = str(uuid4())
        settings = {'unique_id': unique_id}

        task = scrapyd.schedule('default', 'indievox', settings=settings)

        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started', })

    elif request.method == 'GET':
        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)

        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})

        status = scrapyd.job_status('quoll-scrapy', task_id)
        if status == 'finished':
            try:
                # item = ScrapyItem.objects.get(unique_id=unique_id)
                # return JsonResponse({'data': item.to_dict['data']})
                return JsonResponse({'success': 'waiting for implemented'})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})