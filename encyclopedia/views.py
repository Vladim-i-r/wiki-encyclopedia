from django.shortcuts import render

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
        return render(request, "encyclopedia/title.html", {
            "info": util.get_entry(title), "title": title 
        })