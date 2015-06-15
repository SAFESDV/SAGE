# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from billetera.controller import consultar_saldo
from billetera.controller import recargar_saldo
from billetera.controller import consumir_saldo
from billetera.models import BilleteraElectronica
from billetera.exceptions import *

from decimal import Decimal

class consultar_saldoTestCase(TestCase):
    
    def crearBilletera(self, pin, Saldo):
        bill = BilleteraElectronica(
                nombreUsuario    =  "Nombre",
                apellidoUsuario =  "Apellido",
                cedulaTipo       =  "V",
                cedula           =  123456789,
                PIN              =  pin
                )
        bill.save()
        
        try:
            recargar_saldo(bill.id, Saldo);
        except:
            pass
        
        return bill
    
    ###################################################################
    #                 CONSULTAR SALDO                                 #
    ###################################################################
    
    #TDD consulta
    def testconsultaSaldoCero(self):
        
        bill = self.crearBilletera(1234, 0)
        self.assertEqual(consultar_saldo(bill.id), Decimal(0).quantize(Decimal("1.00")))
        
    #TDD consulta
    def testsaldoRegular(self):
        
        bill = self.crearBilletera(1234, 10)
        self.assertEqual(consultar_saldo(bill.id), Decimal(10).quantize(Decimal("1.00")))
        
    #Malicia
    def testConsumirNoID(self):
        
       self.assertRaises(BilleteraElectronica.DoesNotExist, consultar_saldo(2000))
    
    
    ###################################################################
    #                     RECARGAR SALDO                              #
    ###################################################################
    
    # TDD recargar   
    def testConsultaSaldoNoVacio(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id,500)
        self.assertEqual(consultar_saldo(bill.id), Decimal(500).quantize(Decimal("1.00")))        
    
    #borde
    def testRecargaMaxima(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id,10000.00)
        self.assertEqual(consultar_saldo(bill.id), Decimal(10000.00).quantize(Decimal("1.00")))   
    
    #esquina
    def testRecargaDesbordada(self):
        
        bill = self.crearBilletera(1234, 10000.00)
        try:
            recargar_saldo(bill.id, 0.01)
        except:
            pass
        self.assertEqual(consultar_saldo(bill.id), Decimal(10000.00).quantize(Decimal("1.00")))
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

    #Malicia
    def testConsultarNoID(self):
        
       self.assertRaises(AutenticacionDenegada, consultar_saldo, 2000, 1)
    
       
    ###################################################################
    #                      CONSUMIR SALDO                             # 
    ###################################################################
    
    #TDD consumir
    def testConsumoRegular(self):
        
        bill = self.crearBilletera(1234, 500)
        consumir_saldo(bill.id,300)
        self.assertEqual(consultar_saldo(bill.id), Decimal(200).quantize(Decimal("1.00")))   
            
    #TDD consumir/borde
    def testConsumoCero(self):
        
        bill = self.crearBilletera(1234, 500)
        self.assertRaises(MontoCero, consumir_saldo, bill.id, 0)
        self.assertEqual(consultar_saldo(bill.id), Decimal(500).quantize(Decimal("1.00")))
        
    #TDD consumir/borde
    def testConsumoMinimoPositivo(self):
        
        bill = self.crearBilletera(1234, 500)
        consumir_saldo(bill.id,0.01)
        self.assertEqual(consultar_saldo(bill.id), Decimal(499.99).quantize(Decimal("1.00")))
        
    #TDD consumir/borde
    def testConsumirTodo(self):
        
        bill = self.crearBilletera(1234, 500)
        consumir_saldo(bill.id,500)
        self.assertEqual(consultar_saldo(bill.id), Decimal(0).quantize(Decimal("1.00")))
    
    #Malicia
    def testConsumirNegativo(self):
        
        bill = self.crearBilletera(1234, 500)
        self.assertRaises(MontoNegativo, consumir_saldo, bill.id, -0.01)
        self.assertEqual(consultar_saldo(bill.id), Decimal(500).quantize(Decimal("1.00")))
        
    #Malicia
    def testConsultarNoID(self):
        
       self.assertRaises(AutenticacionDenegada, consumir_saldo, 2000, 1)
    
    
    ###################################################################
    #               PROPIEDADES OPERACIONES BILLETERA                 # 
    ###################################################################
    
    #Borde
    def testConsumirHastaSaldoPositivoMinimo(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id, 500)
        consumir_saldo(bill.id,499.99)
        self.assertEqual(consultar_saldo(bill.id), Decimal(0.01).quantize(Decimal("1.00")))
        
    #Malicia
    def testConsumirEnExcesoMaximo(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id, 10000)
        self.assertRaises(SaldoNegativo, consumir_saldo, bill.id, 10000.01)
        self.assertEqual(consultar_saldo(bill.id), Decimal(10000).quantize(Decimal("1.00")))
        
    #Esquina
    def testRecargaMaximaConsumoMinimo(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id, 10000)
        consumir_saldo(bill.id, 0.01)
        self.assertEqual(consultar_saldo(bill.id), Decimal(9999.99).quantize(Decimal("1.00")))
        
    #Esquina
    def testConsumirSaldoMaximoSinTenerSaldoMaximo(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id, 9999.99)
        self.assertRaises(SaldoNegativo, consumir_saldo, bill.id, 10000)
        self.assertEqual(consultar_saldo(bill.id), Decimal(9999.99).quantize(Decimal("1.00")))

    #Esquina
    def testConsumirSaldoMaximoTeniendoSaldoMaximo(self):
        
        bill = self.crearBilletera(1234, 0)
        recargar_saldo(bill.id, 10000)
        consumir_saldo(bill.id, 10000)
        self.assertEqual(consultar_saldo(bill.id), Decimal(0).quantize(Decimal("1.00")))

    