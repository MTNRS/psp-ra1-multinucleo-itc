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
