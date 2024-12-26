from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path:str) -> List[str]:
    '''
    Read the requirements.txt file and return a list of requirements
    '''
    requirements = []
    with open(file_path) as f:
        requirements = f.read().splitlines()

    if HYPHEN_E_DOT in requirements:
        requirements.remove(HYPHEN_E_DOT)

    return requirements

if __name__ == "__main__":
    print(get_requirements('requirements.txt'))