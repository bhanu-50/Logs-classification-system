import re


def classify_with_regex(log_message):
    label = "System Notification"
    regex_patterns = {
        r"User User\d+ logged (in|out).": "User Action",
        r"Backup (started|ended) at .*": label,
        r"Backup completed successfully.": label,
        r"System updated to version .*": label,
        r"File .* uploaded successfully by user .*": label,
        r"Disk cleanup completed successfully.": label,
        r"System reboot initiated by user .*": label,
        r"Account with ID .* created by .*": "User Action"
    }
    
    for pattern, label in regex_patterns.items():
        if re.search(pattern, log_message):
            return label
        
    return None

