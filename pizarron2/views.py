from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
import time
from .models import Contenedor
from django.contrib.auth.decorators import login_required


@login_required(login_url='/account/login/')
def index(request):
    """
    ecp = Contenedor.objects.filter(ESTADO='ECP', ESTATUS='PENDIENTE').extra(
                                            select={'diaDeLaSemana': "DATEPART(WEEKDAY, FECHAPREVENTA)",
                                                    'ecpAduana': "DATEDIFF(DAY,FCECP, FCADUANA)",
                                                    'IDENTIFICADORECP': " CONCAT(CONVERT(VARCHAR(10), FECHAETA, 105),'-',CONVERT(VARCHAR(10),FECHACEDIS, 105),'-',CONVERT(VARCHAR(10), FECHAPREVENTA, 105) ) ",
                                                    'hoy': "getdate()"}).order_by('-IDENTIFICADORECP')
    """                                                

    ecp = Contenedor.objects.filter(ESTADO='ECP', ESTATUS='PENDIENTE').extra(
        select={'diaDeLaSemana': "DATEPART(WEEKDAY, FECHAPREVENTA)",
                'ecpAduana': "DATEDIFF(DAY,FCECP, FCADUANA)",
                
'IDENTIFICADORECP': " cast(CONVERT(VARCHAR(10), FECHAETA, 105) as varchar)+'-'+ cast(CONVERT(VARCHAR(10), FECHACEDIS, 105)as varchar)+'-' +cast(CONVERT(VARCHAR(10), FECHAPREVENTA,105) as varchar )",
     'hoy': "getdate()"}).order_by('-IDENTIFICADORECP')

    aduana = Contenedor.objects.filter(ESTADO='ADUANA', ESTATUS='PENDIENTE').extra(
                                            select={'diaDeLaSemana': "DATEPART(WEEKDAY, FECHAPREVENTA)",
                                                    'ecpAduana': "DATEDIFF(DAY,FCECP, FCADUANA)",
                                                    'hoy': "getdate()"})

    arribado = Contenedor.objects.filter(ESTADO='ARRIBADO', ESTATUS='PENDIENTE').extra(
                                            select={'diaDeLaSemana': "DATEPART(WEEKDAY, FECHAPREVENTA)",
                                                    'ecpAduana': "DATEDIFF(DAY,FCECP, FCADUANA)",
                                                    'aduanaArribado': "DATEDIFF(DAY,FCADUANA, FCARRIBADO)",
                                                    'hoy': "getdate()"})

    pagped = Contenedor.objects.filter(ESTADO='PAGPED', ESTATUS='PENDIENTE').extra(
                                            select={'diaDeLaSemana': "DATEPART(WEEKDAY, FECHAPREVENTA)",
                                                    'ecpAduana': "DATEDIFF(DAY,FCECP, FCADUANA)",
                                                    'aduanaPagped': "DATEDIFF(DAY,FCADUANA, FCPAGPED)",
                                                    'hoy': "getdate()"})

    sol = Contenedor.objects.filter(ESTADO='SOL', ESTATUS='PENDIENTE').extra(
                                            select={'diaDeLaSemana': "DATEPART(WEEKDAY, FECHAPREVENTA)",
                                                    'ecpAduana': "DATEDIFF(DAY,FCECP, FCADUANA)",
                                                    'aduanaSol': "DATEDIFF(DAY,FCADUANA, FCSOL)",
                                                    'hoy': "getdate()"})

    gondola = Contenedor.objects.filter(ESTADO='GONDOLA', ESTATUS='PENDIENTE').extra(
                                            select={'diaDeLaSemana': "DATEPART(WEEKDAY, FECHAPREVENTA)",
                                                    'ecpAduana': "DATEDIFF(DAY,FCECP, FCADUANA)",
                                                    'aduanaArribado': "DATEDIFF(DAY,FCADUANA, FCARRIBADO)",
                                                    'aduanaPagped': "DATEDIFF(DAY,FCADUANA, FCPAGPED)",
                                                    'aduanaSol': "DATEDIFF(DAY,FCADUANA, FCSOL)",
                                                    'arribadoGondola': "DATEDIFF(DAY,FCARRIBADO, FCGONDOLA)",
                                                    'pagpedGondola': "DATEDIFF(DAY,FCPAGPED, FCGONDOLA)",
                                                    'solGondola': "DATEDIFF(DAY,FCSOL, FCGONDOLA)",
                                                    'arribadoPentaco': "DATEDIFF(DAY,FCARRIBADO, FCPENTACO)",
                                                    'pagpedPentaco': "DATEDIFF(DAY,FCPAGPED, FCPENTACO)",
                                                    'solPentaco': "DATEDIFF(DAY,FCSOL, FCPENTACO)",
                                                    'hoy': "getdate()"})

    pentaco = Contenedor.objects.filter(ESTATUS='PENDIENTE', ESTADO='PENTACO').extra(
                                            select={'diaDeLaSemana': "DATEPART(WEEKDAY, FECHAPREVENTA)",
                                                    'ecpAduana': "DATEDIFF(DAY,FCECP, FCADUANA)",
                                                    'aduanaArribado': "DATEDIFF(DAY,FCADUANA, FCARRIBADO)",
                                                    'aduanaPagped': "DATEDIFF(DAY,FCADUANA, FCPAGPED)",
                                                    'aduanaSol': "DATEDIFF(DAY,FCADUANA, FCSOL)",
                                                    'arribadoGondola': "DATEDIFF(DAY,FCARRIBADO, FCGONDOLA)",
                                                    'pagpedGondola': "DATEDIFF(DAY,FCPAGPED, FCGONDOLA)",
                                                    'solGondola': "DATEDIFF(DAY,FCSOL, FCGONDOLA)",
                                                    'arribadoPentaco': "DATEDIFF(DAY,FCARRIBADO, FCPENTACO)",
                                                    'pagpedPentaco': "DATEDIFF(DAY,FCPAGPED, FCPENTACO)",
                                                    'solPentaco': "DATEDIFF(DAY,FCSOL, FCPENTACO)",
                                                    'hoy': "getdate()"})

    semana = Contenedor.objects.filter(ESTATUS='PENDIENTE', ESTADO='SEMANA').extra(
                                            select={'diaDeLaSemana': "DATEPART(WEEKDAY, FECHAPREVENTA)",
                                                    'ecpAduana': "DATEDIFF(DAY,FCECP, FCADUANA)",
                                                    'aduanaArribado': "DATEDIFF(DAY,FCADUANA, FCARRIBADO)",
                                                    'aduanaPagped': "DATEDIFF(DAY,FCADUANA, FCPAGPED)",
                                                    'aduanaSol': "DATEDIFF(DAY,FCADUANA, FCSOL)",
                                                    'arribadoGondola': "DATEDIFF(DAY,FCARRIBADO, FCGONDOLA)",
                                                    'pagpedGondola': "DATEDIFF(DAY,FCPAGPED, FCGONDOLA)",
                                                    'solGondola': "DATEDIFF(DAY,FCSOL, FCGONDOLA)",
                                                    'arribadoPentaco': "DATEDIFF(DAY,FCARRIBADO, FCPENTACO)",
                                                    'pagpedPentaco': "DATEDIFF(DAY,FCPAGPED, FCPENTACO)",
                                                    'solPentaco': "DATEDIFF(DAY,FCSOL, FCPENTACO)",
                                                    'gondolaSemana': "DATEDIFF(DAY,FCGONDOLA, FCSEMANA)",
                                                    'pentacoSemana': "DATEDIFF(DAY,FCPENTACO, FCSEMANA)",
                                                    'ordenDiaSemana': "DATEPART(DW,FECHASEMANA)",
                                                    'hoy': "getdate()"}).order_by('ordenDiaSemana')
    semanadelanio = time.strftime("%W")
    diadelmes = time.strftime("%d")
    diadelasemana = time.strftime("%w")
    suma = int(diadelmes) - int(diadelasemana)
    lunes = suma + 1
    viernes = lunes + 4
    lunesviernes = str(lunes) + '-' + str(viernes)
    ard = str(lunesviernes)
    nombremes = time.strftime("%b")
    context = {
        "ecp": ecp,
        "aduana": aduana,
        "arribado": arribado,
        "pagped": pagped,
        "sol": sol,
        "gondola": gondola,
        "pentaco": pentaco,
        "semana": semana,
        "asemana": semanadelanio,
        "lunesviernes": ard,
        "nombremes": nombremes
    }

    return render(request, 'panel2.html', context)

