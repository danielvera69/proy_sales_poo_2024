import json
from django.http import JsonResponse
from django.db import transaction
from django.urls import reverse_lazy
from app.core.forms.supplier import SupplierForm
from app.core.models import Product
from app.sales.forms.invoice import InvoiceForm
from app.sales.models import Invoice, InvoiceDetail
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q,F
from decimal import Decimal

from proy_sales.utils import custom_serializer, save_audit


class SaleListView(PermissionMixin,ListViewMixin, ListView):
    template_name = 'sales/invoices/list.html'
    model = Invoice
    context_object_name = 'invoices'
    permission_required = 'view_invoice'
    
    def get_queryset(self):
        q1 = self.request.GET.get('q') # ver
        if q1 is not None: 
            self.query.add(Q(id = q1), Q.OR) 
            self.query.add(Q(customer__first_name__icontains=q1), Q.OR) 
            self.query.add(Q(customer__last_name__icontains=q1), Q.OR) 
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['permission_add'] = context['permissions'].get('add_supplier','')
        # context['create_url'] = reverse_lazy('core:supplier_create')
        return context

class SaleCreateView(PermissionMixin,CreateViewMixin, CreateView):
    model = Invoice
    template_name = 'sales/invoices/form.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('sales:invoice_list')
    permission_required = 'add_invoice' # en PermissionMixn se verfica si un grupo tiene el permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = Product.active_products.values('id','description','price','stock','iva__value')
        context['detail_sales'] =[]
        context['save_url'] = reverse_lazy('sales:sales_create') 
        print(context['products'])
        
        return context
    
    def post(self, request, *args, **kwargs):
        print("POST request received")
        form = self.get_form()
        print(request.POST)
        if not form.is_valid():
            messages.success(self.request, f"Error al grabar la venta!!!: {form.errors}.")
            return JsonResponse({"msg":form.errors},status=400)
        data = request.POST
        try:
            with transaction.atomic():
                sale = Invoice.objects.create(
                    customer_id=int(data['customer']),
                    payment_method_id=int(data['payment_method']),
                    issue_date=data['issue_date'],
                    subtotal=Decimal(data['subtotal']),
                    discount=Decimal(data['discount']),
                    iva= Decimal(data['iva']),
                    total=Decimal(data['total']),
                    payment=Decimal(data['payment']),
                    change=Decimal(data['change']),
                    state='F'
                )
                details = json.loads(request.POST['detail'])
                print(details) #[{'id':'1','price':'2'},{}]
                for detail in details:
                    inv_det = InvoiceDetail.objects.create(
                        invoice=sale,
                        product_id=int(detail['id']),
                        quantity=Decimal(detail['quantify']),
                        price=Decimal(detail['price']),
                        iva=Decimal(detail['iva']),  
                        subtotal=Decimal(detail['sub'])
                    )
                    inv_det.product.reduce_stock(Decimal(detail['quantify']))
                save_audit(request, sale, "A")
                messages.success(self.request, f"Éxito al registrar la venta F#{sale.id}")
                return JsonResponse({"msg":"Éxito al registrar la venta Factura"},status=200)
        except Exception as ex:
              return JsonResponse({"msg":ex},status=400)


class SaleUpdateView(PermissionMixin,UpdateViewMixin, UpdateView):
    model = Invoice
    template_name = 'sales/invoices/form.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('sales:invoice_list')
    permission_required = 'change_invoice' # en PermissionMixn se verfica si un grupo tiene el permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = Product.active_products.values('id','description','price','stock','iva__value')
        detail_sale =list(InvoiceDetail.objects.filter(invoice_id=self.object.id).values(
             "product","product__description","quantity","price","subtotal","iva"))
        print("detalle")
        detail_sale=json.dumps(detail_sale,default=custom_serializer)
        context['detail_sales']=detail_sale  #[{'id':1,'precio':2},{},{}]
        context['save_url'] = reverse_lazy('sales:sales_update',kwargs={"pk":self.object.id})
        print(detail_sale)
        return context
    
    def post(self, request, *args, **kwargs):
        print("POST request update")
        form = self.get_form()
        print(request.POST)
        if not form.is_valid():
            messages.success(self.request, f"Error al actualizar la venta!!!: {form.errors}.")
            return JsonResponse({"msg":form.errors},status=400)
        data = request.POST
        try:
            print("facturaId: ")
            print(self.kwargs.get('pk'))
            sale= Invoice.objects.get(id=self.kwargs.get('pk'))
           
            with transaction.atomic():
                sale.customer_id=int(data['customer'])
                sale.payment_method_id=int(data['payment_method'])
                sale.issue_date=data['issue_date']
                sale.subtotal=Decimal(data['subtotal'])
                sale.discount=Decimal(data['discount'])
                sale.iva= Decimal(data['iva'])
                sale.total=Decimal(data['total'])
                sale.payment=Decimal(data['payment'])
                sale.change=Decimal(data['change'])
                sale.state='M'
                sale.save()
                details = json.loads(request.POST['detail'])
                print(details)
                detdelete=InvoiceDetail.objects.filter(invoice_id=sale.id)
                for det in detdelete:
                    det.product.stock+= int(det.quantity)
                    det.product.save()
                detdelete.delete()
               
                for detail in details:
                    inv_det = InvoiceDetail.objects.create(
                        invoice=sale,
                        product_id=int(detail['id']),
                        quantity=Decimal(detail['quantify']),
                        price=Decimal(detail['price']),
                        iva=Decimal(detail['iva']),  
                        subtotal=Decimal(detail['sub'])
                    )
                    inv_det.product.reduce_stock(Decimal(detail['quantify']))
                save_audit(request, sale, "M")
                messages.success(self.request, f"Éxito al Modificar la venta F#{sale.id}")
                return JsonResponse({"msg":"Éxito al Modificar la venta Factura"},status=200)
        except Exception as ex:
              return JsonResponse({"msg":ex},status=400)
          
# class SupplierDeleteView(PermissionMixin,DeleteViewMixin, DeleteView):
    # model = Supplier
    # template_name = 'core/delete.html'
    # success_url = reverse_lazy('core:supplier_list')
    # permission_required = 'delete_supplier'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     context['grabar'] = 'Eliminar Proveedorl'
    #     context['description'] = f"¿Desea Eliminar al Proveedor: {self.object.name}?"
    #     context['back_url'] = self.success_url
    #     return context
    
    # def delete(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     success_message = f"Éxito al eliminar lógicamente al proveedor {self.object.name}."
    #     messages.success(self.request, success_message)
    #     # Cambiar el estado de eliminado lógico
    #     # self.object.deleted = True
    #     # self.object.save()
    #     return super().delete(request, *args, **kwargs)