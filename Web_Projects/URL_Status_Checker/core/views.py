import ast
import json
import grequests

from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from core.utils.helpers import async_url_response


class BaseIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'URL Status Checker'
        context['user_urls'] = self.request.user.urls.all()
        context['urls_to_be_checked'] = json.dumps(list(self.request.user.urls.values_list('url', flat=True)))

        return context


@csrf_exempt
@login_required
def check_urls_status(request):
    if request.method == "POST" and request.is_ajax():
        urls_list = ast.literal_eval(request.POST.get('urls'))
        timeout = int(request.POST.get('timeout', 0))

        response = grequests.map(async_url_response(urls_list, timeout))

        result = []

        # Check whether the response is returned by grequest or not
        # If not, then the url is not a valid url and will be added with the status code of 400
        for idx, res in enumerate(response):
            if res is not None:
                result.append([res.url, res.status_code])
            else:
                result.append([urls_list[idx], 400])

        return JsonResponse({'status': 'ok', 'response': result})

    return JsonResponse({'response': 'error'}, status=404)
