from pathlib import Path
import os
import shutil
import uuid
import unittest as ut


class TestUniDockTools(ut.TestCase):
    def setUp(self):
        self.workdir = Path(f"./tmp+{uuid.uuid4()}")
        self.workdir.mkdir(parents=True, exist_ok=True)
        self.receptor = Path(os.path.join(os.path.dirname(__file__), "1bcu_protein.pdb"))
        self.ligand = Path(os.path.join(os.path.dirname(__file__), "1bcu_ligand.sdf"))
        self.pocket = [5.0, 15.0, 50.0, 15, 15, 15]

    def tearDown(self):
        shutil.rmtree(self.workdir, ignore_errors=True)

    def test_run_unidock_vina(self):
        from unidock_tools.modules.docking import run_unidock

        result_ligands, scores_list = run_unidock(
            receptor=self.receptor,
            ligands=[self.ligand],
            output_dir=self.workdir,
            center_x=self.pocket[0],
            center_y=self.pocket[1],
            center_z=self.pocket[2],
            size_x=self.pocket[3],
            size_y=self.pocket[4],
            size_z=self.pocket[5],
            scoring="vina",
            num_modes=10,
        )

        result_ligand = result_ligands[0]
        self.assertTrue(os.path.exists(result_ligand))

        scores = scores_list[0]
        self.assertAlmostEqual(len(scores), 10)
        for score in scores:
            self.assertTrue(-20 <= score <= 0)


if __name__ == "__main__":
    ut.main()