"""
def mygetview(request):
    if request.method == 'GET':
        print("**get**")
        data = request.GET['mydata']
        astr = "<html><b> you sent a get request </b> <br> returned data: %s</html>" % data
        return HttpResponse(astr)
    return render(request)
"""


def excel_pendientes(request):
    import xlwt
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Grafico_Pizarròn2')

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.num_format_str = '$#,##0.00'
    font_style.num_format_str = 'dd/mm/yyyy'
    columns = ['Referencia', 'Importe Pedido', 'Importe Factura', 'KG', 'CBM', 'Carga',
               'Estatus', 'Estado', 'Monto Flete', 'Fecha BL', 'Fecha ETA', 'Fecha Cedis', 'Fecha Preventa', 'Origen',
               'Destino', 'FWD', 'Factura FWD', 'Fecha Pago FWD ']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    sql = """ Select REFERENCIA, IMPORTEPEDIDO,IMPORTEFACTURA, KG,CBM,CARGA ,ESTATUS,ESTADO,MONTOFLETE,FECHABL,FECHAETA,
              FECHACEDIS,FECHAPREVENTA,ORIGEN,DESTINO,CONTENEDORNO,FWD,FACTURAFWD,FECHAPAGOFWD
              from app_contenedor WHERE ESTATUS='PENDIENTE'
          """
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response
