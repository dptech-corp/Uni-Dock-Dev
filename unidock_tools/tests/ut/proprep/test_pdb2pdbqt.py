from pathlib import Path
import os
import unittest as ut


class TestPdb2Pdbqt(ut.TestCase):
    def setUp(self):
        self.pdb_file = os.path.join(os.path.dirname(__file__), "protein.pdb")
        self.pdbqt_file = "protein.pdbqt"

    def tearDown(self):
        Path(self.pdbqt_file).unlink(missing_ok=True)

    def test_pdb2pdbqt(self):
        from unidock_tools.modules.protein_prep import pdb2pdbqt
        pdb2pdbqt(self.pdb_file, self.pdbqt_file)
        self.assertTrue(os.path.exists(self.pdbqt_file))
