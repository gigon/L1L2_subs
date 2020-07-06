from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_data_files

hiddenimports = collect_submodules('en_core_web_sm') 
datas = collect_data_files("en_core_web_sm")
