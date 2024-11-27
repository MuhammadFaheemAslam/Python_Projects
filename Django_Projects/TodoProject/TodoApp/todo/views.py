from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Todo
from .forms import TodoForm

def index(request):
    todo_list = Todo.objects.order_by('id')

    form = TodoForm()

    context = {'todo_list' : todo_list, 'form' : form}

    return render(request, 'index.html', context)

@require_POST
def addTodo(request):
    form = TodoForm(request.POST)

    if form.is_valid():
        new_todo = Todo(text=request.POST['text'])
        new_todo.created_at = timezone.now()
        new_todo.save()

    return redirect('index')

def completeTodo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.complete = True
    todo.save()

    return redirect('index')

def uncompleteTodo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.complete = False
    todo.save()
    return redirect('index')

def deletecompleted(request):
    Todo.objects.filter(complete__exact=True).delete()
    return redirect('index')

def deleteall(request):
    Todo.objects.all().delete()
    return redirect('index')

def search_todo(request):
    search_text = request.GET.get('search_text', '')  # Get the search query from the request
    todo_list = Todo.objects.filter(text__icontains=search_text)  # Filter tasks based on the search query

    # Pass the search results to the template
    context = {'todo_list': todo_list, 'form': TodoForm()}  # Include the form for adding new tasks
    return render(request, 'index.html', context)
