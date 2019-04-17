from setuptools import setup, find_packages

def read_file(fname):
    with open(fname, 'r') as f:
        return f.read()

setup(
    name="tmuxer",
    version='0.0.2',
    author='Shubham Naik',
    author_email='shub@shub.club',
    description='Quick tool that creates tmux interfaces from a conf file',
    long_description=read_file('./README.md'),
    url='https://github.com/4shub/quicklinks/',
    py_modules=['tmuxer'],
    zip_safe=False,
    install_requires=read_file('./dependencies.txt'),
    license='MIT',
    entry_points= {
        "console_scripts": [
            "tmuxer = tmuxer:tmuxer",
        ]
    }
)