import sys
from .project_template.new_project import new_project

def main():
  try:
    usr_arg = sys.argv[1]
  except:
    usr_arg = ''
  if usr_arg == 'new-project':
    new_project()

if __name__ == '__main__':
  main()