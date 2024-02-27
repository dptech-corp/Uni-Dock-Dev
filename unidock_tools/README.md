# Introduction

Based on Uni-Dock, we have developed several user-friendly and enhanced applications in **UniDockTools**.
Main features are:

- support PDB format receptor and SDF format ligands

- MCDock: 

# Installation

## 1. Install Uni-Dock and UniDockTools

To install UniDock, please follow [Uni-Dock installation docs](../unidock/README.md).

To install UniDockTools, please execute the following command in `Uni-Dock/unidock_tools` directory:

```pip install .```

## 2. Install MGLTools

If you want ro run Uni-Dock with receptor in PDB format, you need to install `mgltools`. Please use the command below:

```conda create -n mgltools mgltools -c bioconda```


# Usage

By installing UniDockTools, you have obtained an executable file called **Unidock** (note the capitalized U), which you can use just like running **unidock**.

## Input ligands with origin sdf format

`Unidock --receptor receptor.pdbqt --gpu_batch ligand1.sdf ligand2.sdf --center_x 9 --center_y -5  --center_z -5 --size_x 20  --size_y 20 --size_z 20 --search_mode balance  --dir .`

## Use gnina CNNscores to rescore docking poses

`Unidock --receptor receptor.pdbqt --gpu_batch ligand1.sdf ligand2.sdf  --scoring gnina --center_x 9 --center_y -5  --center_z -5 --size_x 20  --size_y 20 --size_z 20 --search_mode balance  --dir .`

## Use ligands structure as bias

`Unidock --receptor receptor.pdbqt --gpu_batch ligand1.sdf ligand2.sdf --reference ref1.sdf ref2.sdf --scoring gnina --center_x 9 --center_y -5  --center_z -5 --size_x 20  --size_y 20 --size_z 20 --search_mode balance  --dir . `

## Other usage

  To lower users' learning cost, the other usage methods of **Unidock** remain consistent with the usage of **unidock**.

# License

This project is licensed under the terms of Apache license 2.0. See [LICENSE](./LICENSE) for additional details.
