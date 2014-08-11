from django.shortcuts import render_to_response


def template_test(request):
    """Render a simple template"""
    return render_to_response('simple_seo_test.html', locals())