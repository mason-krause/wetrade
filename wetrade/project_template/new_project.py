from pathlib import Path
import shutil
import os


def new_project():
  src_dir = os.path.dirname(str(__file__))
  files = os.listdir(src_dir)
  ignore = ['new_project.py', 'trading_session.py', '__init__.py', '__pycache__']
  dest_files = os.listdir('.')
  for filename in files:
    if filename not in [*ignore, *dest_files]:
      shutil.copy2(os.path.join(src_dir, filename), '.')