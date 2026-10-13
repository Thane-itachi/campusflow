CampusFlow — Design Decision Log

1. Project Overview

Project name: CampusFlow
Project type: Command-Line Helpdesk Ticket Management System
Programming language: Python
Data storage: JSON
Testing framework: Python "unittest"

CampusFlow is designed to manage helpdesk tickets through a command-line interface. Users can create tickets, view tickets, update ticket statuses, assign tickets, and search for existing tickets.

This document records the major design decisions made during development and explains their reasoning.

2. Decision: Use Python

Decision: Python was selected as the implementation language.

Reasoning:

- Python has readable syntax that makes the application easier to develop and maintain.
- It supports functions, dictionaries, lists, modules, file handling, and automated testing.
- It is suitable for building a command-line application without requiring a complex framework.

Trade-off: Python makes the application straightforward to develop, but additional work would be required to turn it into a web-based or multi-user application.

3. Decision: Use a Command-Line Interface

Decision: CampusFlow uses a menu-driven command-line interface.

Reasoning:

- It provides a simple way to demonstrate the application's main features.
- Users can choose operations from a numbered menu.
- It allows the team to focus on business logic and data management before adding a graphical interface.

Trade-off: The interface is less visual and may be less intuitive for users who are unfamiliar with terminal applications.

4. Decision: Separate the Application into Modules

Decision: The code is divided into separate modules based on responsibility.

The main structure is:

CampusFlow/
├── campusflow/
│   ├── __init__.py
│   ├── reports.py
│   ├── storage.py
│   ├── tickets.py
│   └── workflow.py
├── docs/
├── main.py
├── README.md
└── test/
    ├── test_storage.py
    ├── test_ticket.py
    └── test_workflow.py

Reasoning:

- "main.py" handles the command-line interaction.
- "tickets.py" contains ticket creation, validation, ID generation, and priority calculation.
- "storage.py" handles loading and saving ticket data.
- "workflow.py" handles ticket assignment and status transitions.
- "reports.py" provides a separate location for reporting functionality.
- The "test/" directory keeps automated tests separate from application code.

Trade-off: Modular code is easier to maintain and test, but functions and imports must be organized correctly across files.

5. Decision: Represent Tickets as Dictionaries

Decision: Each ticket is represented as a Python dictionary, with multiple tickets stored in a list.

A ticket contains these fields:

- "id"
- "title"
- "category"
- "urgency"
- "affected_users"
- "priority"
- "status"
- "assigned_to"

Reasoning:

- Dictionaries provide clear names for ticket fields.
- Lists make it straightforward to store and iterate over multiple tickets.
- This structure can be converted to and from JSON without introducing a database dependency.

Trade-off: Dictionaries are flexible, but they do not automatically enforce a fixed schema. Validation is therefore necessary to prevent missing or invalid fields.

6. Decision: Calculate Priority from Business Rules

Decision: Ticket priority is calculated from urgency and the number of affected users.

The priority rules are:

1. High urgency and at least 10 affected users: "critical".
2. High urgency or at least 10 affected users: "high", if the critical rule does not apply.
3. Medium urgency or at least 3 affected users: "medium", if a higher-priority rule does not apply.
4. Otherwise: "low".

Reasoning:

- The rules provide a consistent way to classify tickets.
- Tickets affecting more people can receive higher priority.
- High-urgency issues affecting many users can be identified as critical.

Trade-off: Rule-based prioritization is simple and predictable, but it may not capture every real-world factor, such as the importance of a particular service.

Implementation note: The conditions must be evaluated in the correct order so that a critical ticket is not incorrectly classified as high or medium.

7. Decision: Validate Input Before Creating Tickets

Decision: Ticket details are validated before a ticket dictionary is created.

Validation includes:

- Rejecting blank titles.
- Accepting only the supported categories: "Network", "Hardware", "Software", and "Other".
- Accepting only "low", "medium", and "high" urgency values.
- Requiring the number of affected users to be a positive integer.

Reasoning:

- Validation prevents incorrect data from entering the system.
- It reduces the risk of errors during priority calculation, searching, reporting, and persistence.

Trade-off: Validation introduces additional checks, but these checks improve data consistency and reliability.

8. Decision: Use JSON for Persistence

Decision: Ticket data is stored in a JSON file rather than an external database.

Reasoning:

- JSON is readable and easy to inspect during development.
- Python's built-in "json" module supports serialization and deserialization.
- It avoids the additional setup required by a database server.

Trade-off:

- JSON is suitable for a small, single-user project.
- It is not ideal for concurrent writes by multiple users.
- Searching and updating large datasets may become inefficient.
- File corruption and invalid data must be handled.

Reliability consideration: Saving should be tested by writing ticket data and loading it again. The storage implementation should also handle malformed JSON and unexpected data structures.

9. Decision: Use a Dedicated Workflow Module

Decision: Ticket assignment and status transitions are separated from the command-line interface.

Reasoning:

- Workflow rules can be tested independently of user input.
- Status changes can be checked against permitted transitions.
- Separating business rules from interface code makes the application easier to maintain.

Trade-off: A dedicated module requires clear interfaces between the workflow and main application.

Requirement: The implementation should reject prohibited transitions and avoid changing ticket data when an operation is rejected.

10. Decision: Use Automated Unit Testing

Decision: Python's standard-library "unittest" framework is used to test the application.

Reasoning:

- It does not require installing an additional testing package.
- It supports assertions and automated test discovery.
- It allows ticket logic, workflow behavior, and persistence to be tested separately.

The test command for the current directory structure is:

python3 -m unittest discover -s test -v

Trade-off: Unit tests can verify individual components, but additional integration and manual testing are needed to confirm that the complete application works correctly.

Testing requirements:

- Priority boundaries and invalid inputs.
- Ticket creation and assignment.
- Valid and invalid workflow transitions.
- JSON saving and loading.
- Duplicate ticket IDs, if uniqueness is required.
- Regression testing after code changes and integration.

11. Decision: Use Git for Version Control

Decision: Git and GitHub are used to manage project changes and collaboration.

Reasoning:

- Version control records changes to source files.
- Branches allow work to be developed separately.
- Pull requests provide an opportunity to review changes before merging.
- Testing the integrated "main" branch helps identify problems caused by combining contributions.

Trade-off: Branches and pull requests introduce a review process, but this helps reduce integration risks.

12. Known Limitations and Future Improvements

The current design is intended for a small command-line application. Potential future improvements include:

- Replacing JSON storage with SQLite or another database if the project grows.
- Adding stronger duplicate-ID protection.
- Improving handling of file-system errors.
- Adding more comprehensive workflow and integration tests.
- Improving search and reporting features.
- Developing a graphical or web interface.
- Supporting multiple users with appropriate access controls if the application becomes a shared service.

These are potential improvements rather than claims that the features have already been implemented.

13. Summary

CampusFlow uses a modular Python architecture, dictionary-based ticket records, rule-based priority calculation, JSON persistence, and automated testing. These choices keep the initial implementation simple while making the business logic easier to understand and test.

The main design priority is correctness: ticket details should be validated, priorities should follow the documented rules, workflow transitions should be controlled, and saved data should be recoverable and verifiable.

Design decisions should be reviewed as the project develops, particularly if the system needs to support larger datasets, concurrent users, or stronger reliability requirements.