# Hyperelastic

## SETUP

### Windows

Create a virtual enviorment for the project : \
`pip install venv`  \
`python -m venv venv`  \
`.\venv\Scripts\activate.ps1`  --> depends on the terminal (Powershell = ps1)

For dynamic editing setup use :  \
`pip install -e .`

For create build :  \
`python -m build`
(ha nem fut le... Set-ExecutionPolicy unrestricted)

### Linux

Create a virtual enviorment for the project : \
`pip install virtualenv` \
`python -m venv venv` \
`source venv/bin/activate.csh`

For dynamic editing setup use :  \
`pip install -e .`

### MacOS

`pip install virtualenv` \
`python -m venv venv` \
`source venv/bin/activate`

For dynamic editing setup use :  \
`pip install -e .`

## TEST

Type ' pytest ' in the terminal or run pytest from VScode

## Update the documentation

Open a terminal and to to the \docs folder. Type the following line:\
`.\make.bat html`
