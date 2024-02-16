from pathlib import Path
import os
import unittest as ut


class TestConfGen(ut.TestCase):
    def setUp(self):
        self.input_ligand = os.path.join(os.path.dirname(__file__), "Imatinib.sdf")

    def tearDown(self):
        pass

    def test_confgen_cdpkit(self):
        from rdkit import Chem
        from unidock_tools.modules.confgen.cdpkit import CDPKitConfGenerator

        mol = Chem.SDMolSupplier(self.input_ligand, removeHs=False)[0]

        runner = CDPKitConfGenerator()
        runner.check_env()
        mol_confs = runner.generate_conformation(mol, max_num_confs_per_ligand=100)
        self.assertGreater(len(mol_confs), 10)

    def test_confgen_obabel(self):
        from rdkit import Chem
        from unidock_tools.modules.confgen.obabel import OBabelConfGenerator

        mol = Chem.SDMolSupplier(self.input_ligand, removeHs=False)[0]

        runner = OBabelConfGenerator()
        runner.check_env()
        mol_confs = runner.generate_conformation(mol, max_num_confs_per_ligand=100)
        self.assertGreater(len(mol_confs), 10)