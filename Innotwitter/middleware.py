import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from Innotwitter.settings import JWT_SECRET_KEY
from users.models import User


def jwt_middleware(get_response):
    def middleware(request):
        jwt_token = request.headers.get("Authorization", None)
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms=['HS256'])

            except jwt.ExpiredSignatureError:
                response = create_response("Authentication token has expired", status.HTTP_401_UNAUTHORIZED)
                return response
            except (jwt.DecodeError, jwt.InvalidTokenError):
                response = create_response("Authorization has failed, token is invalid", status.HTTP_401_UNAUTHORIZED)
                return response

            username = payload.get("username", None)

            user = User.objects.filter(username=username).first()

            if user is None:
                response = create_response("User doesn't exist", status.HTTP_401_UNAUTHORIZED)
                return response

            if user.is_blocked:
                response = create_response("User is blocked", status.HTTP_401_UNAUTHORIZED)
                return response

        response = get_response(request)

        return response

    return middleware


def create_response(message, status_code):
    response = Response(data=message, status=status_code)
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
    response.render()

    return response
