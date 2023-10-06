from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
#from markdown2 import markdown
from . import util
from django import forms
from django.utils.safestring import mark_safe


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if title not in util.list_entries():
        return render(request, "encyclopedia/error.html", {
            "error": title 
        })
    else:
        contentmd = util.get_entry(title)
        #content = markdown(contentmd)
        return render(request, "encyclopedia/entry.html", {
            "content": contentmd, "title": title 
        })
    
def search(request):
    s_entries = util.list_entries()
    find_entries = list()

    q = request.GET.get('q').strip()
    if q in util.list_entries():
        return HttpResponseRedirect(f"wiki/{q}")
        #return redirect("entry", title=q)
    
    for s_entry in s_entries:
        if q in s_entry:
            find_entries.append(s_entry)
            print(f'{s_entry} is added')
    print(f'List of entries added {find_entries}')
        

    if find_entries:
        return render(request, "encyclopedia/search.html", {
        "s_entries" : find_entries, 
        "q" : q
        })
    else:
        return render(request, "encyclopedia/error.html",{
            "notfound":q
        })

class NewPageForm(forms.Form):
    title = forms.CharField(label="New Title",widget=forms.TextInput(attrs={'name':'title'}))
    content = forms.CharField(label="Content:",widget=forms.Textarea(attrs={'name':'content','style':'width: 90%; height: 60vh; resize: none; margin-top: 10px;'}))   

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title_user = request.POST.get("title") #title_user = request.session["title"] THIS IS ONLY WHEN USING A DATABASE 
            content_user = request.POST.get("content") #content_user = request.session["content"] THIS IS ONLY WHEN USING A DATABASE 
            if title_user not in util.list_entries():
                util.save_entry(title_user, content_user)
                return render(request, "encyclopedia/entry.html",{
                    "title": title_user,
                    "content": content_user
                })
            else:
                message = "Title already on use, it can't be saved. Try writing a different title or non-existent one."
                return render(request, "encyclopedia/new.html",{
                    "message": message,
                    "form": form
                })
        else:
            return render(request, "encyclopedia/new.html",{
                "form": form
            })

    return render(request,"encyclopedia/new.html", {
        "form":NewPageForm()
    })


def edit_page(request, title):
    if request.method == 'POST':
        form = NewPageForm(initial={'title': title, 'content': util.get_entry(title)})
        form.fields['title'].widget = forms.HiddenInput()
        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return render(request, 'encyclopedia/edit.html', {
                "title": title,
                "content":util.get_entry(title),
                "form": form
            })
            #return HttpResponseRedirect(f"wiki/{title}")
        else:
            contentt = request.POST.get('content')
            return render(request, 'encyclopedia/edit.html', {
                "title": title,
                "content":util.get_entry(title),
                "form": form
            })
        
    return render(request, "encyclopedia/edit.html",{
        "form" : form
    })

#def save_page(request):
 #   if request.method == 'POST':
  #      title = request.POST.get('title')
   #     content = request.POST.get('content')*/

        

def random_page(request):
    return

