from random import randint
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from markdown2 import markdown
from . import util
from django import forms


def index(request):
    """
    Shows the user all the encyclopedia's entries collection
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    """
    Takes the user to the selected encyclopedia entry by clicking any of the home entries collection
    """
    if title not in util.list_entries():
        return render(request, "encyclopedia/error.html", {
            "error": title 
        })
    else:
        contentmd = util.get_entry(title)
        contenthtml = markdown(contentmd)
        return render(request, "encyclopedia/entry.html", {
            "content": contenthtml, "title": title 
        })
    
def search(request):
    """
   Takes the user to the selected encyclopedia entry based on the input from the search bar
    """
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
    title = forms.CharField(label="New Title",widget=forms.TextInput(attrs={'name':'title', 'placeholder':'e.g. CS50 Wikipedia','style':'width: 35%;'}))
    content = forms.CharField(label="Content:",widget=forms.Textarea(attrs={'name':'content','placeholder':'Content...','style':'width: 90%; height: 60vh; resize: none; margin-top: 10px;'}))   

def new_page(request):

    """
    Lets the user create a new entry and save it to the encyclopedia's entries collection
    """

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

class EditPageForm(forms.Form): # Needs to be created in order to disable the Title charfield and be readonly!!!             
    title = forms.CharField(label="Title",widget=forms.TextInput(attrs={'name':'title','readonly':'readonly','style':'width: 35%;'}))
    content = forms.CharField(label="Content   ↓:",widget=forms.Textarea(attrs={'name':'content','placeholder':'Content...','style':'width: 90%; height: 60vh; resize: none; margin-top: 10px;'}))   


def edit_page(request, title):

    """
    Lets the user edit the selected encyclopedia entry
    """
     
    if request.method == "GET":
        content = util.get_entry(title)
        form = EditPageForm({"title": title, "content": content})
        return render(request,"encyclopedia/edit.html",{
            "form": form,
            "title": title
        })

    form = EditPageForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data.get("title")
        content = form.cleaned_data.get("content")
        #util.save_entry(title=title, content=content)
        util.save_entry(form.cleaned_data['title'], bytes(form.cleaned_data['content'], 'utf8')) #This will prevent from the function util adding blank newlines when saving
        return redirect("entry", title)


#def random_page(request):
#    randomp = random.choice(util.list_entries)
#    return redirect("entry", randomp)

def random_page(request):
    """
    Takes the user to a random encyclopedia entry
    """
    entries = util.list_entries()
    randomp = entries[randint(0, len(entries) - 1)]
    return redirect("entry", randomp)
