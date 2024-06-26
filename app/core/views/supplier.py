from django.urls import reverse_lazy
from app.core.forms.supplier import SupplierForm
from app.core.models import Supplier
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, ListViewMixin, PermissionMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q

class SupplierListView(ListViewMixin, ListView):
    template_name = 'core/suppliers/list.html'
    model = Supplier
    context_object_name = 'suppliers'
    permission_required = 'view_supplier'
    
    def get_queryset(self):
        q1 = self.request.GET.get('q') # ver
        if q1 is not None: 
            self.query.add(Q(name__icontains=q1), Q.OR) 
            self.query.add(Q(ruc__icontains=q1), Q.OR) 
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permission_add'] = context['permissions'].get('add_supplier','')
        context['create_url'] = reverse_lazy('core:supplier_create')
        return context

class SupplierCreateView(CreateViewMixin, CreateView):
    model = Supplier
    template_name = 'core/suppliers/form.html'
    form_class = SupplierForm
    success_url = reverse_lazy('core:supplier_list')
    permission_required = 'add_supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Proveedor'
        context['back_url'] = self.success_url
        return context
     
# # Crear un proveedor
# def supplier_create(request):
#     data = {"title1": "IC - Crear Proveedores", "title2": "Ingreso De Proveedores"}
#     if request.method == "POST":
#         form = SupplierForm(request.POST, request.FILES)  # Añadir request.FILES para manejar archivos
#         if form.is_valid():
#             supplier = form.save(commit=False)
#             supplier.user = request.user  # Asignar el usuario actual al proveedor
#             supplier.save()
#             messages.success(request, f"Éxito al crear al proveedor {supplier.name}.")
#             return redirect("core:supplier_list")
#     else:
#         form = SupplierForm()  # Mover esto aquí para que el formulario se cree en ambos casos

#     # Pasar el formulario al contexto de la plantilla en ambos casos
#     data["form"] = form
#     return render(request, "core/suppliers/form.html", data)
