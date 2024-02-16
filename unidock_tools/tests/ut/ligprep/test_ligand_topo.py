from pathlib import Path
import os
import unittest as ut


class TestLigandTopology(ut.TestCase):
    def setUp(self):
        self.input_ligand = os.path.join(os.path.dirname(__file__), "Imatinib.sdf")
        self.output_ligand = "Imatinib_prepared.sdf"

    def tearDown(self):
        Path(self.output_ligand).unlink(missing_ok=True)

    def test_build_topology(self):
        from rdkit import Chem
        from unidock_tools.modules.ligand_prep import TopologyBuilder

        mol = Chem.SDMolSupplier(self.input_ligand, removeHs=False)[0]
        tb = TopologyBuilder(mol)
        tb.build_molecular_graph()
        tb.write_sdf_file(self.output_ligand)
        out_mol = Chem.SDMolSupplier(self.output_ligand, removeHs=False)[0]
        self.assertTrue(out_mol.HasProp("fragInfo"))
        self.assertTrue(out_mol.HasProp("torsionInfo"))
        self.assertTrue(out_mol.HasProp("atomInfo"))
