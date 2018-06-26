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

## Interactive running:
```
python run_plots.py 0
```

## Running trigger study and control plots

### 1: Make trigger histograms (interactively on cmslpc/lxplus)
```
python run_trigs.py
```

### 2: Make control histograms (interactively on cmslpc/lxplus)
```
python run_controlplots.py
```

### 3: Plot trigger turnon (interactively on laptop)

Execute the python notebook [test/trigs/trigger_calcs.ipynb](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/trigs/trigger_calcs.ipynb).

### 3: Plot control plots (interactively on laptop)

Execute the python notebook [test/controlplots/control_plots.ipynb](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/controlplots/control_plots.ipynb).

## Running main analysis background estimate

### 1: Create mistag rates in data (via CRAB)

Run the crab script over all of the datasets in "datasets_jetht.txt".

```
python submit_all_uif.py -c PSet.py -d WritePredDist -f datasets_jetht.txt
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


### 2: Create mistag rates for ttbar MC (interactive on cmslpc/lxplus)

The ttbar MC is small enough to execute interactively. We can skip
the calculation of all of the uncertainties because it will be used
only to subtract the ttbar MC from the mistag rates: 

```
python run_write_mistagrate_ttbarmc.py
```

Move the resulting file to the mistag folder:

```
mv mistag_TTToHadronic_TuneCP5_13TeV-powheg-pythia8_AntiTag.root mistags/
```


### 3: Create the mistag rates and plots (interactive locally)

Execute the python notebook [test/mistag/mistag_rate.ipynb](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/mistag/mistag_rate.ipynb). 

### 4: Add uncertainties to QCD MC (via CRAB)

Now we need to create new trees for the MCs, adding the jet-related
uncertainties. 

```
python submit_rejec.py -c PSetMC.py -d Uncs -f datasets_qcd.txt -t Uncs
```
