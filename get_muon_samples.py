import os

# Updated on Jan 10 2023
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee textfiles/{}.txt".format('/Muon/Run2022C-PromptNanoAODv10_v1-v1/NANOAOD', 'Run2022B'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee textfiles/{}.txt".format('/Muon/Run2022C-PromptNanoAODv10_v1-v1/NANOAOD', 'Run2022C'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee textfiles/{}.txt".format('/Muon/Run2022D-PromptNanoAODv10_v2-v1/NANOAOD', 'Run2022D'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee textfiles/{}.txt".format('/Muon/Run2022E-PromptNanoAODv10_v1-v3/NANOAOD', 'Run2022E'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee textfiles/{}.txt".format('/Muon/Run2022F-PromptNanoAODv10_v1-v2/NANOAOD', 'Run2022F'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee textfiles/{}.txt".format('/Muon/Run2022F-PromptNanoAODv10_v1-v2/NANOAOD', 'Run2022F'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee textfiles/{}.txt".format('/Muon/Run2022G-PromptNanoAODv10_v1-v1/NANOAOD', 'Run2022G'))

# Not updated so far
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee textfiles/{}.txt".format('/JetMET/Run2022E-PromptNanoAODv10_v1-v2/NANOAOD', 'Run2022E-JetMET-v2'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee textfiles/{}.txt".format('/JetMET/Run2022F-PromptNanoAODv10_v1-v2/NANOAOD', 'Run2022F'))



