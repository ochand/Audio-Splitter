"""
Tests para el módulo AudioConverter
"""

import unittest
from pathlib import Path
import sys

# Agregar path del proyecto para imports absolutos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from audio_splitter.core.converter import AudioConverter

class TestAudioConverter(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para tests"""
        self.converter = AudioConverter()
    
    def test_supported_formats(self):
        """Test formatos soportados"""
        self.assertIn('.wav', self.converter.supported_input_formats)
        self.assertIn('.mp3', self.converter.supported_input_formats)
        self.assertIn('.flac', self.converter.supported_input_formats)
        
        self.assertIn('.wav', self.converter.supported_output_formats)
        self.assertIn('.mp3', self.converter.supported_output_formats)
        self.assertIn('.flac', self.converter.supported_output_formats)
    
    def test_quality_presets(self):
        """Test configuraciones de calidad"""
        self.assertIn('mp3', self.converter.QUALITY_PRESETS)
        self.assertIn('flac', self.converter.QUALITY_PRESETS)
        
        # MP3 quality presets
        mp3_presets = self.converter.QUALITY_PRESETS['mp3']
        self.assertIn('low', mp3_presets)
        self.assertIn('medium', mp3_presets)
        self.assertIn('high', mp3_presets)
        
        # FLAC quality presets
        flac_presets = self.converter.QUALITY_PRESETS['flac']
        self.assertIn('low', flac_presets)
        self.assertIn('medium', flac_presets)
        self.assertIn('high', flac_presets)
    
    def test_detect_format_invalid_file(self):
        """Test detección de formato con archivo inexistente"""
        with self.assertRaises(FileNotFoundError):
            self.converter.detect_format("archivo_inexistente.mp3")

if __name__ == '__main__':
    unittest.main()
