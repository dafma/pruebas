from django.db import models
from datetime import datetime, timedelta


ESTADOS_CHOICES = (
    ('PENDIENTE', 'PENDIENTE'),
    ('CONCLUIDO', 'CONCLUIDO')

)
ESTADOSP_CHOICES = (
    ('ECP', 'ETA-CEDIS-PVTA'),
    ('ADUANA', 'ADUANA'),
    ('ARRIBADO', 'ARRIBADO'),
    ('PAGPED', 'PAGPED'),
    ('SOL', 'SOL'),
    ('GONDOLA', 'GONDOLA'),
    ('ENRUTA', 'ENRUTA'),
    ('PENTACO', 'PENTACO'),
    ('SEMANA', 'SEMANA'),
)

PORCENTAJE_CHOICES = (
    ("0%", " 0%"),
    ("5%", " 5%"),
    ("10%", " 10%"),
    ("15%", " 15%"),
    ("20%", " 20%"),
    ("25%", " 25%"),
    ("30%", " 30%"),
    ("35%", " 35%"),
    ("40%", " 40%"),
    ("45%", " 45%"),
    ("50%", " 50%"),
    ("55%", " 55%"),
    ("60%", " 60%"),
    ("65%", " 65%"),
    ("70%", " 70%"),
    ("75%", " 75%"),
    ("80%", " 80%"),
    ("85%", " 85%"),
    ("90%", " 90%"),
    ("95%", " 95%"),
    ("100%", " 100%")
)

CARGA_CHOICES = (
    ("20DC", " 20DC"),
    ("40DC", " 40DC"),
    ("40HQ", " 40HQ")
)

DESTINO_CHOICES = (
    ("MANZANILLO", " MANZANILLO"),
    ("LAZARO", " LAZARO"),
    ("VERACRUZ", " VERACRUZ"),
    )

ORIGEN_CHOICES = (
    ("NINGBO", " NINGBO"),
    ("SHANGHAI", " SHANGHAI"),
    ("QINGDAO", " QINGDAO"),
    ("WUHU", " WUHU"),
    ("CHANGZHOU", " CHANGZHOU"),
    ("ARGENTINA", " ARGENTINA"),
    ("BRASIL", " BRASIL"),
    ("INDIA", " INDIA"),
    ("TURQUIA", " TURQUIA"),
)

FWD_CHOICES = (
    ("GEOCARGO", " GEOCARGO"),
    ("PLUSCARGO", " PLUSCARGO"),
    ("SCHNELLER", " SCHNELLER"),
    ("DRAGONCARGO", " DRAGONCARGO"),
    ("GLOMEX", " GLOMEX"),
    ("HAMBURG", " HAMBURG"),
    ("HAPAG-LLOYD", " HAPAG-LLOYD"),
    ("HELLMANN", " HELLMANN"),
    ("NA", " NA"),
)

