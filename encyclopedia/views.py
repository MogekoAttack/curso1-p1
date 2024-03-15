import os
import re
import markdown2
from random import randint
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import util

class NewEntry(forms.Form):
    title = forms.CharField()
    entry = forms.CharField(widget=forms.Textarea())

class EditEntry(forms.Form):
    entry = forms.CharField(
        # widget=forms.Textarea,
        label="",
        initial="Your name",
    )

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_page(request, title):
    if util.get_entry(title) == None:
        texto = None
    else:
        texto = markdown2.markdown(util.get_entry(title))
    return  render(request, "encyclopedia/entry.html", {
        "title": title,
        "text": texto,
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
    if request.method == 'POST':
        form = NewEntry(request.POST)
        if form.is_valid():
            if util.get_entry(form.cleaned_data['title']) != None:
                return render (request, "encyclopedia/new_page.html",{
                    "form": form,
                    "exist": "ERROR",
                })
            util.save_entry(form.cleaned_data['title'],form.cleaned_data['entry'])
            return HttpResponseRedirect(f"wiki/{form.cleaned_data['title']}")
        else:
            return render (request, "encyclopedia/new_page.html",{
                "form": form,
                "exist": "ERROR",
            })
    return render (request, "encyclopedia/new_page.html",{
        "form": NewEntry(),
        "exist": "",
    })
    
def edit_page(request, title):
    form = EditEntry(request.POST)
    return render (request, "encyclopedia/edit_page.html",{
        "title": title,
        "content": util.get_entry(title),
    })
    
def edit_page_info(request, title):
    if request.method == 'POST':
        entry_text = request.POST.get('entry')
        
        util.save_entry(title, entry_text)
        print(f"Texto recibido: {entry_text}")
        
        return HttpResponseRedirect(f"/wiki/{title}")

def random(request):
    results = util.list_entries()
    return HttpResponseRedirect(f"/wiki/{results[randint(0,results.__len__()-1)]}")