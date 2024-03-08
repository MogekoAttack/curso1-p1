import os
import re
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
    
def search(request):
    query = request.GET.get('q')
    entries = os.listdir('entries')
    results = []

    for entry in entries:
        with open(f'entries/{entry}') as f:
            content = f.read()
            if re.search(query, content, re.I):
                results.append(entry.replace('.md', ''))
                
    return render(request, "encyclopedia/search_results.html", {
        "results": results,
        "query": query
    })
    
def new_page(request):
    return render (request, "encyclopedia/new_page.html")