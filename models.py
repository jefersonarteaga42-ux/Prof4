"""
Modulo de entidades del dominio para Software FJ.
Implementa clases abstractas (ABC), encapsulacion con propiedades, herencia,
polimorfismo y manejo de excepciones con encadenamiento.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import re
from typing import Optional
from exceptions import (
    DatosInvalidosError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    CalculoInconsistenteError,
)


class EntidadBase(ABC):
    """Clase abstracta base para todas las entidades del sistema."""

    def __init__(self, id_entidad: str):
        self.id_entidad = id_entidad
        self._fecha_creacion = datetime.now()

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @id_entidad.setter
    def id_entidad(self, valor: str):
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError("El ID de la entidad es obligatorio y no puede estar vacio.")
        self._id_entidad = valor.strip().upper()

    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion

    @abstractmethod
    def validar(self) -> bool:
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        pass


class Cliente(EntidadBase):
    """Representa un cliente registrado en Software FJ."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.validar()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        if len(valor.strip()) < 3:
            raise DatosInvalidosError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError("El correo electronico es obligatorio.")
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_correo, valor.strip()):
            raise DatosInvalidosError(f"El correo '{valor}' no tiene un formato valido.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError("El telefono es obligatorio.")
        solo_digitos = re.sub(r"\D", "", valor)
        if len(solo_digitos) < 7 or len(solo_digitos) > 15:
            raise DatosInvalidosError("El telefono debe contener entre 7 y 15 digitos.")
        self._telefono = valor.strip()

    def validar(self) -> bool:
        return all([self._id_entidad, self._nombre, self._correo, self._telefono])

    def obtener_resumen(self) -> str:
        return f"Cliente [{self.id_entidad}]: {self.nombre} | Correo: {self.correo} | Tel: {self.telefono}"


class Servicio(EntidadBase):
    """Clase base para los servicios tecnologicos de Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, disponible: bool = True):
        super().__init__(id_servicio)
        self.nombre = nombre
        self.tarifa_hora = tarifa_hora
        self.disponible = disponible
        self.validar()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        self._nombre = valor.strip()

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @tarifa_hora.setter
    def tarifa_hora(self, valor: float):
        try:
            tarifa = float(valor)
        except (TypeError, ValueError) as exc:
            raise DatosInvalidosError("La tarifa por hora debe ser numerica.") from exc
        if tarifa <= 0:
            raise DatosInvalidosError("La tarifa por hora debe ser mayor a cero.")
        self._tarifa_hora = tarifa

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        if not isinstance(valor, bool):
            raise DatosInvalidosError("La disponibilidad debe ser booleana.")
        self._disponible = valor

    @abstractmethod
    def calcular_costo_base(self, duracion_horas: float) -> float:
        """Metodo polimorfico implementado por cada tipo de servicio."""
        pass

    def validar(self) -> bool:
        return self._tarifa_hora > 0 and bool(self._nombre)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Servicio [{self.id_entidad}]: {self.nombre} (${self.tarifa_hora:,.2f}/h) - {estado}"


class ReservaSala(Servicio):
    """Servicio polimorfico para reserva de salas de desarrollo o juntas."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser mayor a cero.")
        self.capacidad = capacidad

    def calcular_costo_base(self, duracion_horas: float) -> float:
        if duracion_horas <= 0:
            raise CalculoInconsistenteError("La duracion en horas debe ser mayor a cero.")
        costo = self.tarifa_hora * duracion_horas
        if duracion_horas >= 4:
            costo *= 0.90
        return round(costo, 2)


class AlquilerEquipo(Servicio):
    """Servicio polimorfico para alquiler de servidores o estaciones de trabajo."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, deposito_seguridad: float = 50000.0, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if deposito_seguridad < 0:
            raise DatosInvalidosError("El deposito de seguridad no puede ser negativo.")
        self.deposito_seguridad = float(deposito_seguridad)

    def calcular_costo_base(self, duracion_horas: float) -> float:
        if duracion_horas <= 0:
            raise CalculoInconsistenteError("La duracion en horas debe ser mayor a cero.")
        return round((self.tarifa_hora * duracion_horas) + self.deposito_seguridad, 2)


class AsesoriaEspecializada(Servicio):
    """Servicio polimorfico de consultoria y arquitectura de software."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, nivel_senior: bool = True, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        self.nivel_senior = nivel_senior

    def calcular_costo_base(self, duracion_horas: float) -> float:
        if duracion_horas <= 0:
            raise CalculoInconsistenteError("La duracion en horas debe ser mayor a cero.")
        recargo_senior = 1.25 if self.nivel_senior else 1.0
        return round((self.tarifa_hora * duracion_horas) * recargo_senior, 2)


class Reserva(EntidadBase):
    """Gestiona el ciclo de vida y calculo financiero de una reserva."""

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: float):
        super().__init__(id_reserva)
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Cliente invalido para la reserva.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Servicio invalido para la reserva.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no esta disponible actualmente.")
        if duracion_horas <= 0:
            raise ReservaInvalidaError("La duracion de la reserva debe ser mayor a 0 horas.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = float(duracion_horas)
        self.estado = "PENDIENTE"
        self.total_pagar = 0.0
        self.validar()

    def confirmar(self, impuesto: float = 0.19, descuento: float = 0.0, recargo_extra: Optional[float] = None):
        """Calcula el valor final con impuestos/descuentos y confirma la reserva."""
        if self.estado != "PENDIENTE":
            raise ReservaInvalidaError(f"Solo se pueden confirmar reservas PENDIENTES (estado actual: {self.estado}).")
        if not (0 <= impuesto <= 1) or not (0 <= descuento < 1):
            raise CalculoInconsistenteError("Porcentajes de impuesto o descuento fuera de rango (0 a 1).")

        try:
            subtotal = self.servicio.calcular_costo_base(self.duracion_horas)
            if recargo_extra is not None:
                if recargo_extra < 0:
                    raise CalculoInconsistenteError("El recargo extra no puede ser negativo.")
                subtotal += recargo_extra

            monto_descuento = subtotal * descuento
            base_gravable = subtotal - monto_descuento
            total = base_gravable * (1 + impuesto)

            if total <= 0:
                raise CalculoInconsistenteError("El total calculado resulto menor o igual a cero.")

            self.total_pagar = round(total, 2)
            self.estado = "CONFIRMADA"
        except CalculoInconsistenteError as exc:
            raise ReservaInvalidaError(f"Fallo el calculo financiero de la reserva {self.id_entidad}.") from exc

    def procesar(self):
        """Marca una reserva confirmada como ejecutada/procesada."""
