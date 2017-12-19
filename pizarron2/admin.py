from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
# from openpyxl.utils import get_column_letter

from .models import Referencia, Contenedor

"""
@admin.register(Referencia)
class  ReferenciaAdmin(admin.ModelAdmin):
    pass
"""    



class ReferenciaInlineAdmin(admin.TabularInline):
    model = Referencia
    extra = 1


@admin.register(Contenedor)
class ContenedorAdmin(admin.ModelAdmin):
    readonly_fields = ('KGPCONSOLIDADO', 'CBMPCONSOLIDADO', 'MONTOPCONSOLIDADO')
    search_fields = ('REFERENCIA',)
    list_display = ('REFERENCIA', 'ESTATUS', 'ESTADO', 'FECHABL', 'FECHAETA', 'FECHACEDIS', 'FECHAPREVENTA', 'DESTINO',
                    'CONTENEDORNO', 'FACTURAFWD', )
    list_filter = ('ESTATUS', 'ESTADO', 'FWD')
    inlines = [ReferenciaInlineAdmin, ]
    actions = ['avanzar_ECP', 'avanzar_ADUANA', 'avanzar_ARRIBADO', 'avanzar_PAGPED', 'avanzar_SOL', 'avanzar_PANTACO',
               'avanzar_ENRUTA', 'avanzar_GONDOLA',  'avanzar_SEMANA', 'avanzar_CONCLUIDO', 'export_xls']

    fieldsets = (
        ('General', {
            'fields': ('REFERENCIA', 'CONTENEDORNO', 'ORIGEN', 'DESTINO','IMPORTEPEDIDO', 'IMPORTEFACTURA',
                       'MONTOFLETE',)
        }),
        ('forwarder', {
            'fields': ('FWD', 'FACTURAFWD', 'FECHAPAGOFWD',)
        }),
        ('Datos Tecnicos Contenedor', {
            'fields': ('CARGA', 'KG', 'CBM', 'KGPCONSOLIDADO', 'CBMPCONSOLIDADO', 'MONTOPCONSOLIDADO') #'fields': ('CARGA', 'KG', 'CBM', 'PCONSOLIDADO')
        }),
        ('Fechas', {
            'fields': ('FECHABL', 'FECHAETA', 'FECHACEDIS', 'FECHAPREVENTA', 'FECHASEMANA')
        }),
        ('Fechas  Reales', {
            'fields': (
            'RALFECHAETA', 'RALFECHABL')
        }),
        ('Comentarios', {
            'classes': ('collapse',),
            'fields': ('NUEVOS', 'MEJORAS', 'OMISIONPREVIOORIGEN', 'ESPECIAL')
        }),

        ('Fechas-tiempo', {
            'classes': ('collapse', ),
            'fields': ('FCECP', 'FCADUANA', 'FCARRIBADO', 'FCPAGPED', 'FCSOL', 'FCGONDOLA', 'FCENRUTA', 'FCPENTACO', 'FCSEMANA')
        })

    )
    """
    fields = (
        ('Puntos',{
            'fields':('BACKORDER', 'FECHAORIGINAL', 'PENDIENTES', 'ESPECIAL')
        } )
    )
    """

    def avanzar_ECP(self, request, queryset):
        queryset.update(ESTADO='ECP',FCECP=timezone.now())
    avanzar_ECP.short_description = 'Avanzar ETA-CEDIS-PVTA'

    def avanzar_ADUANA(self, request, queryset):
        queryset.update(ESTADO='ADUANA', FCADUANA=timezone.now())
    avanzar_ADUANA.short_description = "Avanzar ADUANA"

    def avanzar_ARRIBADO(self, request, queryset):
        queryset.update(ESTADO='ARRIBADO', FCARRIBADO=timezone.now())
    avanzar_ARRIBADO.short_description = "Avanzar ARRIBADO"

    def avanzar_PAGPED(self, request, queryset):
        queryset.update(ESTADO='PAGPED',FCPAGPED=timezone.now())
    avanzar_PAGPED.short_description = "Avanzar PAGPED"

    def avanzar_SOL(self, request, queryset):
        queryset.update(ESTADO='SOL', FCSOL=timezone.now())
    avanzar_SOL.short_description = "Avanzar SOL"

    def avanzar_PANTACO(self, request, queryset):
        queryset.update(ESTADO='PENTACO', FCPENTACO=timezone.now())
    avanzar_PANTACO.short_description = "Avanzar PANTACO"

    def avanzar_ENRUTA(self, request, queryset):
        queryset.update(ESTADO='ENRUTA', FCENRUTA=timezone.now())
    avanzar_ENRUTA.short_description = "Avanzar ENRUTA"

    def avanzar_GONDOLA(self, request, queryset):
        queryset.update(ESTADO='GONDOLA', FCGONDOLA=timezone.now())
    avanzar_GONDOLA.short_description = "Avanzar GONDOLA"

    def avanzar_SEMANA(self, request, queryset):
        queryset.update(ESTADO='SEMANA', FCSEMANA=timezone.now())
    avanzar_SEMANA.short_description = "Avanzar SEMANA"

    def avanzar_CONCLUIDO(self, request, queryset):
        queryset.update(ESTATUS='CONCLUIDO')
    avanzar_CONCLUIDO.short_description = "Avanzar CONCLUIDO"

    def export_xls(modeladmin, request, queryset):
        import xlwt
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=mymodel.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("MyModel")

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.num_format_str = '$#,##0.00'

        columns = [
            (u"REFERENCIA", 5000),
            (u"IMPORTEPEDIDO", 4050),
            (u"IMPORTEFACTURA", 4050),
            (u"NO. CONTENEDOR", 5000),
            (u"KG", 2000),
            (u"CBM", 2000),
            (u"CARGA", 3000),
            (u"ESTATUS", 3000),
            (u"ESTADO", 5000),
            (u"MONTOFLETE", 4000),
            (u"FECHABL", 4000),
            (u"FECHAETA", 4000),
            (u"FECHACEDIS", 4000),
            (u"FECHA PREVENTA", 8000),
            (u"ORIGEN", 4000),
            (u"DESTINO", 4000),
            (u"FWD", 8000),
            (u"FACTURAFWD", 8000),
            (u"FECHAPAGOFWD", 8000),
            (u"BACKORDER", 8000),
            (u"FECHAORIGINAL", 8000),
            (u"PENDIENTES", 8000),
            (u"ESPECIAL", 8000),
            (u"Ptro", 8000),

        ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            # set column width
            ws.col(col_num).width = columns[col_num][1]

        for obj in queryset:
            row_num += 1
            row = [
                obj.REFERENCIA,
                obj.IMPORTEPEDIDO,
                obj.IMPORTEFACTURA,
                obj.CONTENEDORNO,
                obj.KG,
                obj.CBM,
                obj.CARGA,
                obj.ESTATUS,
                obj.ESTADO,
                obj.MONTOFLETE,
                obj.FECHABL,
                obj.FECHAETA,
                obj.FECHACEDIS,
                obj.FECHAPREVENTA,
                obj.ORIGEN,
                obj.DESTINO,
                obj.FWD,
                obj.FACTURAFWD,
                obj.FECHAPAGOFWD,
                obj.NUEVOS,
                obj.MEJORAS,
                obj.OMISIONPREVIOORIGEN,
                obj.ESPECIAL,

            ]
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

    export_xls.short_description = u"Export XLS"

    def export_users_xls(request):
        import xlwt
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.num_format_str = 'dd/MM/yyyy'

        columns = ['REFERENCIA', 'IMPORTEPEDIDO', 'IMPORTEFACTURA', 'CONTENEDORNO', ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)


        rows = Contenedor.objects.all().values_list('REFERENCIA', 'IMPORTEPEDIDO', 'IMPORTEFACTURA', 'CONTENEDORNO')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
    export_users_xls.short_description = u"Otro XLS"

