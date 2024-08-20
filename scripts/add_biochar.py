# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 17:13:14 2022

@author: mdomenech


Biochar script

step 1. add co2 tracking: co2 atmosphere store which tracks the co2 emitted to the atmosphere
step 2. DELETE CO2 STORED;;;; add co2 stored: tracks the co2 stored (captured) in this case this is equivalent to the amount of biochar
step 3. add override components to the networks (for the links)
step 4. add pyrolysis link from the biomass store to the electrical buses and from the pyrolysis to the co2 stored (biochar)


"""
#librariesfrom _helpers python
import logging  #to log messages that you want to see
from _helpers import configure_logging
from override_components import override_component_attrs

#from add_electricity import (add_nice_carrier_names,
#                             _add_missing_carriers_from_costs)

import pypsa
import pandas as pd
import numpy as np


def add_co2_tracking(n):

    elec_opts = snakemake.config['not-electricity']
    carriers = elec_opts['biochar']['Store']

    #_add_missing_carriers_from_costs(n, carriers)

    #buses_i = n.buses.index
    #bus_sub_dict = {k: n.buses[k].values for k in ['x', 'y', 'country']}

    if 'co2-tracking' in carriers:
    # minus sign because opposite to how fossil fuels used:
    # CH4 burning puts CH4 down, atmosphere up
        n.add("Carrier", "co2",
              co2_emissions= snakemake.config["not-electricity"]["biochar"]["co2_seq"],  #sequestration potential biochar
              nice_name = "CO2",
              color = "#235ebc")

        # this tracks CO2 in the atmosphere
        n.add("Bus",
            "co2 atmosphere",
            location="DE",
            carrier="co2")


        # can also be negative
        n.add("Store", "co2 atmosphere",
            #e_nom = 1000,
            e_nom_extendable=True,
            e_min_pu=-1,
            carrier="co2",
            bus="co2 atmosphere",
            #capital_cost=0,
        )

        #CO2 STORED IS DELETED
        #this tracks co2 stored (biochar in this case)
        #n.add("Bus","co2 stored",
        #      location= "DE",
        #      carrier= "co2 stored")

        #n.add("Store","co2 stored",
        #      #e_nom = 1000,
        #      #e_min_pu=-1,
        #      e_nom_extendable=True,
        #      #e_nom_max=np.inf,
        #      #capital_cost=0.,  #capital cost for biochar store
        #      carrier="co2 stored",
        #      bus="co2 stored"
        #      )


def add_pyrolysis(n):

    print("adding pyrolysis")

    elec_opts = snakemake.config['not-electricity']
    tech = elec_opts['biochar']['Link']


    buses_i = n.buses.index[n.buses.carrier == "AC"] #this way co2 tracking is not considered
    j = n.buses[n.buses.carrier == "AC"]
    j = j.shape[0]
    bus_sub_dict =  {k: n.buses[k].values[0:j,] for k in ['x', 'y', 'country']} #do not select co2 tracking buses n.buses.values


    if 'pyrolysis' in tech:
        print("adding pyrolysis")

        pyrolysis_buses_i = n.madd("Bus", buses_i + " pyrolysis", carrier="pyrolysis", **bus_sub_dict)#bus_sub_dict)   #n.buses.index[n.buses.carrier == "AC"]

        #this is the wood store
        n.madd("Store", pyrolysis_buses_i + " biomass storage",
               bus= pyrolysis_buses_i,
               carrier="pyrolysis",
               e_nom = snakemake.config["not-electricity"]["biochar"]["biomass_potential"],  #capacity pyrolysis (available biomass)
               e_initial = snakemake.config["not-electricity"]["biochar"]["biomass_potential"],
               #e_cyclic=True,
               #e_nom_extendable=True,
               marginal_cost = snakemake.config["not-electricity"]["biochar"]["marginal_cost"]*snakemake.config["not-electricity"]["biochar"]["electrical_eff"]) #marginal cost biomass store


        n.madd("Link",pyrolysis_buses_i, #this is what is written in name
               bus0= pyrolysis_buses_i,
               bus1= buses_i,
               #bus2="co2 stored",          #co2 stored is deleted
               bus3="co2 atmosphere",
               #carrier= 'pyrolysis biochar',
               p_nom_extendable=True,
               #lifetime = snakemake.config["not-electricity"]["biochar"]["lifetime"],,
               efficiency = snakemake.config["not-electricity"]["biochar"]["electrical_eff"],  #electrical efficiency
               #efficiency2 = snakemake.config["not-electricity"]["biochar"]["biochar_eff"],    #biochar efficiency
               efficiency3 = -snakemake.config["not-electricity"]["biochar"]["biochar_eff"], #co2 reduction from atmosphere
               capital_cost = snakemake.config["not-electricity"]["biochar"]["capital_cost"]*snakemake.config["not-electricity"]["biochar"]["electrical_eff"])  #1300000.0,    #55250.0, #capital cost pyrolysis
               

if __name__ == "__main__":
    if 'snakemake' not in globals():
        from _helpers import mock_snakemake
        snakemake = mock_snakemake('add_biochar', network='elec',
                                   simpl='', clusters=5)

    configure_logging(snakemake)

    overrides = override_component_attrs(snakemake.input.overrides)
    n = pypsa.Network(snakemake.input.network, override_component_attrs=overrides)

    add_co2_tracking(n)
    add_pyrolysis(n)

    n.export_to_netcdf(snakemake.output[0])
