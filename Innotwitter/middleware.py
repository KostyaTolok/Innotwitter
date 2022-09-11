import jwt
from django.http import HttpResponse

from Innotwitter.settings import JWT_SECRET_KEY
from users.models import User


def jwt_middleware(get_response):
    def middleware(request):
        jwt_token = request.headers.get("Authorization", None)
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return HttpResponse("Authentication token has expired", status=401)
            except (jwt.DecodeError, jwt.InvalidTokenError):
                return HttpResponse("Authorization has failed, token is invalid", status=401)

            username = payload.get("username", None)

            user = User.objects.filter(username=username).first()

            if user is None:
                return HttpResponse("User doesn't exist", status=401)

            if user.is_blocked:
                return HttpResponse("User is blocked", status=401)

        response = get_response(request)

        return response

    return middleware
