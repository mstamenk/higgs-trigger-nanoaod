import os

das_cmd = 'dasgoclient -query=\"file dataset={}\" 2>&1 | tee data/dataset_lists/{}.txt'

datasets = {
    'Run22C_Muon' : '/Muon/Run2022C-PromptNanoAODv10-v1/NANOAOD',
    'Run22D_Muon' : '/Muon/Run2022D-PromptNanoAODv10_v2-v1/NANOAOD',
    'Run22E_Muon' : '/Muon/Run2022E-PromptNanoAODv10_v1-v3/NANOAOD',
    'Run22F_Muon' : '/Muon/Run2022F-PromptNanoAODv10_v1-v2/NANOAOD',

    'Run22C_JetMET' : '/JetMET/Run2022C-PromptNanoAODv10-v1/NANOAOD',
    'Run22D_JetMET' : '/JetMET/Run2022D-PromptNanoAODv10_v2-v1/NANOAOD',
    'Run22E_JetMET' : '/JetMET/Run2022E-PromptNanoAODv10_v1-v3/NANOAOD',
    'Run22F_JetMET' : '/JetMET/Run2022F-PromptNanoAODv10_v1-v2/NANOAOD',

    'Run18D_SingleMuon' : '/SingleMuon/Run2018D-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD  run=325022',
    'Run18D_JetHT' : '/JetHT/Run2018D-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD run=325022',

}                               

for key in datasets:
    os.system(das_cmd.format(datasets[key],key))