class Contenedor(models.Model):
    REFERENCIA = models.CharField(max_length=200, null=True, blank=True)
    FECHACREACION = models.DateField("FECHA CREACIÓN", auto_now_add=True)
    IMPORTEPEDIDO = models.DecimalField("IMPORTE PEDIDO", max_digits=10, decimal_places=2, null=True, blank=True)
    IMPORTEFACTURA = models.DecimalField("IMPORTE FACTURA", max_digits=10, decimal_places=2, null=True, blank=True)
    CONTENEDORNO = models.CharField("NO. CONTENEDOR", max_length=20, null=True, blank=True)
    KG = models.DecimalField("KILOGRAMOS", max_digits=7, decimal_places=2, null=True, blank=True)

    # consolidados
    KGPCONSOLIDADO = models.SmallIntegerField("% KG CONSOLIDADO", null=True, blank=True)
    CBMPCONSOLIDADO = models.SmallIntegerField("% CBM CONSOLIDADO", null=True, blank=True)
    MONTOPCONSOLIDADO = models.SmallIntegerField("% IMPORTE FACTURA CONSOLIDADO", null=True, blank=True)

    CBM = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    CARGA = models.CharField(choices=CARGA_CHOICES, max_length=4, null=True, blank=True)
    ESTATUS = models.CharField(max_length=9, choices=ESTADOS_CHOICES, null=True, blank=True, default='PENDIENTE')
    ESTADO = models.CharField(max_length=20, null=True, blank=True, choices=ESTADOSP_CHOICES)
    MONTOFLETE = models.DecimalField("MONTO FLETE", max_digits=10, decimal_places=2, null=True, blank=True)

    # feha eta cedis y bl
    FECHABL = models.DateField("FECHA BL", null=True, blank=True)
    FECHAETA = models.DateField("FECHA ETA", null=True, blank=True)
    FECHACEDIS = models.DateField("FECHA CEDIS",  null=True, blank=True)
    FECHAPREVENTA = models.DateField("FECHA PREVENTA", null=True, blank=True)

    FECHASEMANA = models.DateField("FECHA SEMANA", null=True, blank=True)
    ORIGEN = models.CharField("ORIGEN", choices=ORIGEN_CHOICES, max_length=10, null=True, blank=True)
    DESTINO = models.CharField("DESTINO", choices=DESTINO_CHOICES, max_length=10, null=True, blank=True)
    CONTENEDORNO = models.CharField("NO. CONTENEDOR", max_length=20, null=True, blank=True)
    FWD = models.CharField("FWD", choices=FWD_CHOICES, max_length=20, null=True, blank=True)
    FACTURAFWD = models.CharField("FACTURA FWD", max_length=30, null=True, blank=True)
    FECHAPAGOFWD = models.DateField("FECHA PAGO FWD", null=True, blank=True)

    #BACKORDER = models.TextField(null=True, blank=True)
    #FECHAORIGINAL = models.TextField(null=True, blank=True)
    #PENDIENTES = models.TextField(null=True, blank=True)
    #ESPECIAL = models.TextField(null=True, blank=True)

    NUEVOS = models.TextField(null=True, blank=True)
    MEJORAS = models.TextField(null=True, blank=True)
    OMISIONPREVIOORIGEN = models.TextField(null=True, blank=True)
    ESPECIAL = models.TextField(null=True, blank=True)

    # fecha creacion = FC
    FCECP = models.DateField(null=True, blank=True)
    FCADUANA = models.DateField(null=True, blank=True)
    FCARRIBADO = models.DateField(null=True, blank=True)
    FCPAGPED = models.DateField(null=True, blank=True)
    FCSOL = models.DateField(null=True, blank=True)
    FCGONDOLA = models.DateField(null=True, blank=True)
    FCENRUTA = models.DateField(null=True, blank=True)
    FCPENTACO = models.DateField(null=True, blank=True)
    FCSEMANA = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.REFERENCIA

    def get_importefactura(self):
        importefactura = sum(item.IMPORTEFACTURA for item in self.contenedorr.all())
        return importefactura

    def get_importepedido(self):
        importepedido = sum(item.IMPORTEPEDIDO for item in self.contenedorr.all())
        return importepedido

    def get_kg_total(self):
        kg = sum(item.KG for item in self.contenedorr.all())
        return kg

    def get_cbm(self):
        cbm = sum(item.CBM for item in self.contenedorr.all())
        return cbm

    def get_porcentaje(self):
        contenedor_20DC_peso = 25200
        contenedor_40DC_peso = 24800
        contenedor_40HQ_peso = 24600

        contenedor_20DC_volumen = 30
        contenedor_40DC_volumen = 65
        contenedor_40HQ_volumen = 73

        contenedor_20DC_monto = 60000
        contenedor_40DC_monto = 90000
        contenedor_40HQ_monto = 90000

        contenedor = self.CARGA
        kg = self.KG
        cbm = self.CBM
        monto = self.IMPORTEFACTURA

        if contenedor == "20DC":
            x = kg * 100
            porcentaje_consolidado = x / contenedor_20DC_peso
            a = ("{0:10.0f}".format(porcentaje_consolidado, 1))

            # cbm
            z = cbm * 100
            cbm_porcentaje_consolidado = z / contenedor_20DC_volumen
            b = ("{0:10.0f}".format(cbm_porcentaje_consolidado, 1))

            # monto
            y = monto * 100
            monto_porcentaje_consolidado = y / contenedor_20DC_monto
            c = ("{0:10.0f}".format(monto_porcentaje_consolidado, 1))
            return a, b, c

        if contenedor == "40DC":
            x = kg * 100
            porcentaje_consolidado = x / contenedor_40DC_peso
            a = ("{0:10.0f}".format(porcentaje_consolidado))

            # cbm
            z = cbm * 100
            cbm_porcentaje_consolidado = z / contenedor_40DC_volumen
            b = ("{0:10.0f}".format(cbm_porcentaje_consolidado, 1))

            # monto
            y = monto * 100
            monto_porcentaje_consolidado = y / contenedor_40DC_monto
            c = ("{0:10.0f}".format(monto_porcentaje_consolidado, 1))
            return a, b, c

        if contenedor == "40HQ":
            x = kg * 100
            porcentaje_consolidado = x / contenedor_40HQ_peso
            a = ("{0:10.0f}".format(porcentaje_consolidado))

            # cbm
            z = cbm * 100
            cbm_porcentaje_consolidado = z / contenedor_40HQ_volumen
            b = ("{0:10.0f}".format(cbm_porcentaje_consolidado, 1))

            # monto
            y = monto * 100
            monto_porcentaje_consolidado = y / contenedor_40HQ_monto
            c = ("{0:10.0f}".format(monto_porcentaje_consolidado, 1))
            return a, b, c

    def get_ecp(self):
        fecha_bl = self.FECHABL
        # fecha_bl = datetime.strptime(s, "%Y/%m/%d")
        puerto_destino = self.ORIGEN  # NINGBO SHANGHAI QINGDAO WUHU CHANGZHOU ARGENTINA BRASIL INDIA TURQUIA

        ningbo_eta = timedelta(days=19)
        nigbo_cedis = timedelta(days=10)

        shanghai_eta = timedelta(days=17)
        shanghai_cedis = timedelta(days=10)

        quingdao_eta = timedelta(days=25)
        quingdao_cedis = timedelta(days=10)

        wuhu_eta = timedelta(days=23)
        wuhu_cedis = timedelta(days=10)

        changzhou_eta = timedelta(days=27)
        changzhou_cedis = timedelta(days=10)

        argentina_eta = timedelta(days=30)
        argentina_cedis = timedelta(days=7)

        brasil_eta = timedelta(days=21)
        brasil_cedis = timedelta(days=7)

        india_eta = timedelta(days=47)
        india_cedis = timedelta(days=7)

        turquia_eta = timedelta(days=39)
        turquia_cedis = timedelta(days=7)

        if "NINGBO" == puerto_destino:
            print("si entro")

            def siguiente_martes(fecha_cedis, weekday):
                days_ahead = weekday - fecha_cedis.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                return fecha_cedis + timedelta(days_ahead)

            fecha_eta = fecha_bl + ningbo_eta
            fecha_cedis = fecha_eta + nigbo_cedis
            fecha_preventa = siguiente_martes(fecha_cedis, 1)

        if "SHANGHAI" == puerto_destino:
            def siguiente_martes(fecha_cedis, weekday):
                days_ahead = weekday - fecha_cedis.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                return fecha_cedis + timedelta(days_ahead)

            fecha_eta = fecha_bl + shanghai_eta
            fecha_cedis = fecha_eta + shanghai_cedis
            fecha_preventa = siguiente_martes(fecha_cedis, 1)

        if "QINGDAO" == puerto_destino:
            def siguiente_martes(fecha_cedis, weekday):
                days_ahead = weekday - fecha_cedis.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                return fecha_cedis + timedelta(days_ahead)

            fecha_eta = fecha_bl + quingdao_eta
            fecha_cedis = fecha_eta + quingdao_cedis
            fecha_preventa = siguiente_martes(fecha_cedis, 1)

        if "WUHU" == puerto_destino:
            def siguiente_martes(fecha_cedis, weekday):
                days_ahead = weekday - fecha_cedis.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                return fecha_cedis + timedelta(days_ahead)

            fecha_eta = fecha_bl + wuhu_eta
            fecha_cedis = fecha_eta + wuhu_cedis
            fecha_preventa = siguiente_martes(fecha_cedis, 1)

        if "CHANGZHOU" == puerto_destino:
            def siguiente_martes(fecha_cedis, weekday):
                days_ahead = weekday - fecha_cedis.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                return fecha_cedis + timedelta(days_ahead)

            fecha_eta = fecha_bl + changzhou_eta
            fecha_cedis = fecha_eta + changzhou_cedis
            fecha_preventa = siguiente_martes(fecha_cedis, 1)

        if "ARGENTINA" == puerto_destino:
            def siguiente_martes(fecha_cedis, weekday):
                days_ahead = weekday - fecha_cedis.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                return fecha_cedis + timedelta(days_ahead)

            fecha_eta = fecha_bl + argentina_eta

            fecha_cedis = fecha_eta + argentina_cedis
            fecha_preventa = siguiente_martes(fecha_cedis, 1)

        if "BRASIL" == puerto_destino:
            def siguiente_martes(fecha_cedis, weekday):
                days_ahead = weekday - fecha_cedis.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                return fecha_cedis + timedelta(days_ahead)

            fecha_eta = fecha_bl + brasil_eta
            fecha_cedis = fecha_eta + brasil_cedis
            fecha_preventa = siguiente_martes(fecha_cedis, 1)

        if "INDIA" == puerto_destino:
            def siguiente_martes(fecha_cedis, weekday):
                days_ahead = weekday - fecha_cedis.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                return fecha_cedis + timedelta(days_ahead)

            fecha_eta = fecha_bl + india_eta
            fecha_cedis = fecha_eta + india_cedis
            fecha_preventa = siguiente_martes(fecha_cedis, 1)

        if "TURQUIA" == puerto_destino:
            def siguiente_martes(fecha_cedis, weekday):
                days_ahead = weekday - fecha_cedis.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                return fecha_cedis + timedelta(days_ahead)

            fecha_eta = fecha_bl + turquia_eta
            fecha_cedis = fecha_eta + turquia_cedis
            fecha_preventa = siguiente_martes(fecha_cedis, 1)

        return fecha_eta, fecha_cedis, fecha_preventa

    def save(self, *args, **kwargs):
        self.KG = self.get_kg_total()
        self.CBM = self.get_cbm()
        self.IMPORTEFACTURA = self.get_importefactura()
        self.IMPORTEPEDIDO = self.get_importepedido()
        fun_consolidado = self.get_porcentaje()

        self.KGPCONSOLIDADO = fun_consolidado[0]
        self.CBMPCONSOLIDADO = fun_consolidado[1]
        self.MONTOPCONSOLIDADO = fun_consolidado[2]

        #fun = self.get_ecp()
        #self.FECHAETA = fun[0]
        #self.FECHACEDIS = fun[1]
        #self.FECHAPREVENTA = fun[2]
        super(Contenedor, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Contenedor"
        verbose_name_plural = "Contenedor"


class Referencia(models.Model):
    IDMOV = models.IntegerField(null=True, blank=True)
    REFERENCIA = models.CharField( max_length=20, null=True, blank=True)
    IMPORTEPEDIDO = models.DecimalField("IMPORTE PEDIDO",max_digits=10, decimal_places=2)
    ESTAENPAGO = models.CharField("ESTA EN PAGO", max_length=20, null=True, blank=True)
    IMPORTEFACTURA = models.DecimalField("IMPORTE FACTURA", max_digits=10, decimal_places=2)
    FECHAPEDIDO = models.DateField("FECHA PEDIDO", null=True, blank=True)
    FECHATENTENTREGA = models.DateField("FECHA TENT. ENTREGA", null=True, blank=True)
    KG = models.DecimalField(max_digits=7, decimal_places=2)
    CBM = models.DecimalField(max_digits=10, decimal_places=3)
    CARGA = models.CharField(max_length=10, null=True, blank=True)
    PDELCONTENEDOR = models.CharField("% DEL CONTENEDOR", max_length=20, null=True, blank=True)
    PVALORFACTURA = models.CharField("% VALOR FACTURA", max_length=20, null=True, blank=True)
    PESO = models.CharField("% PESO", max_length=20, null=True, blank=True)
    PCBM = models.CharField("% CBM", max_length=20, null=True, blank=True)
    contenedor = models.ForeignKey("CONTENEDOR", Contenedor,  related_name='contenedorr', null=True, blank=True)

    def __str__(self):
        return self.REFERENCIA

    class Meta:
        verbose_name = "Contnedor"
        verbose_name_plural = "Contenedor"


