# Sistema de Gestión de Inventarios 

## Objetivo
Este proyecto implementa un **sistema de gestión de inventarios en Python**, que guarda los productos en un archivo de texto (`inventario.txt`) y maneja excepciones al leer y escribir.

##  Funcionalidades
- Carga automática desde `inventario.txt`.
- Menú de consola: listar, añadir, actualizar, eliminar, buscar, recargar.
- Manejo de excepciones: crea archivo si no existe, ignora líneas corruptas, captura errores de permisos.

##  Archivos
- `inventario.py` → código principal
- `inventario.txt` → base de datos en texto (formato CSV con separador "|")
- `README.md` → documentación

##  Formato de inventario.txt
```
id|nombre|cantidad|precio
P001|Cámara digital|5|249.99
P002|Cable HDMI|20|5.50
```

## Ejecución
```bash
python3 inventario.py
```
