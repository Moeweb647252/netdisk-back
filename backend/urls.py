from django.urls import path

urlpatterns = []


def route(p: str):
    def decorator(func):
        urlpatterns.append(path(p, func))
        return func

    return decorator


def routeApi(p: str):
    def decorator(func):
        urlpatterns.append(path("api/" + p, func))
        return func

    return decorator
