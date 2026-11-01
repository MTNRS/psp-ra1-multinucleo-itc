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
