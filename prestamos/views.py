from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import ProtectedError
from .models import Herramienta, Categoria
from .forms import HerramientaForm, CategoriaForm

def es_encargado(user):
    return user.is_authenticated and user.is_staff

def inicio(request):
    return render(request, 'prestamos/inicio.html')

# --- CRUD HERRAMIENTAS ---

@login_required
@user_passes_test(es_encargado)
def herramienta_list(request):
    query = request.GET.get('q', '')
    categoria_id = request.GET.get('categoria', '')
    
    herramientas = Herramienta.objects.all()
    if query:
        herramientas = herramientas.filter(nombre__icontains=query)
    if categoria_id:
        herramientas = herramientas.filter(categoria_id=categoria_id)
        
    categorias = Categoria.objects.all()
    return render(request, 'prestamos/herramienta_list.html', {
        'herramientas': herramientas,
        'categorias': categorias,
        'query': query,
        'categoria_id': categoria_id
    })

@login_required
@user_passes_test(es_encargado)
def herramienta_detail(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    return render(request, 'prestamos/herramienta_detail.html', {'herramienta': herramienta})

@login_required
@user_passes_test(es_encargado)
def herramienta_create(request):
    if request.method == 'POST':
        form = HerramientaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Herramienta creada exitosamente.")
            return redirect('herramienta_list')
    else:
        form = HerramientaForm()
    return render(request, 'prestamos/herramienta_form.html', {'form': form, 'titulo': 'Crear Herramienta'})

@login_required
@user_passes_test(es_encargado)
def herramienta_update(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    if request.method == 'POST':
        form = HerramientaForm(request.POST, instance=herramienta)
        if form.is_valid():
            form.save()
            messages.success(request, "Herramienta actualizada exitosamente.")
            return redirect('herramienta_list')
    else:
        form = HerramientaForm(instance=herramienta)
    return render(request, 'prestamos/herramienta_form.html', {'form': form, 'titulo': 'Editar Herramienta'})

@login_required
@user_passes_test(es_encargado)
def herramienta_delete(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    if request.method == 'POST':
        herramienta.delete()
        messages.success(request, "Herramienta eliminada exitosamente.")
        return redirect('herramienta_list')
    return render(request, 'prestamos/herramienta_confirm_delete.html', {'herramienta': herramienta})


# --- CRUD CATEGORÍAS ---

@login_required
@user_passes_test(es_encargado)
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'prestamos/categoria_list.html', {'categorias': categorias})

@login_required
@user_passes_test(es_encargado)
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada exitosamente.")
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'prestamos/categoria_form.html', {'form': form, 'titulo': 'Crear Categoría'})

@login_required
@user_passes_test(es_encargado)
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada exitosamente.")
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'prestamos/categoria_form.html', {'form': form, 'titulo': 'Editar Categoría'})

@login_required
@user_passes_test(es_encargado)
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        try:
            categoria.delete()
            messages.success(request, "Categoría eliminada exitosamente.")
        except ProtectedError:
            messages.error(request, "No se puede eliminar la categoría porque tiene herramientas asociadas.")
        return redirect('categoria_list')
    return render(request, 'prestamos/categoria_confirm_delete.html', {'categoria': categoria})