---
# TTbarAllHad

So far, this will compute the mistag rates for all the data.

```
cmsrel CMSSW_9_4_4
cd CMSSW_9_4_4/src
cmsenv
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
git clone https://github.com/b2g-nano/TTbarAllHad.git Analysis/TTbarAllHad
git clone https://github.com/rappoccio/PredictedDistribution.git Analysis/PredictedDistribution
scram b -j 10
cd Analysis/TTbarAllHad/test
ln -s ../../../PhysicsTools/NanoAODTools/scripts/haddnano.py .
```
---
## Running trigger study and control plots


### 1: Make trigger histograms (interactively on cmslpc/lxplus)

Main class is in [TTbarResTrigsHadronic.py](https://github.com/b2g-nano/TTbarAllHad/blob/master/python/TTbarResTrigsHadronic.py)

Driver command is in [run_trigs.py](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/run_trigs.py)

```
python run_trigs.py
```

### 2: Make control histograms 

Main class is in [TTbarResControlPlotsHadronic.py](https://github.com/b2g-nano/TTbarAllHad/blob/master/python/TTbarResControlPlotsHadronic.py)

Driver command is in [run_controlplots.py](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/run_controlplots.py)


```
python run_controlplots.py
```

Running on CRAB can be done by:

```
python submit.py -c PSet.py -d ControlPlots -f <dataset_file> -t ControlPlots --shscript crab_script_controlplots.sh --nanoscript run_controlplots.py -o ttbarreshad.root
```

### 3: Plot trigger turnon (interactively on laptop)

Execute the python notebook [test/trigs/trigger_calcs.ipynb](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/trigs/trigger_calcs.ipynb).

### 4: Plot control plots (interactively on laptop)

Execute the python notebook [test/controlplots/control_plots.ipynb](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/controlplots/control_plots.ipynb).

---
## Running main analysis background estimate

### 1: Create mistag rates in data

Main class is in [TTbarResAnaHadronic](https://github.com/b2g-nano/TTbarAllHad/blob/master/python/TTbarResAnaHadronic.py)

Driver is [run_write_mistagrate.py](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/run_write_mistagrate.py)



To run in CRAB:
```
python submit.py -c PSet.py -d WriteMistags -f <dataset_file> -t WriteMistags --shscript crab_script_mistag.sh --nanoscript run_write_mistagrate.py -o ttbarreshad.root
```

Then hadd together the various crab files:

```
hadd JetHT_Run2018A-22May2018-v1_AntiTag.root `xrdfsls -u   /store/user/rappocc/CRAB_UserFiles/JetHT_Run2018A-22May2018-v1_WritePredDist/180614_171959/0000 | grep .root`
hadd JetHT_Run2018A-PromptReco-v1_AntiTag.root `xrdfsls -u   /store/user/rappocc/CRAB_UserFiles/JetHT_Run2018A-PromptReco-v1_WritePredDist/180614_172125/0000 | grep .root`
hadd JetHT_Run2018A-PromptReco-v2_AntiTag.root `xrdfsls -u   /store/user/rappocc/CRAB_UserFiles/JetHT_Run2018A-PromptReco-v2_WritePredDist/180614_172552/0000 | grep .root`
hadd JetHT_Run2018A-PromptReco-v3_AntiTag.root `xrdfsls -u   /store/user/rappocc/CRAB_UserFiles/JetHT_Run2018A-PromptReco-v3_WritePredDist/180614_172647/0000 | grep .root`
hadd JetHT_Run2018B-PromptReco-v1_AntiTag.root `xrdfsls -u   /store/user/rappocc/CRAB_UserFiles/JetHT_Run2018B-PromptReco-v1_WritePredDist/180614_173151/0000 | grep .root`
...
```

You will need to replace the path name with your own EOS space
(wherever the jobs in the previous command were writing to).

Finally move the files into the "mistag" folder:

```
mv *AntiTag*.root mistag/
```


### 2: Create mistag rates for ttbar MC


Main class is in [TTbarResAnaHadronic](https://github.com/b2g-nano/TTbarAllHad/blob/master/python/TTbarResAnaHadronic.py)

#Driver is [run_write_mistagrate_ttbarmc.py](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/run_write_mistagrate_ttbarmc.py)

```
python run_write_mistagrate_mc.py
```

To run on CRAB:

```
python submit.py -c PSet.py -d WriteMistags -f datasets_mc_2018_fall18.txt -t WriteMistagsMC --shscript crab_script_mistag.sh --nanoscript run_write_mistagrate.py -o ttbarreshad.root
```

Move the resulting file to the mistag folder:

```
mv mistag_TTToHadronic_TuneCP5_13TeV-powheg-pythia8_AntiTag.root mistags/
```


### 3: Add files together:

```
cd hists/
hadd ControlPlots_crab__JetHT_Run2016-Nano14Dec2018-v1.root ControlPlots_crab__JetHT_Run2016*.root
hadd ControlPlots_crab__JetHT_Run2017-Nano14Dec2018-v1.root ControlPlots_crab__JetHT_Run2017*.root
hadd ControlPlots_crab__JetHT_Run2018-Nano14Dec2018-v1.root ControlPlots_crab__JetHT_Run2018*.root

```

### 3: Create the mistag rates and plots (interactive locally)

Execute the python notebook [test/mistag/mistag_rate.ipynb](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/mistag/mistag_rate.ipynb). 

### 4: Add uncertainties to QCD MC (via CRAB)

Now we need to create new trees for the MCs, adding the jet-related
uncertainties. These are native NANOAOD tools. 

```
python submit_rejec.py -c PSetMC.py -d Uncs -f datasets_qcd.txt -t Uncs
```

---
## Calculate the background estimate

Main class is in [TTbarResAnaHadronic.py](https://github.com/b2g-nano/TTbarAllHad/blob/master/python/TTbarResAnaHadronic.py)

Driver command is in [run_plots.py](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/run_plots.py)
```
python run_plots.py 0
```
---
