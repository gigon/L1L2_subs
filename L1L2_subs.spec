# -*- mode: python ; coding: utf-8 -*-

import PyInstaller
import sys
from os import path

site_packages = next(p for p in sys.path if 'site-packages' in p)

datas = []
datas.extend([('resources', 'resources')])
datas.extend([(path.join(site_packages,'scikit_learn-0.23.1.dist-info'), 'scikit_learn-0.23.1.egg-info')])
datas.extend([(path.join(site_packages, 'pyphen\\dictionaries'), 'pyphen\\dictionaries')])
datas.extend([(path.join(site_packages, 'en_core_web_sm\\en_core_web_sm-2.3.0\\tokenizer'), 'en_core_web_sm\\')])
datas.extend([(path.join(site_packages, 'en_core_web_sm\\en_core_web_sm-2.3.0\\ner'), 'en_core_web_sm\\ner')])
datas.extend([(path.join(site_packages, 'en_core_web_sm\\en_core_web_sm-2.3.0\\tagger'), 'en_core_web_sm\\tagger')])
datas.extend([('runExe.bat, '.')])

block_cipher = None

a = Analysis(['src\\main.py'],
             pathex=['.'],
             binaries=[],
             datas=datas,
             hiddenimports=[
              'spacy.data.en',
              'spacy.data.en.tokenizer',
              'spacy.kb',
              'spacy.lang', 
              'spacy.lang.en',
              'spacy.lexeme',
              'spacy.matcher._schemas',
              'spacy.morphology',
              'spacy.parts_of_speech',
              'spacy.syntax._beam_utils',
              'spacy.syntax._parser_model',
              'spacy.syntax.arc_eager',
              'spacy.syntax.ner',
              'spacy.syntax.nn_parser',
              'spacy.syntax.stateclass',
              'spacy.tokens',
              'spacy.syntax.transition_system',
              'spacy.tokens._retokenize',
              'spacy.tokens.morphanalysis',
              'spacy.tokens.underscore',
              'spacy.util',
              'spacy.vocab',

              'spacy._align',
              'en_core_web_sm',

              'blis',
              'blis.py',

              'cymem',
              'cymem.cymem',

              'murmurhash',
              'murmurhash.mrmr',

              'preshed.maps',

              'srsly.msgpack.util',

              'thinc.extra.search',
              'thinc.linalg',
              'thinc.neural._aligned_alloc',
              'thinc.neural._custom_kernels',

              'sklearn.utils._cython_blas',
              'sklearn.neighbors.typedefs',
              'sklearn.neighbors.quad_tree',
              'sklearn.tree',
              'sklearn.tree._utils'
            ],
             hookspath=['./pyinstaller-hooks'],
             runtime_hooks=['./pyinstaller-rthooks/pyi_rth_spacy.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='L1L2_subs',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='L1L2_subs')
