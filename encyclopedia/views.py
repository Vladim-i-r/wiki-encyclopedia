from django.shortcuts import redirect, render
#from markdown2 import markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    if title not in util.list_entries():
        return render(request, "encyclopedia/error.html", {
            "error": title 
        })
    else:
        contentmd = util.get_entry(title)
        #content = markdown(contentmd)
        return render(request, "encyclopedia/title.html", {
            "content": contentmd, "title": title 
        })
    
def search(request):
    q = request.GET.get('q').strip()
    if q in util.list_entries():
        return redirect("title", title=q)
    return render(request, "encyclopedia/search.html", {
        "entries" : util.search(q), 
        "q" : q
    })
