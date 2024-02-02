from typing import List, Any, Optional
from pathlib import Path
import os
import copy
import logging
import math
from multiprocessing import Pool
from rdkit import Chem

from .string import make_tmp_dir, randstr
from .rdkit_helper import sdf_writer, set_properties, clear_properties


class Mol:
    def __init__(self, mol: Chem.rdchem.Mol, props: dict):
        self.mol_confs = [mol]
        props.update(mol.GetPropsAsDict())
        self.props = props

    def get_prop(self, key: str, default_value: Optional[Any] = None) -> Any:
        return self.props.get(key, default_value)

    def get_props(self) -> dict:
        return self.props

    def get_first_mol(self) -> Chem.rdchem.Mol:
        return self.mol_confs[0]

    def update_mol_confs(self, mol_confs: List[Chem.rdchem.Mol]):
        self.mol_confs = mol_confs

    def update_props(self, props: dict):
        self.props.update(props)


class MolGroup:
    def __init__(self, ligand_files: List[Path]):
        self.mol_group: List[Mol] = list()
        self._initialize(ligand_files)

    def __iter__(self):
        for mol in self.mol_group:
            yield mol

    def iter_idx_list(self, batch_size: int) -> List[int]:
        real_batch_size = math.ceil(len(self.mol_group) / math.ceil(len(self.mol_group) / batch_size))
        batch_id_list = [list(range(i, i + real_batch_size)) for i in range(0, len(self.mol_group), real_batch_size)]
        for sub_id_list in batch_id_list:
            yield batch_id_list

    def _initialize(self, ligand_files: List[Path]):
        for ligand_file in ligand_files:
            file_prefix = ligand_file.stem
            for mol in Chem.SDMolSupplier(str(ligand_file), removeHs=False):
                if mol:
                    self.mol_group.append(Mol(mol, {"file_prefix": file_prefix}))

    def update_property_by_idx(self, idx: int, property_name: str, value: Any):
        self.mol_group[idx].update_props({property_name: value})

    def update_mol_confs(self, idx: int, mol_confs: List[Chem.Mol]):
        if not isinstance(mol_confs, list):
            logging.warning(f"molecule_list should be list")
            mol_confs = [mol_confs]
        self.mol_group[idx] = [clear_properties(mol) for mol in mol_confs]

    def update_mol_confs_by_file_prefix(self, file_prefix: str, mol_confs_list: List[Chem.Mol]):
        file_prefix_dict = {mol.get_prop("file_prefix", ""): idx for idx, mol in enumerate(self.mol_group)}
        if not file_prefix_dict.get(file_prefix):
            logging.error(f"Cannot find {file_prefix} in MoleculeGroup")
            return
        self.update_mol_confs(file_prefix_dict[file_prefix], mol_confs_list)

    def update_property_by_file_prefix(self, file_prefix: str, property_name: str, value: Any):
        file_prefix_dict = {mol.get_prop("file_prefix", ""): idx for idx, mol in enumerate(self.mol_group)}
        if file_prefix not in file_prefix_dict:
            logging.error(f"Cannot find {file_prefix} in MoleculeGroup")
            return
        self.update_property_by_idx(file_prefix_dict[file_prefix], property_name, value)

    def write_sdf_by_idx(self,
                         idx: int,
                         save_dir: Path = None,
                         seperate_conf: bool = False,
                         conf_prefix: str = "_CONF"
                         ):
        if save_dir is None:
            save_dir = "sdf"
        save_dir = make_tmp_dir(str(save_dir), False, False)

        mol_confs = self.mol_group[idx].get_mol_confs()
        mol_confs_copy = [None] * len(mol_confs)
        props = self.mol_group[idx].get_props()
        for conf_id, mol_conf in enumerate(mol_confs):
            mol_conf_copy = copy.copy(mol_conf)
            set_properties(mol_conf_copy, props)
            mol_confs_copy[conf_id] = mol_conf_copy
        # save SDF files
        sdf_file_list = []
        if seperate_conf:
            for conf_id, mol_conf in enumerate(mol_confs_copy):
                save_name = f"{save_dir}/{props['file_prefix']}{conf_prefix}{idx}.sdf"
                sdf_writer([mol_conf], save_name)
                sdf_file_list.append(Path(save_name))
        else:
            save_name = f"{save_dir}/{props['file_prefix']}.sdf"
            sdf_writer(mol_confs_copy, save_name)
            sdf_file_list.append(Path(save_name))
        return sdf_file_list

    def write_sdf(self, save_dir: Path = None,
                  seperate_conf: bool = False,
                  conf_prefix: str = "_CONF") -> List[Path]:
        result_files = []
        for idx in range(len(self.mol_group)):
            result_files.extend(self.write_sdf_by_idx(idx=idx, save_dir=save_dir,
                                                      seperate_conf=seperate_conf,
                                                      conf_prefix=conf_prefix))
        return result_files
