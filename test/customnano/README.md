# Processing Custom NANOAOD for 2018 Commissioning

## Recipe

I added my own bug fixes to add the AK8 jet trigger objects, but otherwise this is the out-of-the-box NANOAOD for 10.1.x:

```
cmsrel CMSSW_10_1_6
cd cmsrel CMSSW_10_1_6/src
git cms-merge-topic 23501
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
git clone https://github.com/b2g-nano/TTbarAllHad.git Analysis/TTbarAllHad
git clone https://github.com/rappoccio/PredictedDistribution.git Analysis/PredictedDistribution
scram b -j 10
```

I created a cmsDriver command to make a NANOAOD file:

```
cmsDriver.py test101X -s NANO --eventcontent NANOAOD --datatier NANOAOD --filein /store/data/Run2018A/JetHT/MINIAOD/22May2018-v1/80000/709B561E-505E-E811-BC13-44A842CFC9A5.root --conditions auto:run2_data_promptlike -n 100 --era Run2_2018 --no_exec
```

However this somehow used customization for MC from NANOAOD, so I adjusted that by hand. 

## Datasets

Getting information from [here](https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2018Analysis#DATA). The good lumi list is
`/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-317080_13TeV_PromptReco_Collisions18_JSON.txt`.


Datasets available are:
```
> dasgoclient -query "dataset dataset=/Jet*/*Run2018*/MINIAOD"
/JetHT/Run2018A-22May2018-v1/MINIAOD
/JetHT/Run2018A-PromptReco-v1/MINIAOD
/JetHT/Run2018A-PromptReco-v2/MINIAOD
/JetHT/Run2018A-PromptReco-v3/MINIAOD
/JetHT/Run2018B-PromptReco-v1/MINIAOD
```

These are in the file "datasets_2018.txt"

## CRAB submission

Using my own custom submission script, I have:

```
python submit_all.py -c test101X_NANO.py -f datasets_2018.txt -d NANO2018 -l Cert_314472-317080_13TeV_PromptReco_Collisions18_JSON.txt
```
