from django.shortcuts import render


def landing_page_view(request, *args, **kwargs):
    return render(request, 'pages/landing-page.html', {})
