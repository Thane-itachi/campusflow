CampusFlow — AI Learning Log

1. Project Overview

Project name: CampusFlow
Project type: Python CLI Helpdesk Ticket Management System
Role: Engineer A
Language: Python
Testing framework: "unittest"
Data storage: JSON

CampusFlow is a command-line application that allows users to create tickets, view existing tickets, update ticket statuses, assign tickets, and search for tickets. The project helped me practise Python functions, dictionaries, lists, validation, file handling, modular programming, and automated testing.

2. How I Used AI

I used AI as a learning assistant to help me understand Python concepts, review code, investigate errors, and develop test cases for CampusFlow.

AI helped me with:

- Understanding how functions receive arguments and return values.
- Understanding ticket creation and validation.
- Reviewing priority calculation rules and identifying possible logic errors.
- Understanding how Python modules can be separated into different files.
- Learning how JSON data can be saved to and loaded from files.
- Understanding automated testing with Python's "unittest" module.
- Designing boundary tests, invalid-input tests, and workflow tests.
- Preparing evidence for the project's testing and reliability audit.

I used AI explanations to improve my understanding rather than treating every suggested answer as automatically correct.

3. Key Lessons Learned

A. Functions and validation

I learned that a function can validate input before performing an operation. For example, "create_ticket()" checks whether the title, category, urgency, and number of affected users are valid before returning a ticket dictionary.

I also learned that invalid input should be handled deliberately so that it does not create incorrect ticket records.

Relevant file: "campusflow/tickets.py"

B. Conditional logic and priority calculation

I learned how "if", "elif", and "else" statements determine ticket priority based on urgency and the number of affected users.

The project priority rules are:

- High urgency and at least 10 affected users: critical.
- High urgency or at least 10 affected users: high, unless the critical rule applies.
- Medium urgency or at least 3 affected users: medium, unless a higher-priority rule applies.
- Otherwise: low.

I learned that boundary cases matter. For example, a low-urgency ticket affecting three users should receive medium priority under these rules. This helped me understand why testing only ordinary inputs is not enough.

Relevant function: "calculate_priority()" in "campusflow/tickets.py"

C. Lists and dictionaries

I learned how a list can hold multiple ticket dictionaries and how dictionary keys allow the program to access ticket information such as "id", "title", "priority", "status", and "assigned_to".

I also learned that a list must be accessed using an integer index, while dictionary values are accessed using their keys.

D. JSON persistence

I learned how JSON allows ticket information to remain available after the application closes.

The storage module uses saving and loading functions to write ticket data to a file and retrieve it later. I also learned why malformed JSON and unexpected data structures need to be handled.

Relevant file: "campusflow/storage.py"

E. Automated testing

I learned how to run Python unit tests with:

"python3 -m unittest discover -s test -v"

The verbose option helps identify individual tests and makes failures easier to investigate.

I also learned that a test should assert an expected business outcome, rather than simply checking that a function executes without crashing.

F. Workflow validation

I learned that changing a ticket's status should follow the project's workflow rules. A ticket should not be allowed to move through an invalid sequence of states if the requirements prohibit that transition.

Relevant file: "campusflow/workflow.py"

4. AI-Assisted Code Review

During code review, I examined the priority calculation logic and identified a boundary case worth testing: low urgency with four affected users.

Under the project rules, the expected priority is "medium". An earlier version of the function returned "low", indicating that its conditions needed to be reviewed.

This taught me to compare code against written requirements and verify AI-assisted findings through actual execution.

5. New Test Case Designed

Test name: Reject ticket creation when affected users is zero.

Input:

"create_ticket("T999", "Network outage", "Network", "high", 0)"

Expected result: The function raises "ValueError" because the number of affected users must be a positive integer.

Actual result: To be recorded after executing the test on the audited commit.

Status: Proposed test; execution not yet verified.

Why it matters: It helps ensure invalid data cannot be used to create a ticket and interfere with ticket records or priority calculations.

6. Responsible Use of AI

I learned that AI-generated code and explanations should be reviewed before being accepted. A suggested solution may contain incorrect assumptions, overlook a project requirement, or fail on boundary cases.

For CampusFlow, I should:

- Read and understand suggested code before using it.
- Compare implementations against the project requirements.
- Run automated tests after code changes.
- Record actual test results rather than assuming that code works.
- Avoid including passwords, API keys, or other secrets in prompts or source control.
- Be transparent about where AI assistance was used.

7. Evidence and Verification

Test command: "python3 -m unittest discover -s test -v"

Commit SHA: To be recorded from the commit being audited.

Actual number of tests executed: To be recorded after running the test suite.

Test result: To be recorded from the real terminal output.

Known issue to verify: Priority calculation for low urgency with three or more affected users.

Additional checks: Invalid input handling, illegal workflow transitions, duplicate ticket IDs, and JSON persistence.

8. Reflection

Working on CampusFlow helped me connect Python concepts to a practical application. I improved my understanding of functions, validation, data structures, modules, JSON storage, and automated testing.

The most important lesson was that writing code is only one part of software development. Understanding requirements, testing edge cases, reviewing failures, and documenting evidence are also essential.

My next step is to run the complete test suite on the integrated project, review any failures, and document the verified results before completing the sprint audit.