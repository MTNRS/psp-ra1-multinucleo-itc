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
