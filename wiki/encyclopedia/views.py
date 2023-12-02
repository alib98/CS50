import os
import random as python_random
from markdown2 import Markdown

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

from . import util
from . import forms

def highlight_substring(original_string, substring_to_highlight):
    highlighted_string = original_string.replace(
        substring_to_highlight,
        f'<span style="background-color: yellow;">{substring_to_highlight}</span>'
    )
    return highlighted_string

def index(request):
    return render(request, 'encyclopedia/index.html', {
        'entries': util.list_entries()
    })

def entry(request, title):
    article = util.get_entry(title)
    markdowner = Markdown()
    if article == None:
        return render(request, 'encyclopedia/entry_not_found.html')
    else:
        return render(request,'encyclopedia/entry.html', {
            'title': title,
            'article': markdowner.convert(article),
        })
        
def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')       
        if search_query in util.list_entries():
            return HttpResponseRedirect(reverse('entry', kwargs={'title': search_query}))
        else:
            search_result = [s for s in util.list_entries() if search_query in s]
            # if len(search_result) == 0:
            #     return HttpResponseRedirect(reverse('index'))
            #     pass
            # else:
            anchor_links = search_result.copy()
            search_result = [highlight_substring(s, search_query) for s in search_result]
            combined_data = zip(anchor_links, search_result)
            return render(request, 'encyclopedia/search.html', {
                'combined_data': combined_data,
            })
    else:
        return HttpResponseRedirect(reverse('index'))
            
def add(request):
    if request.method == 'POST':
        add_form = forms.AddForm(request.POST)
        if add_form.is_valid():
            title = add_form.cleaned_data['title']
            if util.get_entry(title) is not None:
                return render(request, 'encyclopedia/eror_entry_is_saved_before.html')
            content = add_form.cleaned_data['content']
            filename = f'{title.replace(" ","_")}.md'
            file_path = os.path.join(settings.MEDIA_ROOT, 'entries', filename)
            with open(file_path, 'w') as file:
                file.write(f"# {title}\n\n" + content)
            return HttpResponseRedirect(reverse('entry', kwargs={"title": title}))
    return render(request, 'encyclopedia/add.html', {
        'add_form': forms.AddForm(),
    })

def edit(request, title):
    file_path = os.path.join(settings.MEDIA_ROOT, 'entries', f'{title}.md')
    if request.method == 'POST':
        form = forms.EditForm(request.POST)
        if form.is_valid():
            with open(file_path, 'w') as file:
                file.write(form.cleaned_data['content'])
            return HttpResponseRedirect(reverse('entry', kwargs={"title": title}))
    else:
        with open(file_path, 'r') as file:
            content = file.read()
        return render(request, 'encyclopedia/edit.html', {
                'edit_form': forms.EditForm(initial={
                'title': title, 
                'content': content,
            })
        })
    
def random(request):
    random_article_title = python_random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('entry', kwargs={"title": random_article_title}))

def delete(request, title):
    if request.method == "POST":
            file_path = os.path.join(settings.MEDIA_ROOT, 'entries', f'{title}.md')
            os.remove(file_path)
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'encyclopedia/delete.html', {
            'title': title
        })


    
