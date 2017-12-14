from django.shortcuts import render
from django.db import connection
from django.db import connections
from django.http import HttpResponse
import xlwt
from django.contrib.auth.decorators import login_required

@login_required(login_url='/account/login/')
def inicio(request):
    return render(request, 'inicio.html')

@login_required(login_url='/account/login/')
def enforma(request):
    cursor = connections['pizarron1'].cursor()
    cursor.execute("""Select Referencia, Saldo,ID,MovID ,Estatus,CONVERT(VARCHAR(10), FechaRequerida, 105) as FechaRequerida,
       		CONVERT(VARCHAR(10),FechaEntrega,105) as FechaEntrega , Importe, FormaEntrega ,
       		 DATEPART(MONTH,FechaRequerida) AS Mes,
       		 DATEPART(WEEK,  FechaEntrega) as SemanaDelYear,
              DATEPART(WEEK,  FechaRequerida +49) as SemanaMasSiete,
       	   (Select Comentario  From anexomov where id=Compra.id and rama='COMS' And Tipo='Comentario' and Nombre='BACK ORDER') BACKORDER,
       		(Select Comentario From anexomov where id=Compra.id and rama='COMS' And Tipo='Comentario' and Nombre='FECHA ORIGINAL') FECHAORIGINAL,
       		(Select Comentario From anexomov where id=Compra.id and rama='COMS' And Tipo='Comentario' and Nombre='PENDIENTES') PENDIENTES,
       		(Select Comentario From anexomov where id=Compra.id and rama='COMS' And Tipo='Comentario' and Nombre='ESPECIAL') ESPECIAL,
       		(Select count(id) from CompraD where id=Compra.id) PIEZAS,
               (Select Agente from Prov where proveedor=Compra.Proveedor) Agente
       	   from Compra
               where Mov in('Pedido', 'Pedido Excedente')   and Estatus='PENDIENTE'   and FechaEntrega > GETDATE() ORDER BY  SemanaDelYear ASC ,Agente, Referencia""")

    enforma = cursor.fetchall()
    context = {
        "enforma": enforma
    }
    return render(request, 'enforma.html', context)

@login_required(login_url='/account/login/')
def retrasos(request):
    cursor = connections['pizarron1'].cursor()
    cursor.execute("""Select  FechaEntrega,Year(FechaEntrega) as Yeara,Referencia, ID,MovID ,Estatus,CONVERT(VARCHAR(10), 
                FechaRequerida, 105) as FechaRequerida,
    		    CONVERT(VARCHAR(10),FechaEntrega,105) as FechaEntrego , Importe, FormaEntrega ,Saldo,
    			 DATEPART(MONTH,FechaRequerida) AS Mes,
    			 cast(DATEPART(WEEK,  FechaEntrega)as varchar) + '-' + cast(Year(FechaEntrega)as varchar) as SemanaDelYear , 
                DATEPART(WEEK,  FechaRequerida +49 ) as SemanaMasSiete,
                (Select Comentario  From anexomov where id=Compra.id and rama='COMS' And Tipo='Comentario' and Nombre='BACK ORDER') BACKORDER,
                (Select Comentario From anexomov where id=Compra.id and rama='COMS' And Tipo='Comentario' and Nombre='FECHA ORIGINAL') FECHAORIGINAL,
                (Select Comentario From anexomov where id=Compra.id and rama='COMS' And Tipo='Comentario' and Nombre='PENDIENTES') PENDIENTES,
                (Select Comentario From anexomov where id=Compra.id and rama='COMS' And Tipo='Comentario' and Nombre='ESPECIAL') ESPECIAL,
                (Select count(id) from CompraD where id=Compra.id) PIEZAS,
                (Select Agente from Prov where proveedor=Compra.Proveedor) Agente
    	    from Compra
            where Mov in('Pedido', 'Pedido Excedente') and Estatus='PENDIENTE'  and FechaEntrega <  GETDATE() ORDER BY  FechaEntrega DESC, Agente """)
    retrasos = cursor.fetchall()
    context = {
        "retrasos":retrasos
    }
    return render(request, 'retrasos.html', context)



def sqlViewPendientes(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="retrasos.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Semanas')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Fecha Entrega','Agente','Referencia', 'Com del Movimiento','Fecha Requerida',  'Importe', 'Saldo','Forma Entrega', 'Back Order', 'Fecha Original','Pendientes', 'Especial'  ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    cursor = connections['pizarron1'].cursor()
    cursor.execute("""Select CONVERT(VARCHAR (10), FechaEntrega, 105) as FechaEntregaa  ,
    (Select Agente from Prov where proveedor=Compra.Proveedor) Agente,
    Referencia,MovID,
    CONVERT(VARCHAR(10), FechaRequerida, 105) as FechaRequeridaa,
    Importe,Saldo, FormaEntrega,
	(Select Comentario  From anexomov where id=Compra.id and rama='COMS' And Tipo='Comentario' and Nombre='BACK ORDER') BACKORDER,
	(Select Comentario From anexomov where id=Compra.id and rama='COMS' And Tipo='Comentario' and Nombre='FECHA ORIGINAL') FECHAORIGINAL,
	(Select Comentario From anexomov where id=Compra.id and rama='COMS' And Tipo='Comentario' and Nombre='PENDIENTES') PENDIENTES,
	(Select Comentario From anexomov where id=Compra.id and rama='COMS' And Tipo='Comentario' and Nombre='ESPECIAL') ESPECIAL
	from Compra
    where Mov in('Pedido', 'Pedido Excedente') and Estatus='PENDIENTE'   and FechaEntrega < GETDATE() ORDER BY  FechaEntrega DESC """)
    rows  = cursor.fetchall()
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response



def sqlViewenForma(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="enForma.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Semanas')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Fecha Entrega','Agente','Referencia', 'Com del Movimiento','Fecha Requerida',  'Importe', 'Saldo','Forma Entrega', 'Back Order', 'Fecha Original','Pendientes', 'Especial'  ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cursor = connections['pizarron1'].cursor()
    cursor.execute("""Select CONVERT(VARCHAR (10), FechaEntrega, 105) as FechaEntregaa  ,
    (Select Agente from Prov where proveedor=Compra.Proveedor) Agente,
    Referencia,MovID,
    CONVERT(VARCHAR(10), FechaRequerida, 105) as FechaRequerida,
    Importe, Saldo,FormaEntrega,
	(Select Comentario  From anexomov where id=Compra.id and rama='COMS' And Tipo='Comentario' and Nombre='BACK ORDER') BACKORDER,
	(Select Comentario From anexomov where id=Compra.id and rama='COMS' And Tipo='Comentario' and Nombre='FECHA ORIGINAL') FECHAORIGINAL,
	(Select Comentario From anexomov where id=Compra.id and rama='COMS' And Tipo='Comentario' and Nombre='PENDIENTES') PENDIENTES,
	(Select Comentario From anexomov where id=Compra.id and rama='COMS' And Tipo='Comentario' and Nombre='ESPECIAL') ESPECIAL
	from Compra
    where Mov in('Pedido', 'Pedido Excedente') and Estatus='PENDIENTE'   and FechaEntrega > GETDATE() ORDER BY  FechaEntrega ASC """)
    rows = cursor.fetchall()
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

