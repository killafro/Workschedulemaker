import csv
import itertools
import os
import random
import sys
from tabulate import tabulate


class NotEnoughWorkersError(Exception):
    pass


all_days = {
    "1": "Monday",
    "2": "Tuesday",
    "3": "Wednesday",
    "4": "Thursday",
    "5": "Friday",
    "6": "Saturday",
    "7": "Sunday",
}


def main():
    """Orchestrate the scheduling process based by provided shifts and worker information.

    This function serves as the main entry point for the scheduling script.
    It handles command line arguments, imports shifts data, collects worker
    information, and displays the resulting schedule.

    Usage:
        python script.py shifts_file.csv

    Command Line Arguments:
        shifts_file (str): The path to the CSV file containing shifts data.

    Steps:
        1. Import shifts data from the specified CSV file.
        2. Display a table with all shifts for visual reference.
        3. Ask the user for the minimum number of workers needed.
        4. Collect information about workers, including names and unavailable days.
        5. Check if there are enough workers based on the provided preferences.
        6. Clear the terminal for a clean display.
        7. Assign shifts to workers, considering their preferences.
        8. Display the resulting schedule.
        9. ask the user if the schedule needs to be saved to a file. To provide a file name. And then creates the file.
    """

    # Check if shifts file is in the command line
    if len(sys.argv) < 2:
        print("Usage: python script.py shifts_file.csv")
        sys.exit(1)

    # shifts_file is the file where the data about the shifts comes from
    shifts_file = sys.argv[1]

    # import shifts
    shifts = import_shifts(shifts_file)

    # create table with all shifts
    table_data = shifts_table(shifts)

    # ask the minimum amount of workers
    min_workers = total_workers()

    # ask what employees need to be added to the schedule
    employees = get_worker_information()

    # check if there are enough workers
    minimum_workers_check(len(employees), min_workers)

    # clear terminal
    os.system("clear")

    # print requested days
    show_requested_free_days(employees)

    # assign shifts
    assignments = complete_assignement(shifts, employees)


    # print table with shifts
    table_data = show_schedule(shifts, assignments)

    # asks the user if they want the table in a seperate file
    save_schedule_to_file(table_data)


def import_shifts(shifts_file):
    """Import the shifts from a CSV file into a list of dictionaries.

    Each dictionary represents a shift with keys 'shift', 'start', 'end', and 'days'.
    Values are stripped of excess spaces. If the file is not found, a FileNotFoundError is raised.
    If the CSV file is empty or lacks required headers, a ValueError is raised.
    If the file does not have a '.csv' extension, a ValueError is raised.

    Args:
        shifts_file (str): The path to the CSV file containing shift data.

    Returns:
        list: List of dictionaries representing shifts.

    Raises:
        FileNotFoundError: If the specified file is not found.
        ValueError: If the CSV file is empty, lacks required headers, or does not have a '.csv' extension.


    """

    shifts = []
    required_headers = ["shift", "start", "end", "days"]

    if not shifts_file.lower().endswith(".csv"):
        raise ValueError(
            f"Error: File '{shifts_file}' does not have a '.csv' extension."
        )

    try:
        with open(shifts_file, "r") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames:
                raise ValueError("Error: CSV file is empty.")

            # Check if the required headers are present
            if not all(header in reader.fieldnames for header in required_headers):
                raise ValueError(
                    f"Error: CSV file must have headers {required_headers}."
                )
            for row in reader:
                shifts.append(
                    {
                        "shift": row["shift"].strip(),
                        "start": row["start"].strip(),
                        "end": row["end"].strip(),
                        "days": row["days"].strip(),
                    }
                )
    except FileNotFoundError:
        print("Error: file '{shifts_file}' not found.")
        exit(1)
    return shifts


def shifts_table(shifts):
    """Generate a table displaying shifts with corresponding days.
    Args:
        shifts_data (list): List of dictionaries containing shift information.

    Returns:
        list: List of lists representing the table data.
    """

    headers = ["Shift", "Start", "End"] + list(all_days.values())
    table_data = []

    for shift in shifts:
        row = [shift["shift"], shift["start"], shift["end"]] + [""] * len(all_days)
        days = shift["days"].strip()

        # Mark the corresponding day with "+" to show what shifts need a worker
        # row + 3 because the first columns are the shift, start and end date

        for day_num in days:
            row[3 + int(day_num) - 1] = "+"
        table_data.append(row)

        # used to center the values of the table
        colalign = ["center"] * len(headers)

    print(tabulate(table_data, headers=headers, tablefmt="grid", colalign=colalign))
    return table_data


