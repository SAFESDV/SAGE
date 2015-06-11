# -*- coding: utf-8 -*-

from django.test import TestCase
from billetera.controller import consultar_saldo
from billetera.controller import recargar_saldo
from billetera.models import BilleteraElectronica
from billetera.models import PagoRecargaBilletera
from billetera.forms import BilleteraElectronicaForm
from billetera.forms import BilleteraElectronicaRecargaForm
from billetera.forms import PagoRecargaForm

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
    
    # TDD   
    def testConsultaSaldoNoVacio(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id,500)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(500).quantize(Decimal("1.00")))        
    
    #borde
    def testRecargaMaxima(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id,99999.99)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(99999.99).quantize(Decimal("1.00")))   
    
    #borde
    def testRecargaDesbordada(self):
        
        bill = self.crearBilletera(1234, 99999.99)
        self.assertRaises(Exception, recargar_saldo(bill.id,Decimal(0.01).quantize(Decimal("1.00"))))
        
    #borde
    def testRecargaMinima(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id,Decimal(0.01).quantize(Decimal("1.00")))
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(0.01).quantize(Decimal("1.00")))
    
    #esquina    
    def testRecargasSeguidasMaxima(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id,50000)
        recargar_saldo(bill.id,49999.99)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(99999.99).quantize(Decimal("1.00")))
        
    #Malicia    
    def testRecargaNula(self):
        
        bill = self.crearBilletera(1234, 500)
        recargar_saldo(bill.id,0)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(500).quantize(Decimal("1.00")))        
             
    #Malicia    
    def testRecargaNegativa(self):
        
        bill = self.crearBilletera(1234, 500)
        self.assertRaises(Exception, recargar_saldo(bill.id,-1))