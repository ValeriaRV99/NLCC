import os
import numpy as np
from dftpy.mpi import pmi, sprint, mp
from dftpy.ions import Ions
from ase.lattice.cubic import FaceCenteredCubic
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.io.trajectory import Trajectory
from ase import units
from dftpy.grid import DirectGrid
from dftpy.field import DirectField
from dftpy.functional import Functional, TotalFunctional
from dftpy.optimization import Optimization
from dftpy.config.config import DefaultOption, OptionFormat, PrintConf
from dftpy.api.api4ase import DFTpyCalculator
import pathlib
from dftpy.mpi import MP, sprint
np.random.seed(8888)
mp = MP(parallel=True)
size = 3
a = 4.259663119760805 # Number taken from EXP_INFO
T = 300  # Kelvin
atoms = FaceCenteredCubic(
    directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]], latticeconstant=a, symbol="Ag", size=(size, size, size), pbc=True
)

ions = Ions.from_ase(atoms)
PP_list = {'Ag': '../Ag_AE_1_gbrv.psp8'} ## Pseudo with NLCC
grid = DirectGrid(ecut=50, lattice=ions.cell, mp=mp, full=False)
rho = DirectField(grid=grid)

PSEUDO = Functional(type='PSEUDO', grid=grid, ions=ions, PP_list=PP_list)
core = PSEUDO.core_density
PSEUDO.local_PP()
if PSEUDO.vlines_core['Ag'] is None: print('Not core')
KE = Functional(type='KEDF', name='TFvW', y=0.2, core_density=core)
XC = Functional(type='XC', name='LDA', core_density=core, libxc=False)
HARTREE = Functional(type='HARTREE')

funcDict = {'KE' :KE, 'XC' :XC, 'HARTREE' :HARTREE, 'PSEUDO' :PSEUDO}
EnergyEvaluator = TotalFunctional(**funcDict)

rho[:] = ions.get_ncharges() / ions.cell.volume

opt_options = {'econv' : 1e-6, "maxiter": 100}
optimizer = Optimization(EnergyEvaluator=EnergyEvaluator, optimization_options = opt_options, optimization_method='CG')

calc = DFTpyCalculator(optimizer = optimizer, evaluator = EnergyEvaluator, rho = rho)

atoms.set_calculator(calc)

MaxwellBoltzmannDistribution(atoms, temperature_K=50)

dyn = Langevin(atoms, 0.5 * units.fs, temperature_K = T, friction = 0.1)

step = 0
interval = 1

def printenergy(a=atoms):
    global step, interval
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    sprint(
        "Step={:<8d} Epot={:.5f} Ekin={:.5f} T={:.3f} Etot={:.5f}".format(
            step, epot, ekin, ekin / (1.5 * units.kB), epot + ekin
        )
    )
    step += interval

def printenergy(a=atoms):
    global step, interval
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    sprint(
        "Step={:<8d} Epot={:.5f} Ekin={:.5f} T={:.3f} Etot={:.5f}".format(
            step, epot, ekin, ekin / (1.5 * units.kB), epot + ekin
        )
    )
    step += interval

def check_stop():
    if os.path.isfile('dftpy_stopfile'): exit()


traj = Trajectory("md_ngbrv.traj", "w", atoms)

dyn.attach(check_stop, interval=1)
dyn.attach(printenergy, interval=1)
dyn.attach(traj.write, interval=1)

dyn.run(20000)
# from ase.geometry.analysis import Analysis
# analysis = Analysis(list(Trajectory('md_ngbrv.traj')))
# rdf = analysis.get_rdf(rmax=5, nbins=100, return_dists=True)
# rdf = np.asarray(rdf).mean(axis=0)
# np.save('rdf_ngbrv', rdf)
