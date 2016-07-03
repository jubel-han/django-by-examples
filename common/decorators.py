from django.http import HttpResponseBadRequest


def ajax_required(f):
    def warp(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    warp.__doc__=f.__doc__
    warp.__name__=f.__name__
    return warp
