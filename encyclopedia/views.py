from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
#from markdown2 import markdown
from . import util


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
            print(f'Se agrega {s_entry}')
    print(f'Visualizando la(s) que encontro {find_entries}')
        

    if find_entries:
        return render(request, "encyclopedia/search.html", {
        "s_entries" : find_entries, 
        "q" : q
        })
    else:
        return render(request, "encyclopedia/error.html")

