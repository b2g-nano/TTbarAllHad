---
# TTbarAllHad

So far, this will compute the mistag rates for all the data.

```
cmsrel CMSSW_10_2_9
cd CMSSW_10_2_9/src
cmsenv
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
git clone https://github.com/b2g-nano/TTbarAllHad.git Analysis/TTbarAllHad
git clone https://github.com/rappoccio/PredictedDistribution.git Analysis/PredictedDistribution
scram b -j 10
cd Analysis/TTbarAllHad/test
ln -s ../../../PhysicsTools/NanoAODTools/scripts/haddnano.py .
```
---
## Run trigger study


### Make trigger histograms (interactively on cmslpc/lxplus)

Main class is in [TTbarResTrigsHadronic.py](https://github.com/b2g-nano/TTbarAllHad/blob/master/python/TTbarResTrigsHadronic.py)

Driver command is in [run_trigs.py](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/run_trigs.py)

```
python run_trigs.py
```

### Plot trigger histograms (interactively on laptop)

Execute the python notebook [test/trigs/trigger_calcs.ipynb](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/trigs/trigger_calcs.ipynb).


## Control region

### Make control histograms 

Main class is in [TTbarResControlPlotsHadronic.py](https://github.com/b2g-nano/TTbarAllHad/blob/master/python/TTbarResControlPlotsHadronic.py)

Driver command is in [run_controlplots.py](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/run_controlplots.py)

```
python run_controlplots.py
```

Running on CRAB can be done by:

```
python submit.py -c PSet.py -d ControlPlots -f <dataset_file> -t ControlPlots --shscript crab_script_controlplots.sh --nanoscript run_controlplots.py -o ttbarreshad.root
```


#### Plot control histograms (interactively on laptop)

Execute the python notebook [test/controlplots/control_plots.ipynb](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/controlplots/control_plots.ipynb).

---
## Running main analysis background estimate

### Create mistag rates

Main class is in [TTbarResAnaHadronic](https://github.com/b2g-nano/TTbarAllHad/blob/master/python/TTbarResAnaHadronic.py)

Driver is [run_write_mistagrate.py](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/run_write_mistagrate.py)



To run in CRAB:
```
python submit.py -c PSet.py -d WriteMistags -f <dataset_file> -t WriteMistags --shscript crab_script_mistag.sh --nanoscript run_write_mistagrate.py -o ttbarreshad.root
```

#### Plot the mistag rates (interactive locally)

Execute the python notebook [test/mistag/mistag_rate.ipynb](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/mistag/mistag_rate.ipynb). 


---
## Calculate the background estimate

Main class is in [TTbarResAnaHadronic.py](https://github.com/b2g-nano/TTbarAllHad/blob/master/python/TTbarResAnaHadronic.py)

Driver command is in [run_plots.py](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/run_plots.py)
```
python run_plots.py 0
```
---



## Add uncertainties to QCD MC (via CRAB)

Now we need to create new trees for the MCs, adding the jet-related
uncertainties. These are native NANOAOD tools. 

```
python submit_rejec.py -c PSetMC.py -d Uncs -f datasets_qcd.txt -t Uncs
```

