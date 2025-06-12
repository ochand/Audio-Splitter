"""
Tests para el módulo AudioSplitter
"""

import unittest
import tempfile
import numpy as np
from pathlib import Path
import sys

# Agregar path del proyecto para imports absolutos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from audio_splitter.core.splitter import split_audio, convert_to_ms
from audio_splitter.utils.audio_utils import time_to_ms, ms_to_time, validate_audio_segment

class TestAudioSplitter(unittest.TestCase):
    
    def test_convert_to_ms(self):
        """Test conversión de tiempo a milisegundos"""
        # Formato MM:SS
        self.assertEqual(convert_to_ms("1:30"), 90000)  # 1 min 30 seg = 90000 ms
        self.assertEqual(convert_to_ms("0:05"), 5000)   # 5 seg = 5000 ms
        
        # Formato MM:SS.ms
        self.assertEqual(convert_to_ms("1:30.500"), 90500)  # 1 min 30.5 seg = 90500 ms
        
        # Formato HH:MM:SS
        self.assertEqual(convert_to_ms("1:01:30"), 3690000)  # 1 hora 1 min 30 seg
    
    def test_time_to_ms(self):
        """Test conversión usando audio_utils"""
        self.assertEqual(time_to_ms("2:15"), 135000)
        self.assertEqual(time_to_ms("0:30.750"), 30750)
    
    def test_ms_to_time(self):
        """Test conversión de ms a tiempo legible"""
        self.assertEqual(ms_to_time(90000), "01:30.000")
        self.assertEqual(ms_to_time(5500), "00:05.500")
    
    def test_validate_audio_segment(self):
        """Test validación de segmentos"""
        # Segmento válido
        self.assertTrue(validate_audio_segment(0, 30000, 60000))
        
        # Segmento inválido - inicio después del fin
        self.assertFalse(validate_audio_segment(40000, 30000, 60000))
        
        # Segmento inválido - fin después de la duración
        self.assertFalse(validate_audio_segment(50000, 70000, 60000))
        
        # Segmento inválido - inicio negativo
        self.assertFalse(validate_audio_segment(-1000, 30000, 60000))

if __name__ == '__main__':
    unittest.main()
