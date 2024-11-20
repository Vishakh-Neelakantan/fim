
File Integrity Manager
Submitted By
Name: Vishakh
Semester: Seventh
Course: Cybersecurity

Abstract
This project presents a File Integrity Manager that continuously monitors a specified directory for any file modifications, deletions, and creations. Using the SHA-256 hashing algorithm, it ensures that files are not tampered with. In case of any changes, real-time alerts are sent via email, enhancing system security and providing prompt notifications to users.

Objectives
Monitor file system events such as file creation, modification, and deletion.
Ensure file integrity by calculating and comparing SHA-256 hashes.
Send real-time email notifications for each detected event.
Provide robust error handling, especially for permission issues.
Features
Event Detection: Tracks file events (create, modify, delete) using the Watchdog library.
Hash Verification: Computes file hashes using SHA-256 to detect unauthorized changes.
Real-Time Alerts: Sends email alerts for any file system activity.
Error Handling: Gracefully handles PermissionError during file access.
System Design
Modules
File Monitoring
Implements FileSystemEventHandler from the Watchdog library.
Detects events (on_created, on_modified, on_deleted).

Hash Calculation
Uses SHA-256 to compute file hashes.
Ensures efficient and accurate detection of changes.

Email Notification
Sends alerts using Python's smtplib.
Supports local SMTP debugging for testing purposes.

Initialization
Precomputes hashes for all files in the monitored directory during startup.
