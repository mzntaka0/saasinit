# -*- coding: utf-8 -*-
"""
"""
import warnings
import uuid
from datetime import datetime
from calendar import timegm

import jwt
from django.contrib.auth import authenticate

from functools import wraps
from django.http import JsonResponse

from rest_framework_jwt.compat import get_username_field
from rest_framework_jwt.settings import api_settings


def get_username(jwt):
    username = jwt.get('nickname')  # nickname is equal to username in Auth0
    tenant = jwt.get('https://next-ocr.io/tenant')
    authenticate(remote_user=username, tenant=tenant)
    return username


def jwt_payload_handler(user):
    username_field = get_username_field()
    username = get_username(user)

    warnings.warn(
        'The following fields will be removed in the future: '
        '`email` and `user_id`. ',
        DeprecationWarning
    )

    payload = {
        'user_id': user.pk,
        'tenant_id': user.tenant_id,
        'username': username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }
    if hasattr(user, 'email'):
        payload['email'] = user.email
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)
    if isinstance(user.tenant_id, uuid.UUID):
        payload['user_id'] = str(user.tenant_id)

    payload[username_field] = username

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload


def jwt_decode_handler(token):
    # FIXME: need to validate jwt
    #options = {
    #    'verify_exp': api_settings.JWT_VERIFY_EXPIRATION,
    #}
    ## get user from token, BEFORE verification, to get user secret key
    #unverified_payload = jwt.decode(token, None, False)
    #secret_key = jwt_get_secret_key(unverified_payload)
    #jwt_ = jwt.decode(
    #    token,
    #    api_settings.JWT_PUBLIC_KEY or secret_key,
    #    api_settings.JWT_VERIFY,
    #    options=options,
    #    leeway=api_settings.JWT_LEEWAY,
    #    audience=api_settings.JWT_AUDIENCE,
    #    issuer=api_settings.JWT_ISSUER,
    #    algorithms=[api_settings.JWT_ALGORITHM]
    #)
    jwt_ = jwt.decode(token, verify=False)
    return jwt_


def jwt_get_secret_key(payload=None):
    """
    For enhanced security you may want to use a secret key based on user.
    This way you have an option to logout only this user if:
        - token is compromised
        - password is changed
        - etc.
    """
    if api_settings.JWT_GET_USER_SECRET_KEY:
        User = get_user_model()  # noqa: N806
        user = User.objects.get(pk=payload.get('user_id'))
        key = str(api_settings.JWT_GET_USER_SECRET_KEY(user))
        return key
    return api_settings.JWT_SECRET_KEY


class JWTManager:

    def __init__(self):
        pass

    @staticmethod
    def get_token_auth_header(request):
        """Obtains the Access Token from the Authorization Header
        """
        auth = request.META.get("HTTP_AUTHORIZATION", None)
        token = auth.split()[1]
        return token

    @staticmethod
    def requires_scope(required_scope):
        """Determines if the required scope is present in the Access Token
        Args:
            required_scope (str): The scope required to access the resource
        """
        def require_scope(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                token = JWTManager.get_token_auth_header(args[0])
                unverified_claims = jwt.get_unverified_claims(token)
                token_scopes = unverified_claims["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
                response = JsonResponse({'message': 'You don\'t have access to this resource'})
                response.status_code = 403
                return response
            return decorated
        return require_scope
