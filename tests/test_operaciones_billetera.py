# -*- coding: utf-8 -*-

from django.test import TestCase
from billetera.controller import consultar_saldo
from billetera.controller import recargar_saldo
from billetera.controller import consumir_saldo
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
    
    #TDD consulta
    def testconsultaSaldoCero(self):
        
        bill = self.crearBilletera(1234, 0)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(0).quantize(Decimal("1.00")))
        
    #TDD consulta
    def testsaldoRegular(self):
        
        bill = self.crearBilletera(1234, 10)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(10).quantize(Decimal("1.00")))
    
    # TDD recargar   
    def testConsultaSaldoNoVacio(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id,500)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(500).quantize(Decimal("1.00")))        
    
    #borde
    def testRecargaMaxima(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id,9999.99)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(9999.99).quantize(Decimal("1.00")))   
    
    #esquina
    def testRecargaDesbordada(self):
        
        bill = self.crearBilletera(1234, 10000.00)
        recargar_saldo(bill.id, 0.01)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(10000.00).quantize(Decimal("1.00")))
    #borde
    def testRecargaMinima(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id,Decimal(0.01).quantize(Decimal("1.00")))
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(0.01).quantize(Decimal("1.00")))
    
    #esquina    
    def testRecargasSeguidasMaxima(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id,5000)
        recargar_saldo(bill.id,4999.99)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(9999.99).quantize(Decimal("1.00")))
        
    #Malicia    
    def testRecargaNula(self):
        
        bill = self.crearBilletera(1234, 500)
        recargar_saldo(bill.id,0)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(500).quantize(Decimal("1.00")))        
             
    #Malicia    
    def testRecargaNegativa(self):
        
        bill = self.crearBilletera(1234, 500)
        self.assertRaises(Exception, recargar_saldo(bill.id,-1))
    
    #TDD consumir
    def testConsumoCero(self):
        
        bill = self.crearBilletera(1234, 500)
        self.assertRaises(Exception, consumir_saldo(bill.id,0))
        
    #TDD consumir
    def testConsumoMinimoPositivo(self):
        
        bill = self.crearBilletera(1234, 500)
        consumir_saldo(bill.id,0.01)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(499.99).quantize(Decimal("1.00")))
        
    #TDD consumir
    def testConsumirTodo(self):
        
        bill = self.crearBilletera(1234, 500)
        consumir_saldo(bill.id,500)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(0).quantize(Decimal("1.00")))
    
    #Borde
    def testConsumirHastaSaldoPositivoMinimo(self):
        
        bill = self.crearBilletera(1234, 500)
        consumir_saldo(bill.id,499.99)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(0.01).quantize(Decimal("1.00")))
        
    #Borde
    def testConsumirDeMasConDiferenciaMinima(self):
        
        bill = self.crearBilletera(1234, 500)
        self.assertFalse(Exception, consumir_saldo(bill.id,500.01))
        
    #Malicia
    def testConsumirNegativo(self):
        
        bill = self.crearBilletera(1234, 500)
        self.assertFalse(Exception, consumir_saldo(bill.id,-1))
        
    #Esquina
    def testConsumirRegularTeniendoSaldoMaximo(self):
        
        bill = self.crearBilletera(1234, 10000)
        consumir_saldo(bill.id,500)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(9500).quantize(Decimal("1.00")))
        
    #Borde
    def testConsumirSaldoMaximoSinTenerSaldoMaximo(self):
        
        bill = self.crearBilletera(1234, 100)
        self.assertFalse(Exception, consumir_saldo(bill.id,10000))

    #Esquina
    def testConsumirSaldoMaximoTeniendoSaldoMaximo(self):
        
        bill = self.crearBilletera(1234, 10000)
        consumir_saldo(bill.id,10000)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(0).quantize(Decimal("1.00")))
                    
    #TDD consumir
    def testConsumoRegular(self):
        
        bill = self.crearBilletera(1234, 500)
        consumir_saldo(bill.id,300)
        self.assertEqual(consultar_saldo(bill.id,1234), Decimal(200).quantize(Decimal("1.00")))   