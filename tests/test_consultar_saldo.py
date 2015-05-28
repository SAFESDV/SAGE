# -*- coding: utf-8 -*-

from django.test import TestCase
from billetera.controller import consultar_saldo
from billetera.models import BilleteraElectronica
from billetera.forms import BilleteraElectronicaForm

from decimal import Decimal

class consultar_saldoTestCase(TestCase):
    
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
    
    def testconsultaSaldoCero(self):
        
        bill = self.crearBilletera(1234, 0)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(0).quantize(Decimal("1.00")))
    
    def testsaldoRegular(self):
        
        bill = self.crearBilletera(1234, 10)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(10).quantize(Decimal("1.00")))
    