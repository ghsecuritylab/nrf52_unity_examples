import unittest
import serial
import os
import sys
import subprocess
from time import sleep
from jemu import Jemu

dir = os.path.dirname(os.path.abspath(__file__))
fw_bin = os.path.join(dir, '..', 'pca10040', 'blank', 'armgcc', '_build', 'nrf52832_xxaa.bin')


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.jemu = Jemu(working_directory=dir)
        self.jemu.load(fw_bin)

    def tearDown(self):
        pass

    def test_sanity(self):
        with self.jemu as j:
            running = True
            while running:
                line = j.uart.read_line()
                words = line.split(" ")
                if (len(words) > 3) and (words[2] == "Temperature:"):
                    temperature = int(words[3].partition(".")[0])
                    self.assertEqual(temperature, 2762)
                    return True

