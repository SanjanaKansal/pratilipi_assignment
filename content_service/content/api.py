import json

from tastypie.resources import Resource
from tastypie.utils.urls import trailing_slash
from django.conf.urls import url
from django.http import HttpResponseNotAllowed
from content import dal, connector, exceptions

class ContentResource(Resource):
    class Meta:
        resource_name = 'content'

    def prepend_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('fetch_and_upload_content'),
                name="api_fetch_and_upload_content",
            ),
            url(
                r"^(?P<resource_name>%s)/series%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('fetch_series'),
                name="api_fetch_series",
            ),
            url(
                r"^(?P<resource_name>%s)/chapters%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('fetch_chapters'),
                name="api_fetch_chapters",
            )
        ]

    def fetch_and_upload_content(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.upload_content(request, *args, **kwargs)
        elif request.method == 'GET':
            return self.fetch_content(request, *args, **kwargs)
        return HttpResponseNotAllowed(request.method, 'Invalid Request Method')

    def upload_content(self, request, *args, **kwargs):
        data = json.loads(request.body)
        title = data.get('title')
        chapters = data.get('chapters')
        validation_err = self._validate_json_data(request, {'title': title, 'chapters': chapters})
        if validation_err:
            return validation_err
        dal.save_content(title, chapters)
        return self.create_response(request, {'success': True, 'message': 'Chapters successfully added to the series'})

    def fetch_content(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        if not user_id:
            content = dal.get_content()
            return self.create_response(request, {'content': content})
        response = connector.get_user_from_user_service(user_id)
        if response.get('error'):
            return self.error_response(request, {'success': False, 'error': response['error'], 'message': response['message']})
        content = dal.get_content_for_user(user_id)
        return self.create_response(request, {'success': True, 'content': content})

    def fetch_series(self, request, *args, **kwargs):
        title = request.GET.get('title')
        try:
            series = dal.get_series(title)
        except exceptions.SeriesDoesNotExistException as e:
            return self.error_response(request, {'error': e.error, 'message': e.message})
        return self.create_response(request, {'id': series.id, 'title': series.title})

    def fetch_chapters(self, request, *args, **kwargs):
        title = request.GET.get('title')
        chapters = dal.get_chapter_details(title)
        return self.create_response(request, {'chapters': chapters})

    def _validate_json_data(self, request, data):
        error_in_attrs = []
        for attr, val in data.items():
            if not val:
                error_in_attrs.append(attr)

        if error_in_attrs:
            return self.error_response(
                request,
                [
                    {
                        'error': 'no{}Present'.format(attr),
                        'message': 'No {} present'.format(attr)
                    }
                    for attr in error_in_attrs
                ]
            )