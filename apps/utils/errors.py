from django.shortcuts import render


def error_400(request, exception):
    return render(request, 'errors/400.html', status=400)


def error_403(request, exception):
    return render(request, 'errors/403.html', status=403)


def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def error_500(request, **kwargs):
    return render(request, 'errors/500.html', status=500)
