from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_dynamic_libs
from PyInstaller.utils.hooks import collect_data_files

hiddenimports = collect_submodules('sklearn') 
binaries = collect_dynamic_libs('sklearn', destdir='./sklearn/.libs/')
datas = collect_data_files('sklearn')
