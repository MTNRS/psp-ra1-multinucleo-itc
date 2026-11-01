# Reporte de proyecto

## Información de generación

- **Fecha:** 2026-11-01 18:16:37 +0100
- **Usuario:** freak
- **Equipo:** JARVIS
- **Sistema operativo:** Windows
- **Arquitectura:** x86_64
- **Directorio de ejecución:** `C:/Users/freak/Documents/DAM2-entregas/psp-ra1-multinucleo-itc/02-proyecto-unidad`
- **Proyecto documentado:** `C:/Users/freak/Documents/DAM2-entregas/psp-ra1-multinucleo-itc`
- **HMAC-SHA-256 de autenticidad:** `335f165929e490a04044576664522fcfd4b534f320a106002118abd1c97248f9`

> El HMAC-SHA-256 se calcula sobre el documento completo usando un secreto incluido en el programa y 64 ceros en el propio campo del HMAC. El secreto no se escribe en el informe. Este mecanismo permite comprobar integridad y que el documento fue generado con el mismo secreto.

## Estructura del proyecto

```
C:/Users/freak/Documents/DAM2-entregas/psp-ra1-multinucleo-itc
├── .gitignore
├── 01-ejercicios
│   └── RECORRIDO.md
├── 02-proyecto-unidad
│   ├── app.py
│   ├── motor.py
│   └── test_motor.py
├── 03-criterios-evaluacion
│   └── RESPUESTAS.md
└── README.md
```

## Bases de datos SQLite

Esta sección documenta únicamente el esquema de las bases SQLite detectadas. No se vuelcan registros ni datos de usuario.

No se han encontrado bases SQLite con extensiones .db, .sqlite o .sqlite3.

## Código (intercalado)

