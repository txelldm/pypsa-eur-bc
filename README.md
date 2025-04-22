PyPSA-Eur extension with pyrolysis technology. (output: electricity and negative emissions)

# PyPSA-Eur-bc installation

cd path/without/spaces


*if pypsa-eur not installed:

git clone git@github.com:txelldm/pypsa-eur-bc.git

cd pypsa-eur-bc

.../pypsa-eur-bc % conda env create -f envs/environment.yaml

.../pypsa-eur-bc % conda activate pypsa-eur


*if pypsa-eur allready installed: 

conda activate pypsa-eur

git clone git@github.com:txelldm/pypsa-eur-bc.git




*create network

snakemake results/networks/elec_s_3_ecb_lcopt_Co2L-8H-Ep.nc --cores --keep-target-files

