from django.urls import path
from .tools import *

urlpatterns = []


def route(p: str):
    def decorator(func):
        urlpatterns.append(path(p, func))
        return func

    return decorator


def routeApi(p: str):
    def decorator(func):
        def warp(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except BackendException as e:
                return e.args[0]

        urlpatterns.append(path("api/" + p, warp))
        return warp

    return decorator
