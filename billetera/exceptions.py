class SaldoExcedido(Exception):
    
    def __init__(self):
        pass

    def __str__(self):
        return "Saldo maximo de la billetera excedido."
    
class SaldoNegativo(Exception):
    
    def __init__(self):
        pass

    def __str__(self):
        return "Saldo de la billetera no puede quedar en negativo."
    
class MontoNegativo(Exception):
    
    def __init__(self):
        pass

    def __str__(self):
        return "El monto no puede ser negativo."
    
class MontoCero(Exception):
    
    def __init__(self):
        pass

    def __str__(self):
        return "El monto no puede ser cero."
    
class AutenticacionDenegada(Exception):
    
    def __init__(self):
        pass

    def __str__(self):
        return "Autenticacion denagada, intente de nuevo."