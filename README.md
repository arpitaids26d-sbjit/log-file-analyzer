# Automated Log File Analyzer

A simple Python program that reads a system log file, finds Errors, Warnings and Info messages, counts them, shows the most common problems, and saves a summary report in a text file.

**Author:** Sonali Nirmal
**Course:** Python Programming Lab (N-PCCCD304P), CSE (DS), Semester III
**Institute:** S. B. Jain Institute of Technology, Management & Research, Nagpur

---

## Features

- Reads log messages from a text file
- Identifies ERROR, WARNING and INFO messages
- Counts each type of message and shows percentages
- Shows the top 3 most common errors and warnings
- Shows the severity of each type and the overall system severity
- Prints a summary report and saves it in `report.txt`
- Handles missing files, empty files and wrongly formatted lines

---

## Project Structure

```
log-file-analyzer/
├── log_analyzer.py     Main Python program
├── sample_logs.txt     Sample log messages
├── report.txt          Report created by the program
├── README.md           Project description
├── .gitignore          Files Git should ignore
└── docs/               Project report (PDF)
```

---

## Installation

1. Install Python 3.8 or higher from https://www.python.org
2. Install Git from https://git-scm.com
3. Download the project:

```
git clone https://github.com/sonalinds26d-boop/log-file-analyzer.git
cd log-file-analyzer
```

No extra libraries are needed. The program uses only built-in Python modules.

---

## How to Run

```
python log_analyzer.py
```

The report is shown on the screen and saved in `report.txt`.

---

## Log File Format

Each line must look like this:

```
YYYY-MM-DD HH:MM:SS LEVEL Message text
```

Example:

```
2026-10-16 08:02:30 ERROR Database connection failed
```

LEVEL can be `ERROR`, `WARNING` or `INFO`. Lines in any other format are skipped and counted as "skipped lines".

---

## Severity Levels

| Message Type | Severity |
|---|---|
| ERROR | HIGH |
| WARNING | MEDIUM |
| INFO | LOW |

Overall system severity:

- **HIGH:** 5 or more errors
- **MEDIUM:** 1 to 4 errors, or 5 or more warnings
- **LOW:** no errors and fewer than 5 warnings

---

## How the Program Works (Logic Summary)

1. The program opens `sample_logs.txt`.
2. It checks that the file exists and is not empty.
3. Each line is split into date, time, level and message.
4. A counter is increased for every ERROR, WARNING and INFO.
5. A dictionary stores how many times each error and warning message appears.
6. The dictionary is sorted to find the top 3 most common messages.
7. A report is built, printed on the screen and saved in `report.txt`.

---

## Python Concepts Used

- Variables, `if / elif / else`, `for` loops
- Strings, lists, tuples and dictionaries
- Functions
- File handling and exception handling (`try / except`)
- Object Oriented Programming (class `LogAnalyzer`)

---

## Sample Output

For the included `sample_logs.txt`:

- Total Errors: 6
- Total Warnings: 6
- Total Info messages: 8
- Most common error: Database connection failed (3 times)
- Most common warning: Disk usage above 80 percent (3 times)
- Overall severity: HIGH