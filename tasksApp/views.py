from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.core.paginator import Paginator
from django.db.models import Q  

def task_list(request):
    query = request.GET.get('q', '')
    
    if query:
        tasks = Task.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        tasks = Task.objects.all()

    paginator = Paginator(tasks, 10)  # Muestra 10 tareas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'task_list.html', {'page_obj': page_obj, 'query': query})


def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        Task.objects.create(title=title, description=description)
        return redirect('task_list')
    return render(request, 'add_task.html')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.save()
        return redirect('task_list')
    
    return render(request, 'edit_task.html', {'task': task})

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('task_list')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')