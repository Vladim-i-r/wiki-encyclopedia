from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
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
        return render(request, "encyclopedia/error.html")

class NewPageForm(forms.Form):
    title = forms.CharField(label="New Title\n",widget=forms.TextInput(attrs={'name':'title'}))
    content = forms.CharField(label=mark_safe("Content:"),widget=forms.Textarea(attrs={'name':'content'}))   

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            print("Si es valido y se haria el reverse para la nueva pagina")
            #return render(request, "encyclopedia/new.html")
        else:
            print("Se imprime se verifica si existe y se imprime un warning, se redirije a la misma")

    return render(request,"encyclopedia/new.html", {
        "form":NewPageForm()
    })


