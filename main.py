from campusflow.search import search_tickets, filter_tickets
from campusflow.reports import generate_ticket_report
from campusflow.tickets import (
    create_ticket,
    generate_ticket_id,
    validate_category,
    validate_urgency,
    validate_affected_users
)

from campusflow.storage import load_tickets, save_tickets

tickets = load_tickets("tickets.json")

def create_new_ticket():
    while True:
        title = input("Enter ticket title: ").strip()

        if title:
            break

        print("Ticket title cannot be empty. Please try again.")

    while True:
        category = input(
            "Enter ticket category (Network/Hardware/Software/Other): "
        ).strip()

        if validate_category(category):
            break

        print("Invalid category. Please try again.")

    while True:
        urgency = input(
            "Enter its urgency (low/medium/high): "
        ).strip().lower()

        if validate_urgency(urgency):
            break

        print("Invalid urgency. Enter low, medium, or high.")

    while True:
        try:
            affected_users = int(
                input("Enter the number of users affected: ")
            )

            if validate_affected_users(affected_users):
                break

            print("The number of users must be greater than zero.")

        except ValueError:
            print("Please enter a valid whole number.")

    ticket_id = generate_ticket_id(tickets)

    ticket = create_ticket(
        ticket_id,
        title,
        category,
        urgency,
        affected_users
    )

    tickets.append(ticket)
    save_tickets(tickets, "tickets.json")

    print("\nTicket created successfully!")
    print(ticket)


def view_tickets(tickets):
    if not tickets:
        print("\nNo tickets found! You can add your new ticket")
        return

    print("\n=== ALL THE TICKETS IS BEING LISTED NOW ===")

    for ticket in tickets:
        print("------------------------")
        print(f"ID: {ticket['id']}")
        print(f"Title: {ticket['title']}")
        print(f"Category: {ticket['category']}")
        print(f"Urgency: {ticket['urgency']}")
        print(f"Affected Users: {ticket['affected_users']}")
        print(f"Priority: {ticket['priority']}")
        print(f"Status: {ticket['status']}")
        print(f"Assigned To: {ticket['assigned_to']}")

# view_tickets(tickets)

def update_ticket_status(tickets):
    if not tickets:
        print("\nNo ticket found to update")
        return

    ticket_id = input("Enter the ticket ID you want to upadate: ").strip()

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            print(f"\nCurrent status: {ticket['status']}")
            print("1. Open")
            print("2. In progress")
            print("3. Resolved")

            choice = input("Choose the new status of the issue: ").strip()

            if choice == "1":
                ticket["status"] = "open"
            
            elif choice == "2":
                ticket["status"] = "in_progress"

            elif choice == "3":
                ticket["status"] = "resolved"

            else:
                print("Invalid choice")
                return

            save_tickets(tickets, "tickets.json")
            print("Ticket status has been Successfully Updated🎉")


def assign_ticket(tickets):
    if not tickets:
        print("\nNo tickets available to assign.")
        return

    ticket_id = input("Enter the ticket ID: ").strip()

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            name = input("Enter the team member's name: ").strip()

            if not name:
                print("Team members name cannot be empty")
                return

            ticket["assigned_to"] = name

            save_tickets(tickets, "tickets.json")

            print(f"Ticket {ticket_id} assigned to {name} successfully 🎉")
            return

    print("Ticket cannot be found!")

def search_ticket(tickets):
    if not tickets:
        print("\nNo tickets available to search.")
        return

    ticket_id = input("Enter the ticket ID to search for: ").strip()

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            print("\n===== TICKET FOUND =====")
            print(f"ID: {ticket['id']}")
            print(f"Title: {ticket['title']}")
            print(f"Category: {ticket['category']}")
            print(f"Urgency: {ticket['urgency']}")
            print(f"Affected Users: {ticket['affected_users']}")
            print(f"Priority: {ticket['priority']}")
            print(f"Status: {ticket['status']}")
            print(f"Assigned To: {ticket['assigned_to']}")
            return

    print("Ticket ID not found.")

def search_tickets_by_title(tickets):
    """Find tickets using words from their titles."""
    title = input("Enter a word or phrase from the ticket title: ").strip()

    results = search_tickets(tickets, title)

    if results:
        print(f"\nFound {len(results)} matching ticket(s).")
        view_tickets(results)
    else:
        print("\nNo tickets matched your search.")


def filter_tickets_menu(tickets):
    """Allow users to filter tickets by category, status, and priority."""
    print("\nLeave a filter blank to ignore it.")

    category = input(
        "Category (Network/Hardware/Software/Other): "
    ).strip()

    status = input(
        "Status (open/in_progress/resolved): "
    ).strip().lower()

    priority = input(
        "Priority (critical/high/medium/low): "
    ).strip().lower()

    results = filter_tickets(
        tickets,
        category=category or None,
        status=status or None,
        priority=priority or None,
    )

    if results:
        print(f"\nFound {len(results)} matching ticket(s).")
        view_tickets(results)
    else:
        print("\nNo tickets matched those filters.")


def view_ticket_report(tickets):
    """Display ticket statistics."""
    report = generate_ticket_report(tickets)

    print("\n===== CAMPUSFLOW TICKET REPORT =====")
    print(f"Total tickets: {report['total']}")
    print(f"Open tickets: {report['open']}")
    print(f"In-progress tickets: {report['in_progress']}")
    print(f"Resolved tickets: {report['resolved']}")
    print(f"Unresolved tickets: {report['unresolved']}")
    print(
        f"Resolution percentage: "
        f"{report['resolution_percentage']}%"
    )

    print("\nTickets by priority:")
    for priority, count in report["by_priority"].items():
        print(f"  {priority}: {count}")

    print("\nTickets by category:")
    for category, count in report["by_category"].items():
        print(f"  {category}: {count}")

    print("\nTickets by assignee:")
    for assignee, count in report["by_assignee"].items():
        print(f"  {assignee}: {count}")

while True:
    print("\n==== CAMPUSFLOW ====")
    print("1. Create a ticket")
    print("2. View all tickets")
    print("3. Update ticket status")
    print("4. Assign ticket")
    print("5. Search ticket by ID")
    print("6. Search tickets by title")
    print("7. Filter tickets")
    print("8. View ticket report")
    print("9. Exit")

    choice = input("Please choose an option: ").strip()

    if choice == "1":
        create_new_ticket()

    elif choice == "2":
        view_tickets(tickets)

    elif choice == "3":
        update_ticket_status(tickets)

    elif choice == "4":
        assign_ticket(tickets)

    elif choice == "5":
        search_ticket(tickets)

    elif choice == "6":
        search_tickets_by_title(tickets)

    elif choice == "7":
        filter_tickets_menu(tickets)

    elif choice == "8":
        view_ticket_report(tickets)

    elif choice == "9":
        print("Thank you for using CampusFlow!")
        break

    else:
        print("Invalid choice. Please select an option from 1 to 9.")
