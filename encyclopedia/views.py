from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_page(request, title):
    return  render(request, "encyclopedia/prueba.html", {
        "title": title,
        "text": util.get_entry(title),
    })