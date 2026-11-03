import random
import markdown2
from django.shortcuts import redirect, render
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {"message": f'The page "{title}" was not found.'}, status=404)
    return render(request, "encyclopedia/entry.html", {"title": title, "content": markdown2.markdown(content)})

def search(request):
    query = request.GET.get("q", "").strip()
    entries = util.list_entries()
    exact = next((name for name in entries if name.casefold() == query.casefold()), None)
    if exact:
        return redirect("entry", title=exact)
    results = [name for name in entries if query.casefold() in name.casefold()] if query else []
    return render(request, "encyclopedia/search.html", {"query": query, "results": results})

def new_page(request):
    if request.method == "POST":
        title, content = request.POST.get("title", "").strip(), request.POST.get("content", "")
        if not title or not content.strip():
            return render(request, "encyclopedia/new_page.html", {"error": "Both a title and Markdown content are required.", "title": title, "content": content})
        if title.casefold() in [name.casefold() for name in util.list_entries()]:
            return render(request, "encyclopedia/new_page.html", {"error": f'An entry named "{title}" already exists.', "title": title, "content": content})
        if "/" in title or "\\" in title or title in {".", ".."}:
            return render(request, "encyclopedia/new_page.html", {"error": "Please choose a valid title without slashes.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    existing = util.get_entry(title)
    if existing is None:
        return render(request, "encyclopedia/error.html", {"message": f'The page "{title}" was not found.'}, status=404)
    if request.method == "POST":
        content = request.POST.get("content", "")
        if not content.strip():
            return render(request, "encyclopedia/edit_page.html", {"title": title, "content": content, "error": "Entry content cannot be empty."})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit_page.html", {"title": title, "content": existing})

def random_page(request):
    entries = util.list_entries()
    if not entries:
        return render(request, "encyclopedia/error.html", {"message": "There are no encyclopedia entries yet."})
    return redirect("entry", title=random.choice(entries))
