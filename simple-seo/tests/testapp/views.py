"""Views for Johnny's testapp."""

from django.shortcuts import render_to_response


def template_test(request):
    """Render a simple template"""
    return render_to_response('test.html', locals())