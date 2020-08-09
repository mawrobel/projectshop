from django.contrib import admin
from .models import Order, OrderItem
import csv
from django.utils.html import mark_safe
import datetime
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html_join


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment: filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.description = 'Export to CSV'




class OrderAdmin(admin.ModelAdmin):
    def order_detail(self, obj):
        display_text = ", ".join([
            "<a href={}>Show more</a>".format(reverse('orders:admin_order_detail', args=[obj.id]))])
        if display_text:
            return mark_safe(display_text)
        return "-"

    order_detail.allow_tags = True
    order_detail.short_description = "Details"

    def order_pdf(self, obj):
        display_text = ", ".join([
            "<a href={}>PDF</a>".format(reverse('orders:admin_order_pdf', args=[obj.id]))])
        if display_text:
            return mark_safe(display_text)
        return "-"

    order_pdf.allow_tags = True
    order_pdf.short_description = "Order in PDF"

    def __init__(self, *args, **kwargs):
        super(OrderAdmin, self).__init__(*args, **kwargs)

    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated', 'canceled', 'order_detail', 'order_pdf']
    list_filter = ['paid', 'created', 'updated', 'canceled']
    inlines = [OrderItemInline]
    actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)


