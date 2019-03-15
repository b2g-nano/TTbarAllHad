# Submit the crab files 

python submit.py -c PSet.py -d WriteMistags -f datasets/datasets_jetht_13TeV_Nano14Dec2018.txt -t WriteMistags --shscript crab_script_mistag.sh --nanoscript run_write_mistagrate.py -o ttbarreshad.root -l all_goodruns_13TeV.txt
python submit.py -c PSet.py -d WriteMistags -f datasets/datasets_all_Nano14Dec2018.txt -t WriteMistags --shscript crab_script_mistag.sh --nanoscript run_write_mistagrate.py -o ttbarreshad.root
python submit.py -c PSet.py -d ControlPlots -f datasets/datasets_jetht_13TeV_Nano14Dec2018.txt -t ControlPlots --shscript crab_script_controlplots.sh --nanoscript run_controlplots.py -o ttbarreshad.root -l all_goodruns_13TeV.txt
python submit.py -c PSet.py -d ControlPlots -f datasets/datasets_all_Nano14Dec2018.txt -t ControlPlots --shscript crab_script_controlplots.sh --nanoscript run_controlplots.py -o ttbarreshad.root

# After output, get the results
python multicrab.py -c status -w ControlPlots
python multicrab.py -c status -w WriteMistags

# Add them together
python hadd_files.py -d WriteMistags
hadd WriteMistags_crab__JetHT_Run2016-Nano14Dec2018-v1.root crab__JetHT_Run2016*.root
hadd WriteMistags_crab__JetHT_Run2017-Nano14Dec2018-v1.root crab__JetHT_Run2017*.root
hadd WriteMistags_crab__JetHT_Run2018-Nano14Dec2018-v1.root crab__JetHT_Run2018*.root
python hadd_files.py -d ControlPlots
hadd ControlPlots_crab__JetHT_Run2016-Nano14Dec2018-v1.root crab__JetHT_Run2016*.root
hadd ControlPlots_crab__JetHT_Run2017-Nano14Dec2018-v1.root crab__JetHT_Run2017*.root
hadd ControlPlots_crab__JetHT_Run2018-Nano14Dec2018-v1.root crab__JetHT_Run2018*.root

#
# Next : run the ipynbs for mistags and control plots. These will create files that are used for the bkg estimate.
#
#  (This is interactive)
# 
#
# The outputs are then copied to specific files:
# 
cp hists/ControlPlots_crab__QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8_RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X.root ./modmass.root
mv mistag/mistag_rates.root .


# Now run the background estimation. 
python submit.py -c PSet.py -d BkgEstimate -f datasets/datasets_jetht_13TeV_Nano14Dec2018.txt -t BkgEstimate --shscript crab_script.sh --nanoscript run_plots.py -o ttbarreshad.root -l all_goodruns_13TeV.txt
python submit.py -c PSet.py -d BkgEstimate -f datasets/datasets_all_Nano14Dec2018.txt -t BkgEstimate --shscript crab_script.sh --nanoscript run_plots.py -o ttbarreshad.root

# Add them together
python hadd_files.py -d BkgEstimate
hadd BkgEstimate_crab__JetHT_Run2016-Nano14Dec2018-v1.root BkgEstimate_crab__JetHT_Run2016*.root
hadd BkgEstimate_crab__JetHT_Run2017-Nano14Dec2018-v1.root BkgEstimate_crab__JetHT_Run2017*.root
hadd BkgEstimate_crab__JetHT_Run2018-Nano14Dec2018-v1.root BkgEstimate_crab__JetHT_Run2018*.root
mv BkgEstimate_crab__JetHT_Run201*.root hists/


