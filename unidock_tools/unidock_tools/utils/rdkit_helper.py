import logging
import traceback
from rdkit import Chem


def set_properties(mol: Chem.rdchem.Mol, properties: dict):
    """
    Set properties to a molecule.

    Args:
        mol (Chem.rdchem.Mol): The molecule.
        properties (dict): A dictionary of properties.

    Returns:
        Chem.Mol: The molecule with properties set.
    """
    for key, value in properties.items():
        try:
            if isinstance(key, int):
                mol.SetIntProp(key, value)
            elif isinstance(key, float):
                mol.SetDoubleProp(key, value)
            else:
                mol.SetProp(key, str(value))
        except:
            logging.warning(f"set property {key} err: {traceback.format_exc()}")
