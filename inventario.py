#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Dict, Optional
import os

INVENTARIO_FILE = "inventario.txt"
FIELD_SEP = "|"

@dataclass
class Producto:
    id: str
    nombre: str
    cantidad: int
    precio: float

    def to_line(self) -> str:
        return f"{self.id}{FIELD_SEP}{self.nombre}{FIELD_SEP}{self.cantidad}{FIELD_SEP}{self.precio}\n"

    @staticmethod
    def from_line(line: str) -> Optional["Producto"]:
        parts = line.strip().split(FIELD_SEP)
        if len(parts) != 4:
            return None
        pid, nombre, cantidad_s, precio_s = parts
        try:
            cantidad = int(cantidad_s)
            precio = float(precio_s)
        except ValueError:
            return None
        return Producto(id=pid, nombre=nombre, cantidad=cantidad, precio=precio)

class Inventario:
    def __init__(self, ruta: str = INVENTARIO_FILE):
        self.ruta = ruta
        self.productos: Dict[str, Producto] = {}
        self._ensure_file_exists()
        self.cargar_desde_archivo()

    def _ensure_file_exists(self):
        try:
            if not os.path.exists(self.ruta):
                with open(self.ruta, "w", encoding="utf-8") as f:
                    f.write("")
                print(f"[INFO] Archivo de inventario '{self.ruta}' creado correctamente.")
        except PermissionError:
            print(f"[ERROR] No tengo permiso para crear '{self.ruta}'.")
        except OSError as e:
            print(f"[ERROR] Error al crear archivo: {e}")

    def cargar_desde_archivo(self):
        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                lineas = f.readlines()
        except FileNotFoundError:
            print(f"[WARN] Archivo '{self.ruta}' no encontrado. Se intentará crear.")
            self._ensure_file_exists()
            return
        except PermissionError:
            print(f"[ERROR] No tengo permiso para leer '{self.ruta}'.")
            return
        except OSError as e:
            print(f"[ERROR] Error al leer '{self.ruta}': {e}")
            return

        self.productos.clear()
        for line in lineas:
            if not line.strip():
                continue
            prod = Producto.from_line(line)
            if prod is None:
                print(f"[WARN] Línea corrupta ignorada: {line.strip()}")
                continue
            self.productos[prod.id] = prod
        print(f"[INFO] {len(self.productos)} productos cargados.")

    def guardar_todo(self) -> bool:
        try:
            with open(self.ruta, "w", encoding="utf-8") as f:
                for p in self.productos.values():
                    f.write(p.to_line())
            return True
        except PermissionError:
            print(f"[ERROR] Sin permisos para escribir '{self.ruta}'.")
            return False
        except OSError as e:
            print(f"[ERROR] Error al escribir archivo: {e}")
            return False

    def añadir_producto(self, producto: Producto) -> bool:
        if producto.id in self.productos:
            print(f"[WARN] Ya existe un producto con id '{producto.id}'.")
            return False
        self.productos[producto.id] = producto
        if self.guardar_todo():
            print(f"[OK] Producto '{producto.nombre}' añadido.")
            return True
        return False

    def actualizar_producto(self, producto: Producto) -> bool:
        if producto.id not in self.productos:
            print(f"[WARN] No existe producto con id '{producto.id}'.")
            return False
        self.productos[producto.id] = producto
        if self.guardar_todo():
            print(f"[OK] Producto '{producto.id}' actualizado.")
            return True
        return False

    def eliminar_producto(self, id_producto: str) -> bool:
        if id_producto not in self.productos:
            print(f"[WARN] No existe producto con id '{id_producto}'.")
            return False
        eliminado = self.productos.pop(id_producto)
        if self.guardar_todo():
            print(f"[OK] Producto '{eliminado.nombre}' eliminado.")
            return True
        return False

    def listar_productos(self):
        if not self.productos:
            print("[INFO] Inventario vacío.")
            return
        print(f"{'ID':10} | {'Nombre':30} | {'Cant.':>6} | {'Precio':>8}")
        print("-"*62)
        for p in self.productos.values():
            print(f"{p.id:10} | {p.nombre:30} | {p.cantidad:6d} | {p.precio:8.2f}")

    def obtener_producto(self, id_producto: str) -> Optional[Producto]:
        return self.productos.get(id_producto)

def menu():
    inv = Inventario()
    while True:
        print("\n--- MENÚ DE INVENTARIO ---")
        print("1. Listar productos")
        print("2. Añadir producto")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Buscar producto por ID")
        print("6. Recargar desde archivo")
        print("0. Salir")
        elec = input("Elige una opción: ").strip()

        if elec == "1":
            inv.listar_productos()
        elif elec == "2":
            pid = input("ID: ").strip()
            nombre = input("Nombre: ").strip()
            try:
                cantidad = int(input("Cantidad: ").strip())
                precio = float(input("Precio: ").strip())
            except ValueError:
                print("[ERROR] Entrada inválida.")
                continue
            p = Producto(pid, nombre, cantidad, precio)
            inv.añadir_producto(p)
        elif elec == "3":
            pid = input("ID a actualizar: ").strip()
            existing = inv.obtener_producto(pid)
            if not existing:
                print("[WARN] No existe producto.")
                continue
            nombre = input(f"Nombre [{existing.nombre}]: ").strip() or existing.nombre
            cantidad_s = input(f"Cantidad [{existing.cantidad}]: ").strip()
            precio_s = input(f"Precio [{existing.precio}]: ").strip()
            try:
                cantidad = int(cantidad_s) if cantidad_s else existing.cantidad
                precio = float(precio_s) if precio_s else existing.precio
            except ValueError:
                print("[ERROR] Entrada inválida.")
                continue
            p = Producto(pid, nombre, cantidad, precio)
            inv.actualizar_producto(p)
        elif elec == "4":
            pid = input("ID a eliminar: ").strip()
            confirm = input("¿Eliminar? (s/n): ").strip().lower()
            if confirm == "s":
                inv.eliminar_producto(pid)
        elif elec == "5":
            pid = input("ID a buscar: ").strip()
            p = inv.obtener_producto(pid)
            print(p if p else "No encontrado.")
        elif elec == "6":
            inv.cargar_desde_archivo()
        elif elec == "0":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
