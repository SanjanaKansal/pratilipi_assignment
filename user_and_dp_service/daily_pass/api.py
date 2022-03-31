import json

from tastypie.resources import Resource
from tastypie.utils.urls import trailing_slash
from django.conf.urls import url
from django.http import HttpResponseNotAllowed

from daily_pass import dal, connector
from daily_pass.exceptions import NoLockedChapterException


from user import dal as user_dal
from user.exceptions import UserDoesNotExistException


class DailyPassResource(Resource):
    class Meta:
        resource_name = 'daily_pass'

    def prepend_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('fetch_and_unlock_chapter'),
                name="api_unlock_chapter",
            )
        ]

    def fetch_and_unlock_chapter(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.get_unlocked_chapters(request, *args, **kwargs)
        elif request.method == 'POST':
            return self.unlock_chapter(request, *args, **kwargs)
        return HttpResponseNotAllowed(request.method, 'Invalid Request Method')

    def unlock_chapter(self, request, *args, **kwargs):
        data = json.loads(request.body)
        title = data.get('title')
        user_id = request.GET.get('user_id')
        validation_err = self._validate_json_data(request, {'title': title})
        if validation_err:
            return validation_err

        response = connector.get_series_from_content_service(title)
        if response.get('error'):
            return self.error_response(request, {'error': response['error'], 'message': response['message']})

        try:
            user_dal.get_user(user_id)
        except UserDoesNotExistException as e:
            return self.error_response(request, {'error': e.error, 'message': e.message})

        try:
            chapter = dal.unlock_chapter(user_id, title)
        except NoLockedChapterException as e:
            return self.error_response(request, {'error': e.error, 'message': e.message})
        return self.create_response(
            request,
            {
                'success': True,
                'message': 'New Chapter unlocked',
                'chapter': chapter
            }
        )

    def get_unlocked_chapters(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        try:
            user_dal.get_user(user_id)
        except UserDoesNotExistException as e:
            return self.error_response(request, {'error': e.error, 'message': e.message})
        unlocked_chapters_for_user = dal.get_unlocked_chapters_for_user(user_id)
        return self.create_response(request, {'chapters': unlocked_chapters_for_user})

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
                        'error': 'no{}Present'.format(''.join([attr[0].upper(), attr[1:]])),
                        'message': 'No {} present'.format(attr)
                    }
                    for attr in error_in_attrs
                ]
            )


