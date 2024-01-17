# QR-register<!-- omit from toc -->

## Table of Contents<!-- omit from toc -->

- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [File formatting](#file-formatting)
    - [Attendance sheet](#attendance-sheet)
    - [Delegate's info sheet](#delegates-info-sheet)
  - [Initial configuration](#initial-configuration)
    - [Global values](#global-values)
    - [Attendance](#attendance)
    - [Delegates' info](#delegates-info)
  - [Running the application](#running-the-application)
    - [Creating QR codes](#creating-qr-codes)
    - [Scanning the QR](#scanning-the-qr)
- [Troubleshooting](#troubleshooting)
- [Credits](#credits)

## Built with<!-- omit from toc -->

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  

To run any Python file in the PowerShell:

```shell
python PATH/TO/PYTHON/file.py
```

## Getting started

### Prerequisites

- Virtual Environment
  
  ```shell
  python -m venv env
  ```

- OAuth credentials - obtain from me

> [!CAUTION]  
> Sharing the credentials will allow potential malicious activities to be performed under my account. So please keep my credentials secret :sob::sob::sob:.

### Installation

Just download this repo then move the `env` into the directory, after that open PowerShell and activate the environment

```shell
env/Scripts/activate
```

Then install the necessary libraries

```shell
python -m pip install -r requirements.txt
```

Finally, move the `credentials.json` into `auth/`.

## Usage

### File formatting

All examples can be found in this [Google Sheets](https://docs.google.com/spreadsheets/d/1UT_GerjzJCv7Bu_MnEMHZUr533mF3xe0W0rMiUlHnq4/edit#gid=0).

#### Attendance sheet

- Every delegate should have a unique identifier.
- The delegates' identifier and attendance cell should be on the same row.
- No merged cells should be in the delegates' row.

#### Delegate's info sheet

- Identifier always be in the first column (A).
- Name always be in the second column (B).
- No merged cells should be in the delegates' row.
- Anything can be put after these columns as they will be ignored.

### Initial configuration

Find `src/config.json` which contains all the configuration of the program.  

#### Global values

The first two attributes of `config.json`.

| Attribute         | Meaning                                                  |
|-------------------|----------------------------------------------------------|
| camera_id         | 0 (default) for webcam or 1 for back cam                 |
| sheets_id         | The ID of the Google Sheets used for attendance          |

Example:  
To use the front cam and access the example Google Sheets, the configuration file should look as follows:

```json
{
  "camera_id": 0,
  "sheets_id": "1UT_GerjzJCv7Bu_MnEMHZUr533mF3xe0W0rMiUlHnq4",
}
```

#### Attendance

The attributes within `"attendance": {...}`.

| Attribute         | Meaning                                                  |
|-------------------|----------------------------------------------------------|
| page              | The name of the sheet where the attendance is located    |
| register_column   | The column in which attendance will be marked            |
| identifier_column | The column in which the delegates' identifiers are placed |
| start_row         | The row containing the first delegate                    |

Example:  
To configure the program for registration Room 1 in the example, the configuration file should look as follows:

```json
"attendance": {
  "page": "Room 1",
  "register_column": "G",
  "identifier_column": "C",
  "start_row": 3
}
```

#### Delegates' info

The attributes within `"info": {...}`.

| Attribute         | Meaning                                                  |
|-------------------|----------------------------------------------------------|
| page              | The name of the sheet where the info is located          |
| start_row         | The row containing the first delegate                    |

Example:  
To configure the program to extract data in the example, the configuration file should look as follows:

```json
"info": {
  "page": "delegatesInfo",
  "start_row": 2
}
```

### Running the application

Run `src/main.py`. If it is your first time running, a Google sign-in prompt may open. Make sure to sign in with the account that has access to your attendance spreadsheet.

#### Creating QR codes

1. Click on button that says 'Create QR codes'.

2. The results will be saved in `qrcodes/`.

#### Scanning the QR

1. As one scans their QR, a green frame will be drawn around it if the QR code is detected. Their infomation (Identifier, Name) will also be shown underneath.

2. Once all the delegates have registered, click on button that says `Save and Register` then wait for the program to sync the data with the Google Sheets.

## Troubleshooting

**Sign in with the wrong Google Account?** Delete the `auth/token.json` then run `src/register.py` again.
> [!CAUTION]  
> Again, do not share this token with anyone (same reason as credentials).

**QR code not registering?** Make sure the QR code is perpendicular to the camera and the lighting is neither too dark nor too bright.

**Running scripts is disabled on this system ERROR?** Open PowerShell as Administrator then type

```shell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
```

## Credits

A program made for the BISHCMC MUN club.

Idea proposal: Henry Bui  
Developer: Gia Phu