def total_workers():
    """Ask for the minimum number of workers needed for the schedule.

    This function prompts the user to input the minimum number of workers
    required for the schedule. It validates the input to ensure a positive
    integer is provided.

    Returns:
        int: The minimum number of workers needed for the schedule.
    """
    while True:
        try:
            min_workers = int(input("Whats the minimum amount of workers you need? "))
            if min_workers > 0:
                return min_workers
            else:
                print("Input invalid: please give a positive number!")
        except ValueError:
            print("Input invalid: Please input a positive integer!")


def get_worker_information():
    """Collect information about workers including names and unavailable days.

    This function prompts the user to enter names of workers and the days
    when they are unavailable to work. The information is stored in a list
    of dictionaries, where each dictionary represents a worker with their
    name and a list of unavailable days.

    Returns:
        list: List of dictionaries, where each dictionary contains:
            - 'name' (str): The name of the worker.
            - 'unavailable_days' (list): List of integers representing days
              when the worker is unavailable to work (1-7).
    """
    print("Keep typing names of workers. When you're done, press enter.")
    workers = []

    while True:
        worker_name = get_worker_name()
        if not worker_name:
            break

        unavailable_days = get_unavailable_days(worker_name)

        workers.append({"name": worker_name, "unavailable_days": unavailable_days})

    return workers


def get_worker_name():
    """asks user for a worker

    Returns:
    str: The name of the worker entered by the user.

    """
    return input("Worker: ").strip()


def get_unavailable_days(worker_name):
    """Prompt the user to enter days when a worker is unavailable to work.
    Args:
        worker_name (str): The name of the worker.

    Returns:
        list: List of integers representing days when the worker is unavailable to work (1-7).
    """
    while True:
        input_prompt = f"Enter days (1-7) when {worker_name} can't work (comma-separated): "
        user_input = input(input_prompt).strip()

        # Check if the user pressed enter without providing any input
        if not user_input:
            return ""

        unavailable_days_input = user_input.split(",")

        # Check if any day is invalid
        if all(is_valid_day(day) for day in unavailable_days_input):
            return [day.strip() for day in unavailable_days_input]
        else:
            print("Invalid input. Please enter valid days (1-7). Try again.")


def is_valid_day(day):
    """Check if the given day input is a valid day of the week (between 1 and 7).
    Args:
        day (str): The day input to be checked.
    Returns:
        bool: True if the input is a valid day, False otherwise.
    """
    return day.strip().isdigit() and 1 <= int(day.strip()) <= 7


def minimum_workers_check(employees, min_workers):
    """Check if there are enough workers based on the minimum required.

    Args:
        employees (int): The number of workers.
        min_workers (int): The minimum required number of workers.

    Raises:
        ValueError: If there are not enough workers.

    Returns:
        bool: True if there are enough workers, False otherwise.
    """
    if employees < int(min_workers):
        print("Not enough workers!")
        exit(1)
    return True


def complete_assignement(shifts, employees):
    """Complete the assignment of shifts to employees.

    This function attempts to assign shifts to employees based on their preferences.
    If there are not enough workers to cover all shifts, the user is prompted to
    generate a schedule without considering employee preferences.

    Args:
        shifts (list): A list of dictionaries representing shifts.
        employees (list): A list of dictionaries representing workers and their preferences.

    Returns:
        dict: A dictionary representing the assigned shifts.

    Raises:
        InsufficientWorkersError: If there are not enough workers, and the user chooses not to generate
            a schedule without considering employee preferences.
    """
    try:
        assignments = assign_schedule(shifts, employees)

    # Not enough workers to cover all shifts based on preferences
    except NotEnoughWorkersError:
        consider_preferences = (
            input(
                "It's not possible to accommodate everyone's preferences.\n"
                "Do you want to generate a schedule without considering employee preferences? (yes/no): "
            )
            .strip()
            .lower()
        )

        if consider_preferences == "yes":
            # Assign shifts without considering employee preferences
            assignments = assign_schedule_without_preferences(shifts, employees)
        else:
            os.system("clear")

            print(
                "Exiting the program. Please adjust preferences or provide more workers."
            )
            exit(1)
    return assignments


