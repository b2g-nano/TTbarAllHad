python submit.py -c PSet.py -d WriteMistags -f datasets_jetht_2018_rereco.txt -t WriteMistags --shscript crab_script_mistag.sh --nanoscript run_write_mistagrate.py -o ttbarreshad.root
python submit.py -c PSet.py -d WriteMistags -f datasets_mc_2018_fall18.txt -t WriteMistagsMC --shscript crab_script_mistag.sh --nanoscript run_write_mistagrate.py -o ttbarreshad.root

python submit.py -c PSet.py -d ControlPlots -f datasets_jetht_2018_rereco.txt -t ControlPlots --shscript crab_script_controlplots.sh --nanoscript run_controlplots.py -o ttbarreshad.root
python submit.py -c PSet.py -d ControlPlots -f datasets_mc_2018_fall18.txt -t ControlPlotsMC --shscript crab_script_controlplots_mc.sh --nanoscript run_controlplots_mc.py -o ttbarreshad.root
