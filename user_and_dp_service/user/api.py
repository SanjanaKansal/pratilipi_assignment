import json

from tastypie.resources import Resource
from tastypie.utils.urls import trailing_slash
from django.conf.urls import url
from django.http import HttpResponseNotAllowed

from user import dal
from user import exceptions


class UserResource(Resource):
    class Meta:
        resource_name = 'user'

    def prepend_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('fetch_and_create_user'),
                name="api_fetch_and_create_user",
            )
        ]

    def fetch_and_create_user(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.create_user(request, *args, **kwargs)
        elif request.method == 'GET':
            return self.fetch_user(request, *args, **kwargs)
        return HttpResponseNotAllowed(request.method, 'Invalid Request Method')

    def create_user(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        validation_err = self._validate_json_data(request, {'username': username, 'password': password})
        if validation_err:
            return validation_err
        try:
            dal.get_user_by_username(username)
        except exceptions.UserDoesNotExistException:
            user = dal.save_user(username, password)
            return self.create_response(
                request,
                {
                    'success': True,
                    'message': 'User successfully created',
                    'user': {
                        'id': user.id,
                        'username': user.username
                    }
                }
            )
        exc = exceptions.UsernameAlreadyExistException
        return self.error_response(
            request,
            {
                'success': False,
                'error': exc.error,
                'message': exc.message
            }
        )

    def fetch_user(self, request, *args, **kwargs):
        id = request.GET.get('id')
        try:
            user = dal.get_user(id)
        except exceptions.UserDoesNotExistException as e:
            return self.error_response(request, {'error': e.error, 'message': e.message})
        return self.create_response(request, {'id': user.id, 'username': user.username})

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




