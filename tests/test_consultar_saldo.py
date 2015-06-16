# -*- coding: utf-8 -*-

from django.test import TestCase
from billetera.controller import consultar_saldo
from billetera.controller import recargar_saldo
from billetera.models import BilleteraElectronica
from billetera.forms import BilleteraElectronicaForm
from billetera.forms import BilleteraRecargaForm
from billetera.forms import PagoRecargaForm
from transacciones.models import *
from billetera.exceptions import *

from decimal import Decimal

class consultar_saldoTestCase(TestCase):
    
    def crearBilletera(self, pin, Saldo):
        bill = BilleteraElectronica(
                nombreUsuario    =  "Nombre",
                apellidoUsuario =  "Apellido",
                cedulaTipo       =  "V",
                cedula           =  123456789,
                PIN              =  pin,
                )
        bill.save()
        
        try:
            recargar_saldo(bill.id, Saldo);
        except:
            pass
        
        return bill
    
    def testconsultaSaldoCero(self):
        
        bill = self.crearBilletera(1234, 0)
        self.assertEqual(consultar_saldo(bill.id), Decimal(0).quantize(Decimal("1.00")))
    
    def testsaldoRegular(self):
        
        bill = self.crearBilletera(1234, 10)
        self.assertEqual(consultar_saldo(bill.id), Decimal(10).quantize(Decimal("1.00")))
    
    # TDD   
    def testConsultaSaldoNoVacio(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id,500)
        self.assertEqual(consultar_saldo(bill.id), Decimal(500).quantize(Decimal("1.00")))        
    
    #borde
    def testRecargaMaxima(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id,10000.00)
        self.assertEqual(consultar_saldo(bill.id), Decimal(10000.00).quantize(Decimal("1.00")))   
    
    #borde
    def testRecargaDesbordada(self):
        
        bill = self.crearBilletera(1234, 99999.99)
        self.assertRaises(Exception, recargar_saldo(bill.id,Decimal(0.01).quantize(Decimal("1.00"))))
        
    #borde
    def testRecargaMinima(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id,Decimal(0.01).quantize(Decimal("1.00")))
        self.assertEqual(consultar_saldo(bill.id), Decimal(0.01).quantize(Decimal("1.00")))
    
    #esquina    
    def testRecargasSeguidasMaxima(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id,5000)
        recargar_saldo(bill.id,5000)
        self.assertEqual(consultar_saldo(bill.id), Decimal(10000.00).quantize(Decimal("1.00")))
        
    #Malicia    
    def testRecargaNula(self):
        
        bill = self.crearBilletera(1234, 500)
        self.assertRaises(MontoCero, recargar_saldo, bill.id, 0)
        self.assertEqual(consultar_saldo(bill.id), Decimal(500).quantize(Decimal("1.00")))        
             
    #Malicia    
    def testRecargaNegativa(self):
        
        bill = self.crearBilletera(1234, 500)
        self.assertRaises(MontoNegativo, recargar_saldo, bill.id, -1)