@echo off

rem Install virtual environment if not already installed
pip install virtualenv

rem Create virtual environment
python -m venv venv

rem Activate the virtual environment
call venv\Scripts\activate

rem Install dependencies from local source
pip install -e .

echo Setup completed !!!
