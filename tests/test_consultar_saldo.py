# -*- coding: utf-8 -*-

from django.test import TestCase
from estacionamientos.controller import consultar_saldo
from estacionamientos.controller import recargar_saldo
from estacionamientos.models import BilleteraElectronica
from estacionamientos.models import PagoRecargaBilletera
from estacionamientos.forms import BilleteraElectronicaForm
from estacionamientos.forms import BilleteraElectronicaRecargaForm
from estacionamientos.forms import PagoRecargaForm

from decimal import Decimal

class consultar_saldoTestCase(TestCase):
    
    # TDD
    def crearBilletera(self, pin, Saldo):
        bill = BilleteraElectronica(
                nombreUsuario    =  "Nombre",
                apellidoUsuario =  "Apellido",
                cedulaTipo       =  "V",
                cedula           =  123456789,
                PIN              =  pin,
                saldo            =  Saldo
                )
        bill.save()
        return bill
    
    # TDD
    def testconsultaSaldoCero(self):
        
        bill = self.crearBilletera(1234, 0)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(0).quantize(Decimal("1.00")))
    
    # TDD
    def testsaldoRegular(self):
        
        bill = self.crearBilletera(1234, 10)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(10).quantize(Decimal("1.00")))
    # TDD   
    def testConsultaSaldoNoVacio(self):
        
        bill = self.crearBilletera(1234, 10)
        recargar_saldo(bill.id,500)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(500).quantize(Decimal("1.00")))        
    
    