# psp-ra1-multinucleo-itc
**README.md**
```markdown
# PSP · RA1 · Multinúcleo ITC

Unidad 1: programación multiproceso. Laboratorio gráfico de renderizado de
imágenes fractales para estudiar reparto de carga CPU en ITC. Es una propuesta
académica independiente; no se integra en producción ni utiliza datos reales.

Python 3, sin dependencias externas. Desde 02-proyecto-unidad ejecutar
`python app.py`. Pulsar Comparar: genera la misma imagen secuencialmente y
mediante procesos independientes. Se muestran PID, franjas, tiempo CPU,
tiempos totales y equivalencia de píxeles. Pruebas: `python -m unittest -v`.

El factor puede ser menor que 1: crear procesos y transferir bytes cuesta
tiempo. La interfaz no garantiza aceleración en equipos cargados. El sistema
operativo decide en qué núcleos ejecuta cada proceso; los PID distintos
demuestran procesos independientes, no una asignación fija de núcleos.

El hilo coordinador evita bloquear Tk; los cálculos paralelos se ejecutan
en ProcessPoolExecutor. La cola de la interfaz transporta mensajes al hilo
principal. pool.map obtiene resultados y el contexto espera y cierra procesos.

## Uso de IA

Se ha utilizado asistencia de IA para implementar y revisar el laboratorio.
El alumno debe ejecutar, comprender y explicar los procesos antes de entregar.
```
## 01-ejercicios
**RECORRIDO.md**
```markdown
# Prácticas

1. Calcular una franja y observar el PID.
2. Repartir franjas entre dos procesos y recuperar bytes.
3. Comparar resultados secuenciales y paralelos.
4. Medir con 1, 2 y 4 procesos; explicar costes y variaciones.

Material revisado: unidad 001 de PSP, procesos, comunicación,
sincronización y aplicaciones multiproceso.
```
## 02-proyecto-unidad
**app.py**
```python
"""Ventana de comparación secuencial/multiproceso, sin bloquear Tk."""
import os
import queue
import threading
import tkinter as tk
from tkinter import ttk
from multiprocessing import freeze_support
from motor import renderizar

def main():
    ventana=tk.Tk();ventana.title('ITC · Laboratorio multinúcleo');ventana.geometry('860x740')
    ttk.Label(ventana,text='Renderizado CPU · Secuencial frente a multinúcleo',font=('Segoe UI',17)).pack(pady=15)
    ttk.Label(ventana,text=f'CPU lógicas disponibles: {os.cpu_count()} · Cada franja genera píxeles reales de una imagen fractal.').pack()
    barra=ttk.Frame(ventana);barra.pack(pady=10)
    ttk.Label(barra,text='Procesos:').pack(side='left')
    cantidad=tk.IntVar(value=min(4,os.cpu_count() or 1))
    ttk.Spinbox(barra,from_=1,to=os.cpu_count() or 1,textvariable=cantidad,width=4).pack(side='left')
    etiqueta=ttk.Label(ventana);etiqueta.pack()
    registro=tk.Text(ventana,height=12);registro.pack(fill='both',expand=True,padx=20,pady=10)
    estado=tk.StringVar(value='Pulsa Comparar para generar la misma imagen por ambos métodos.')
    ttk.Label(ventana,textvariable=estado,wraplength=800).pack(pady=10)
    eventos=queue.Queue();tiempos={};imagenes={}
    def trabajar(n):
        try:
            for paralelo in (False,True):
                modo='Paralelo' if paralelo else 'Secuencial'
                imagen,filas,tiempo=renderizar(paralelo,n,notificar=lambda r:eventos.put(('fila',modo,r)))
                eventos.put(('fin',modo,imagen,tiempo))
            eventos.put(('listo',))
        except Exception as error:eventos.put(('error',str(error)))
    def iniciar():
        try:n=cantidad.get();assert 1<=n<=(os.cpu_count() or 1)
        except Exception:estado.set('Selecciona un número válido de procesos.');return
        boton.config(state='disabled');registro.delete('1.0','end');estado.set('Calculando: primero secuencial, después paralelo…');threading.Thread(target=trabajar,args=(n,),daemon=True).start()
    boton=ttk.Button(barra,text='Comparar',command=iniciar);boton.pack(side='left',padx=15)
    def atender():
        try:
            while True:
                evento=eventos.get_nowait()
                if evento[0]=='fila':
                    _,modo,r=evento;registro.insert('end',f"{modo}: PID {r['pid']} · filas {r['inicio']}-{r['fin']} · CPU {r['cpu']:.3f}s\n");registro.see('end')
                elif evento[0]=='fin':
                    _,modo,datos,segundos=evento;imagenes[modo]=datos;tiempos[modo]=segundos
                    foto=tk.PhotoImage(data=b'P6\n480 320\n255\n'+datos,format='PPM');etiqueta.configure(image=foto);etiqueta.image=foto
                elif evento[0]=='listo':
                    estado.set(f"Secuencial: {tiempos['Secuencial']:.2f}s · Paralelo: {tiempos['Paralelo']:.2f}s · Factor: {tiempos['Secuencial']/tiempos['Paralelo']:.2f}x · Píxeles idénticos: {imagenes['Secuencial']==imagenes['Paralelo']}");boton.config(state='normal')
                elif evento[0]=='error':estado.set(evento[1]);boton.config(state='normal')
        except queue.Empty:pass
        ventana.after(100,atender)
    atender();ventana.mainloop()
if __name__=='__main__':freeze_support();main()
```
**motor.py**
```python
"""Renderizado CPU por franjas para comparar procesos con trabajo idéntico."""
import os
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context

def franja(tarea):
    ancho,alto,inicio,fin,iteraciones=tarea
    reloj=time.perf_counter();cpu=time.process_time();pixeles=bytearray()
    for y in range(inicio,fin):
        for x in range(ancho):
            c=complex(-2.1+3*x/ancho,-1.2+2.4*y/alto);z=0j;n=0
            while abs(z)<=2 and n<iteraciones:
                z=z*z+c;n+=1
            pixeles.extend((0,0,0) if n==iteraciones else (n*9%256,n*5%256,n*13%256))
    return {'inicio':inicio,'fin':fin,'pid':os.getpid(),'segundos':time.perf_counter()-reloj,'cpu':time.process_time()-cpu,'pixeles':bytes(pixeles)}

def renderizar(paralelo=False,procesos=2,ancho=480,alto=320,iteraciones=250,notificar=lambda r:None):
    tareas=[(ancho,alto,y,min(y+20,alto),iteraciones) for y in range(0,alto,20)]
    inicio=time.perf_counter();resultados=[]
    if paralelo:
        with ProcessPoolExecutor(max_workers=procesos,mp_context=get_context('spawn')) as pool:
            for resultado in pool.map(franja,tareas):resultados.append(resultado);notificar(resultado)
    else:
        for tarea in tareas:
            resultado=franja(tarea);resultados.append(resultado);notificar(resultado)
    duracion=time.perf_counter()-inicio
    imagen=b''.join(r['pixeles'] for r in sorted(resultados,key=lambda r:r['inicio']))
    return imagen,resultados,duracion
```
**test_motor.py**
```python
import unittest
from motor import renderizar
class Pruebas(unittest.TestCase):
    def test_equivalencia_y_procesos(self):
        import os
        sec,_,_=renderizar(False,2,100,80,80)
        par,filas,_=renderizar(True,2,100,80,80)
        self.assertEqual(sec,par)
        self.assertEqual(len(par),100*80*3)
        self.assertTrue(all(r['pid']!=os.getpid() for r in filas))
if __name__=='__main__':unittest.main()
```
## 03-criterios-evaluacion
**RESPUESTAS.md**
```markdown
# Criterios RA1

| Criterio | Evidencia |
|---|---|
| a | Concurrencia: tareas progresan durante el mismo periodo; apropiada para render y cálculo |
| b | Paralelismo local usa varios núcleos; distribuido usa máquinas y red. Local evita red pero limita recursos; distribuido escala con costes de comunicación |
| c | Cada trabajador tiene PID y espacio de memoria; el SO planifica su ejecución |
| d | Hilos comparten memoria del proceso; el hilo coordinador mantiene Tk receptivo; procesos aíslan los cálculos |
| e | ProcessPoolExecutor crea trabajadores con spawn |
| f | Se envían parámetros serializados y se devuelven bytes; no se necesita memoria mutable común |
| g | pool.map devuelve resultados; contexto espera y libera; queue sincroniza con interfaz |
| h | Franjas independientes se calculan en paralelo |
| i | test_motor verifica equivalencia exacta y PID diferentes al padre; README explica límites |

## Pruebas pendientes de usuario

Abrir ventana, ejecutar Comparar, revisar imagen y mensajes. Observar el
Administrador de tareas para distribución de carga. Los tiempos no equivalen
a una garantía de aceleración ni a una medición de afinidad de CPU.
```
