from pathlib import Path
import os
import shutil
import subprocess
import pytest


@pytest.fixture
def receptor():
    return Path(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputs", "1bcu_protein.pdb"))


@pytest.fixture
def ligand():
    return Path(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputs", "1bcu_ligand.sdf"))


@pytest.fixture
def pocket():
    return [5.0, 15.0, 50.0, 15, 15, 15]


def test_unidock_pipeline_default(receptor, ligand, pocket):
    from unidock_tools.modules.docking.unidock import UniDockRunner

    results_dir = "unidock_results"
    cmd = f"unidock_tools unidock -r {receptor} -l {ligand} -sd {results_dir} \
        -cx {pocket[0]} -cy {pocket[1]} -cz {pocket[2]} -ex {pocket[3]} -ey {pocket[4]} -ez {pocket[5]} \
        -sf vina -nm 1"
    print(cmd)
    resp = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")
    print(resp.stdout)
    assert resp.returncode == 0, f"run unidock pipeline app err:\n{resp.stderr}"

    result_file = os.path.join(results_dir, "1bcu_ligand_out.sdf")
    assert os.path.exists(result_file), f"docking result file not found"

    score_list = UniDockRunner.read_scores(result_file)
    score = score_list[0]
    assert -20 <= score <= 0, f"Uni-Dock score not in range: {score}"
    shutil.rmtree(results_dir, ignore_errors=True)


def test_unidock_pipeline_ligand_index(receptor, ligand, pocket):
    from unidock_tools.modules.docking.unidock import UniDockRunner

    index_file = Path("ligand_index.txt")
    with open(index_file, "w") as f:
        f.write(str(ligand))
    results_dir = "unidock_results"
    cmd = f"unidock_tools unidock -r {receptor} -i {index_file} -sd {results_dir} \
        -cx {pocket[0]} -cy {pocket[1]} -cz {pocket[2]} -ex {pocket[3]} -ey {pocket[4]} -ez {pocket[5]} \
        -sf vina -nm 1"
    print(cmd)
    resp = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")
    print(resp.stdout)
    assert resp.returncode == 0, f"run unidock pipeline app err:\n{resp.stderr}"

    result_file = os.path.join(results_dir, "1bcu_ligand_out.sdf")
    assert os.path.exists(result_file), f"docking result file not found"

    score_list = UniDockRunner.read_scores(result_file)
    score = score_list[0]
    assert -20 <= score <= 0, f"Uni-Dock score not in range: {score}"
    index_file.unlink(missing_ok=True)
    shutil.rmtree(results_dir, ignore_errors=True)


def test_unidock_pipeline_scoring_ad4(receptor, ligand, pocket):
    from unidock_tools.modules.docking.unidock import UniDockRunner

    results_dir = "unidock_results"
    cmd = f"unidock_tools unidock -r {receptor} -l {ligand} -sd {results_dir} \
        -cx {pocket[0]} -cy {pocket[1]} -cz {pocket[2]} -ex {pocket[3]} -ey {pocket[4]} -ez {pocket[5]} \
        -sf ad4 -nm 1"
    print(cmd)
    resp = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")
    print(resp.stdout)
    assert resp.returncode == 0, f"run unidock pipeline app err:\n{resp.stderr}"

    result_file = os.path.join(results_dir, "1bcu_ligand_out.sdf")
    assert os.path.exists(result_file), f"docking result file not found"

    score_list = UniDockRunner.read_scores(result_file)
    score = score_list[0]
    assert -20 <= score <= 0, f"Uni-Dock score not in range: {score}"
    shutil.rmtree(results_dir, ignore_errors=True)


def test_unidock_pipeline_multi_pose(receptor, ligand, pocket):
    from unidock_tools.modules.docking.unidock import UniDockRunner

    results_dir = "unidock_results"
    cmd = f"unidock_tools unidock -r {receptor} -l {ligand} -sd {results_dir} \
        -cx {pocket[0]} -cy {pocket[1]} -cz {pocket[2]} -ex {pocket[3]} -ey {pocket[4]} -ez {pocket[5]} \
        -sf vina -nm 4"
    print(cmd)
    resp = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")
    print(resp.stdout)
    assert resp.returncode == 0, f"run unidock pipeline app err:\n{resp.stderr}"

    result_file = os.path.join(results_dir, "1bcu_ligand_out.sdf")
    assert os.path.exists(result_file), f"docking result file not found"

    score_list = UniDockRunner.read_scores(result_file)
    assert len(score_list) == 4, f"docking result pose num({len(score_list)}) not match"
    for score in score_list:
        assert -20 <= score <= 0, f"Uni-Dock score not in range: {score}"
    shutil.rmtree(results_dir, ignore_errors=True)