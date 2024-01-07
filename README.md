# QR-register

## Getting started

### Prerequisites

* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  
* OAuth credentials - obtain from [me](ghuynh2@bisvietnam.com)
  > [!CAUTION]  
  > Sharing the credentials will allow potential malicious activites to be performed under your account. So please keep my credentials secret :sob:

### Installation

Just simply download this repo then open PowerShell in the file directory and install the below.

* Virtual Environment

    ```shell
    python -m venv env
    cd env
    Scripts/activate
    cd ..
    ```

* Libraries

    ```shell
    python -m pip install -r requirements.txt
    ```

## Usage

### Creating QR codes

1. From your spreadsheets app, download the list of delegates name and their email as a `.csv` file
    > [!IMPORTANT]  
    > As long as the names are in the first column and the emails are in the last column, then the program will successfully import the data

2. Run `qrCreate.py`

3. Delete `a.txt` file

### Registrating
