import os


os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee textfiles/{}.txt".format('/Muon/Run2022D-PromptNanoAODv10-v1/NANOAOD', 'Run2022D'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee textfiles/{}.txt".format('/Muon/Run2022E-PromptNanoAODv10_v1-v2/NANOAOD', 'Run2022E'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee textfiles/{}.txt".format('/Muon/Run2022E-PromptNanoAODv10_v1-v1/NANOAOD', 'Run2022E-v1'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee textfiles/{}.txt".format('file dataset=/Muon/Run2022C-PromptNanoAODv10-v1/NANOAOD', 'Run2022C'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee textfiles/{}.txt".format('/JetMET/Run2022E-PromptNanoAODv10_v1-v2/NANOAOD', 'Run2022E-JetMET-v2'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee textfiles/{}.txt".format('/JetMET/Run2022F-PromptNanoAODv10_v1-v2/NANOAOD', 'Run2022F'))



