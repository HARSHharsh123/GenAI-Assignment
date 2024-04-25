from setuptools import find_packages , setup



def get_requirements(file_path):
    '''
        This Function will Return the List of Requirements
    '''
    requirements = []

    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        ## readlines() will also read \n so are task is to remove \n from this list
        requirements = [req.replace('\n' , "") for req in requirements]
    return requirements

setup(
    name = 'mcqgenai projectt',
    version = '0.0.0.0.1',
    author='Harsh Shukla',
    author_email= 'hs0814497@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)