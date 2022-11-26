# Instillation Instructions

You will need python installed on your machine to run this script.
If you are using a windows PC, download the latest version of python 3 from python.org. When installing, make sure to click "Add Python to Path" (see https://medium.com/@omoshalewa/why-you-should-add-python-to-path-and-how-58693c17c443)

# to get the GSheet bit to work

You need to install the following two packages (remove the backticks if pasting into terminal):

`pip3 install --user pipenv install gspread install --upgrade google-api-python-client oauth2client  install gspread`

`pip3 install --user pipenv install gspread install --upgrade google-api-python-client oauth2client  install --upgrade google-api-python-client oauth2client`

# CREDS

You will need to download the Google API creds (ask Jonny) and pass in the path to the creds when you run the program (see below)


# Running Instructions
open terminal
navigate to this folder in terminal
Get your input ready by replacing data.csv with your file.
type `python quant.py <path to creds>` in terminal
i.e `python quant.py /Users/jonathanrankin/Downloads/parts-quantifier-c6b9beaaf2f2.json`




Things to note:


- the highest level item number should be an integer, without decimal places (i.e 5, not 5.0)
