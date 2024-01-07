# QR-register<!-- omit from toc -->

## Table of Contents<!-- omit from toc -->

- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Creating QR codes](#creating-qr-codes)
  - [Formatting the Google Sheets](#formatting-the-google-sheets)
  - [Initial configuration](#initial-configuration)
  - [Scanning the QR](#scanning-the-qr)
- [Troubleshooting](#troubleshooting)

## Built with<!-- omit from toc -->

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  

## Getting started

### Prerequisites

- OAuth credentials - obtain from [me](ghuynh2@bisvietnam.com)
  > [!CAUTION]  
  > Sharing the credentials will allow potential malicious activites to be performed under your account. So please keep my credentials secret :sob::sob::sob:

- Virtual Environment
  
  ```shell
  python -m venv env
  ```

### Installation

Just simply download this repo then move the `env` into the directory, after that open PowerShell and activate the environment with

```shell
cd env
Scripts/activate
cd ..
```

Then install the necessary libraries

```shell
python -m pip install -r requirements.txt
```

## Usage

### Creating QR codes

1. From your spreadsheets app, download the list of delegates name and their email as `delegatesInfo.csv`
    > [!IMPORTANT]  
    > As long as the names are in the first column and the emails are in the last column, then the program will successfully import the data. Anything in the middle will be ignored.  

2. Move the file into `QR-register/`

3. Run `src/qrCreate.py`

   ```shell
   python src/qrCreate.py
   ```

4. Delete `qrcodes/a.txt` file

### Formatting the Google Sheets

Just ensure that the delegate's email and their attendance cell are both located on the same row

### Initial configuration

Find `src/config.json` which contains all the configuration of the program.

- camera_id: 0 (default) for webcam or 1 for back cam
- sheets_id: The ID of the Google Sheets used for attendance
  ![sheets id](images/sheetsID.png)
- register_column: The column in which attendance will be marked
- mail_column: The column in which the delegates' mail are placed
- start_row: The row containing the first delegate  

An example configuration might look like

```json
{
    "camera_id": 1,
    "sheets_id": "1UT_GerjzJCv7Bu_MnEMHZUr533mF3xe0W0rMiUlHnq4",
    "register_column": "G",
    "mail_column": "C",
    "start_row": 3
}
```

### Scanning the QR

1. Move `credentials.json` into `QR-register/auth/`

2. Run `src/main.py`

3. If it is your first time running, a Google sign-in prompt may open. Make sure to sign in with the account that has access to the attendance spreadsheet

4. As one scan their QR, a green frame will be drawn around it if login successful as well as their email address appearing in green underneath

5. Once all the delegates have registered, close the window then wait for the program to sync the data with the Google Sheets

## Troubleshooting

Sign in with the wrong Google Account? Delete the `auth/token.json` then run `src/main.py` again 
> [!CAUTION]  
> Again, do not share this token to anyone (same reason as credentials)

QR code not registering? Make sure the QR code is perpendicular to the camera and lighting is neither too dark nor too bright
