from pathlib import Path
import os
import shutil
import uuid
import pytest


@pytest.fixture
def receptor():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputs", "1bcu_protein.pdb")


@pytest.fixture
def ligand():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputs", "1bcu_ligand.sdf")


@pytest.fixture
def pocket():
    return [5.0, 15.0, 50.0, 15, 15, 15]


def test_run_unidock_vina(receptor, ligand, pocket):
    from unidock_tools.modules.docking import run_unidock

    workdir = Path(f"./tmp+{uuid.uuid4()}")
    workdir.mkdir(parents=True, exist_ok=True)

    result_ligands, scores_list = run_unidock(
        receptor=receptor,
        ligands=[ligand],
        output_dir=workdir,
        center_x=pocket[0],
        center_y=pocket[1],
        center_z=pocket[2],
        size_x=pocket[3],
        size_y=pocket[4],
        size_z=pocket[5],
        scoring="vina",
        num_modes=10,
    )

    result_ligand = result_ligands[0]
    assert os.path.exists(result_ligand)

    scores = scores_list[0]
    assert len(scores) == 10
    for score in scores:
        assert -20 <= score <= 0

    shutil.rmtree(workdir, ignore_errors=True)