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
