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