def assign_schedule(shifts, employees):
    """Assign shifts to employees based on their preferences.

     Args:
         shifts (list): A list of dictionaries representing shifts.
         employees (list): A list of dictionaries representing workers and their preferences.

     Returns:
         dict: A dictionary representing the assigned shifts.
     """

    assignments = {shift["shift"]: {day: [] for day in all_days.values()} for shift in shifts
                    }
    assigned_shifts_per_day = {employee["name"]: {day: None for day in all_days.values()}
          for employee in employees
          }
    employee_list = [
           employee
           for _ in range(len(shifts) * len(all_days))
           for employee in random.sample(employees, len(employees))
           ]

    for shift in shifts:
            for day_num in shift["days"]:
                day_name = all_days[day_num]

                # Check if the employee_list is empty
                if not employee_list:
                    print("Error: Not enough employees to cover all shifts.")
                    exit(1)

                # Get the employee from the list
                employee = employee_list.pop()

                # Check if the employee is already assigned on that day or can't work on that day
                while (
                    assigned_shifts_per_day[employee["name"]][day_name] is not None
                    or day_num in employee["unavailable_days"]
                ):
                    # Check if the employee_list is empty after the previous pop
                    if not employee_list:
                        raise NotEnoughWorkersError(
                            "Not enough workers to cover all shifts based on preferences."
                        )

                    # Get the next employee from the list
                    employee = employee_list.pop()

                # Assign the employee to the shift on that day
                assignments[shift["shift"]][day_name].append(employee["name"])
                assigned_shifts_per_day[employee["name"]][day_name] = shift["shift"]

    return assignments


def assign_schedule_without_preferences(shifts, employees):
    """Assign shifts to employees without considering their preferences.

    Args:
        shifts (list): List of dictionaries representing shifts.
        employees (list): List of dictionaries representing workers.

    Returns:
        dict: A dictionary representing the assigned shifts.
    """
    assignments = {
        shift["shift"]: {day: [] for day in all_days.values()} for shift in shifts
    }
    available_employees = [employee["name"] for employee in employees]

    # Shuffle the list of available employees
    random.shuffle(available_employees)

    # Use itertools.cycle to cycle through the shuffled list
    employee_cycle = itertools.cycle(available_employees)

    for shift in shifts:
        for day_num in shift["days"]:
            day_name = all_days[day_num]

            # Get the next employee from the cycled list
            employee = next(employee_cycle)

            # Assign the employee to the shift on that day
            assignments[shift["shift"]][day_name].append(employee)

    return assignments


def show_requested_free_days(workers):
    """Display the requested free days for each worker.

    Args:
        workers (list): List of dictionaries representing workers and their preferences.
    """
    print("\nRequested Free Days:")
    for worker in workers:
        worker_name = worker["name"]
        requested_days = worker["unavailable_days"]
        free_days = []

        for requested_day in requested_days:
            free_days.append(all_days[requested_day])


        if free_days:
            print(f"{worker_name}: {', '.join(free_days)}")
        else:
            print(f"{worker_name} has no requested free days.")


def show_schedule(shifts, assignments):
    """Display the schedule assignments in a tabular format.

    Args:
        shifts (list): List of dictionaries representing shifts.
        assignments (dict): A dictionary representing the assigned shifts.
    """
    headers = ["Shift"] + list(all_days.values())
    table_data = []

    for shift in shifts:
        row = [shift["shift"]] + [
            ", ".join(assignments[shift["shift"]][day]) for day in all_days.values()
        ]
        table_data.append(row)

    colalign = ["center"] * len(headers)

    print("\nSchedule Assignments:")
    print(tabulate(table_data, headers=headers, tablefmt="grid", colalign=colalign))
    return table_data


def save_schedule_to_file(table_data):
    """Asks the user if they want to Save the schedule to a file.

    Args:
        table_data (list): List of lists representing the schedule table.
        headers (list): List of header strings for the table.
    """

    save_to_file = input("Do you want to save the schedule to a file? (yes/no): ").strip().lower()
    headers = ["Shift"] + list(all_days.values())

    if save_to_file == 'yes':
        # Get the filename from the user
        filename = input("Enter the filename (include extension, e.g., schedule.txt): ").strip()

        #center the table
        colalign = ["center"] * len(headers)

        # Save the schedule to the specified file
        with open(filename, 'w') as file:
            file.write(tabulate(table_data, headers=headers, tablefmt="grid", colalign = colalign))

        print(f"Schedule saved to {filename}")


if __name__ == "__main__":
    main()
