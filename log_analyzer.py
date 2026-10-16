"""
Automated Log File Analyzer
---------------------------
This program reads a log file, finds Errors, Warnings and Info
messages, counts them, shows the most common problems, and saves
a summary report in a text file.

Expected log line format:
2026-10-16 10:15:32 ERROR Database connection failed
"""

import os

# ---------------- Settings ----------------
LOG_FILE = "sample_logs.txt"
REPORT_FILE = "report.txt"

# Severity of each message type
SEVERITY = {
    "ERROR": "HIGH",
    "WARNING": "MEDIUM",
    "INFO": "LOW",
}


# ---------------- Helper functions ----------------
def get_count(item):
    """Return the count from a (message, count) pair."""
    return item[1]


def top_messages(message_dict, how_many=3):
    """Return the most common messages from a dictionary."""
    sorted_items = sorted(message_dict.items(), key=get_count, reverse=True)
    return sorted_items[:how_many]


def percentage(part, total):
    """Return percentage of part out of total."""
    if total == 0:
        return 0.0
    return (part / total) * 100


# ---------------- Main class ----------------
class LogAnalyzer:
    """Reads a log file and analyzes its messages."""

    def __init__(self, file_name):
        self.file_name = file_name
        self.counts = {"ERROR": 0, "WARNING": 0, "INFO": 0}
        self.error_messages = {}
        self.warning_messages = {}
        self.total_lines = 0
        self.skipped_lines = 0

    def read_file(self):
        """Read the log file. Return a list of lines, or None if there is a problem."""
        # Check 1: does the file exist?
        if not os.path.exists(self.file_name):
            print("Error: The file '" + self.file_name + "' was not found.")
            return None

        # Check 2: can we open and read it?
        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except OSError:
            print("Error: Could not read the file '" + self.file_name + "'.")
            return None

        # Check 3: is the file empty (or only blank lines)?
        real_lines = []
        for line in lines:
            if line.strip() != "":
                real_lines.append(line.strip())

        if len(real_lines) == 0:
            print("Error: The file '" + self.file_name + "' is empty.")
            return None

        return real_lines

    def analyze(self, lines):
        """Go through each line and count the message types."""
        for line in lines:
            self.total_lines += 1

            # Split into: date, time, level, message
            parts = line.split(" ", 3)

            if len(parts) < 4:
                self.skipped_lines += 1
                continue

            level = parts[2].upper()
            message = parts[3]

            if level == "ERROR":
                self.counts["ERROR"] += 1
                self.error_messages[message] = self.error_messages.get(message, 0) + 1
            elif level == "WARNING":
                self.counts["WARNING"] += 1
                self.warning_messages[message] = self.warning_messages.get(message, 0) + 1
            elif level == "INFO":
                self.counts["INFO"] += 1
            else:
                self.skipped_lines += 1

    def overall_severity(self):
        """Decide the overall health of the system."""
        errors = self.counts["ERROR"]
        warnings = self.counts["WARNING"]

        if errors >= 5:
            return "HIGH - Immediate attention needed"
        elif errors >= 1 or warnings >= 5:
            return "MEDIUM - Needs to be checked"
        else:
            return "LOW - System looks healthy"

    def build_report(self):
        """Create the report as one text string."""
        total_valid = self.counts["ERROR"] + self.counts["WARNING"] + self.counts["INFO"]
        report = []

        report.append("=" * 50)
        report.append("        LOG FILE ANALYSIS REPORT")
        report.append("=" * 50)
        report.append("File analyzed      : " + self.file_name)
        report.append("Total lines read   : " + str(self.total_lines))
        report.append("Valid log messages : " + str(total_valid))
        report.append("Skipped lines      : " + str(self.skipped_lines))
        report.append("")

        report.append("--- MESSAGE COUNT SUMMARY ---")
        report.append("Total Errors       : " + str(self.counts["ERROR"]))
        report.append("Total Warnings     : " + str(self.counts["WARNING"]))
        report.append("Total Info         : " + str(self.counts["INFO"]))
        report.append("")

        report.append("--- PERCENTAGE OF EACH TYPE ---")
        for level in self.counts:
            pct = percentage(self.counts[level], total_valid)
            report.append(level + " : " + format(pct, ".1f") + "%")
        report.append("")

        report.append("--- SEVERITY OF ISSUES ---")
        for level in self.counts:
            report.append(level + " messages -> Severity: " + SEVERITY[level]
                          + " (" + str(self.counts[level]) + " found)")
        report.append("Overall system severity: " + self.overall_severity())
        report.append("")

        report.append("--- TOP 3 MOST COMMON ERRORS ---")
        common_errors = top_messages(self.error_messages)
        if len(common_errors) == 0:
            report.append("No errors found.")
        else:
            number = 1
            for message, count in common_errors:
                report.append(str(number) + ". " + message + "  (" + str(count) + " times)")
                number += 1
        report.append("")

        report.append("--- TOP 3 MOST COMMON WARNINGS ---")
        common_warnings = top_messages(self.warning_messages)
        if len(common_warnings) == 0:
            report.append("No warnings found.")
        else:
            number = 1
            for message, count in common_warnings:
                report.append(str(number) + ". " + message + "  (" + str(count) + " times)")
                number += 1

        report.append("")
        report.append("=" * 50)
        report.append("             END OF REPORT")
        report.append("=" * 50)

        return "\n".join(report)

    def save_report(self, report_text, report_file):
        """Save the report text into a file."""
        try:
            with open(report_file, "w", encoding="utf-8") as file:
                file.write(report_text)
            print("\nReport saved successfully in '" + report_file + "'.")
        except OSError:
            print("Error: Could not save the report.")


# ---------------- Main program ----------------
def main():
    print("Automated Log File Analyzer")
    print("Reading file: " + LOG_FILE + "\n")

    analyzer = LogAnalyzer(LOG_FILE)
    lines = analyzer.read_file()

    # Stop if the file was missing or empty
    if lines is None:
        print("Analysis stopped.")
        return

    analyzer.analyze(lines)
    report_text = analyzer.build_report()

    print(report_text)
    analyzer.save_report(report_text, REPORT_FILE)


main()