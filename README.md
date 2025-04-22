# PyPSA-Eur-bc installation

cd path/without/spaces


_______
*if pypsa-eur not installed:

git clone git@github.com:txelldm/pypsa-eur-bc.git

cd pypsa-eur-bc

.../pypsa-eur-bc % conda env create -f envs/environment.yaml

.../pypsa-eur-bc % conda activate pypsa-eur


_______


*if pypsa-eur allready installed: 

conda activate pypsa-eur

git clone git@github.com:txelldm/pypsa-eur-bc.git



_______



*create network

snakemake results/networks/elec_s_3_ecb_lcopt_Co2L-8H-Ep.nc --cores --keep-target-files

