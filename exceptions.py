"""
Modulo de excepciones personalizadas para el sistema de Software FJ.
Define una jerarquia clara de errores de dominio para mantener la estabilidad.
"""


class SoftwareFJError(Exception):
    """Excepcion base para todos los errores del sistema de Software FJ."""
    pass


class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando los datos ingresados (nombre, correo, documento, etc.) son invalidos."""
    pass


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parametro obligatorio para crear una entidad o servicio."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio inactivo o sin cupo/disponibilidad."""
    pass


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando ocurre un error logico en el flujo o estado de una reserva."""
    pass


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un calculo de tarifa, descuento o impuesto genera un valor incoherente."""
    pass
