import os
# import hmtdock
import csv
from rmsdfn import rmsd
import subprocess as sp

output_path = input_path = "/root/dockdata/gpu_redock/vina12_result_all_3"
configure_file = "/root/dockdata/CASF_2016_all.csv"
vina_gpu_path = "/root/Vina1.2-GPU"

def dock(ligpath, scoring_func, rigid_receptor, flex_receptor, center_x, center_y, center_z, size_x, size_y,\
    size_z, exhaustiveness, energy_range, min_rmsd, num_of_poses, max_step):
    if flex_receptor == None:
        cmd = "/root/Vina1.2-GPU/build/linux/release/vina --receptor {} --gpu_batch {} \
        --center_x {} --center_y {} --center_z {} --size_x {} \
        --size_y {} --size_z {} --exhaustiveness {} --energy_range {} \
        --num_modes {} --max_step {} --dir {}".format( 
            input_path + '/' + rigid_receptor, 
            input_path + '/' + ligpath, center_x, center_y, center_z, 
            size_x, size_y, size_z, 
            exhaustiveness, energy_range, num_of_poses, 
            max_step, output_path)
    else:
        cmd = "/root/Vina1.2-GPU/build/linux/release/vina --scoring {} --receptor {} --flex {} --ligand {} \
            --center_x {} --center_y {} --center_z {} --size_x {} \
            --size_y {} --size_z {} --exhaustiveness {} --energy_range {} \
            --num_modes {} --dir {}".format(scoring_func, 
                rigid_receptor, flex_receptor, 
                ligpath, center_x, center_y, center_z, 
                size_x, size_y, size_z, 
                exhaustiveness, energy_range, num_of_poses, 
                max_step, output_path)
    print(cmd)
    sp.run(cmd, shell=True)


with open(configure_file, "r") as f:
    reader = csv.reader(f)

    os.chdir(vina_gpu_path)
    cnt = 0
    test = True
    for ls in reader:
        cnt = cnt + 1
        # if cnt >= 7:
        #     continue
        print(ls)
        pdbname = ls[1]
        if pdbname == "2yge" or pdbname == "3uri" or pdbname == "3ag9":
            continue
        # if not (pdbname == "1e66" or pdbname == "3e92" or pdbname == "3e93"):
        #     continue
        os.chdir(vina_gpu_path)
        dock(pdbname+'_ligand_flex.pdbqt', 'vina', pdbname+'_protein.pdbqt', None, ls[7], ls[8], ls[9], ls[10], ls[11], ls[12], 1024, 9, 1, 1,
            20)
        os.chdir(input_path)
        # convert output 
        cmd = "obabel %s_ligand_flex_out.pdbqt -O %s_ligand_out.pdb"%(
            pdbname, pdbname)
        sp.run(cmd, shell=True)
        cmd = "obabel %s_ligand_flex.pdbqt -O %s_ligand.pdb"%(
            pdbname, pdbname)
        sp.run(cmd, shell=True)
        rmsd_ = rmsd(pdbname+'_ligand.pdb', pdbname+'_ligand_out.pdb')
        with open("vgpu_rmsd_thread1024_step20_flex_all.csv", "a") as out_f:
            out_f.write(pdbname+','+str(rmsd_)+"\n")
