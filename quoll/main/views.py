from urllib.parse import urlparse
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse
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

@csrf_exempt
@require_http_methods(['POST', 'GET']) # only GET and POST
def crawl(request):
    if request.method == 'POST':
        url = request.POST.get('url', None)

        if not url:
            return JsonResponse({'error': 'Missing args'})
        if not is_valid_url(url):
            return JsonResponse({'error': 'URL is invalid'})

        domain = urlparse(url).netloc  # parse the url and extract the domain
        unique_id = str(uuid4())

        task = scrapyd.schedule('quoll-scrapy', 'indievox')

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