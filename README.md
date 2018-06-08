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

## Running on CRAB:
```
python submit_all_uif.py -c PSet.py -d WritePredDist -f datasets_jetht.txt
```
## Adding Uncertainties to MC:
```
python submit_rejec.py -c PSetMC.py -d Uncs -f datasets_qcd.txt -t Uncs
```
## Creating the mistag rate

Execute the python notebook [test/mistag/mistag_rate.ipynb](https://github.com/b2g-nano/TTbarAllHad/blob/master/test/mistag/mistag_rate.ipynb). 
