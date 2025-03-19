import click
import json
import os

TODO_FILE = "todo.json"


def load_task():
    """Load tasks from todo.json, or create an empty list if file is missing/corrupt."""
    if not os.path.exists(TODO_FILE):
        return []

    try:
        with open(TODO_FILE, "r") as file:
            return json.load(file)  
    except json.JSONDecodeError:
        return []  


def save_tasks(tasks):
    """Save updated tasks to todo.json"""
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


@click.group()
def cli():
    """Simple Todo List Manager"""
    pass


@click.command()
@click.argument("task")
def add(task):
    """Add a new Task to the List"""
    tasks = load_task()  # Load existing tasks
    tasks.append({"task": task, "done": False})  # Append new task
    save_tasks(tasks)  # Save updated list
    click.echo(f"Task Added Successfully: {task}")


@click.command(name="list")
def list_tasks():
    """List all the Tasks"""
    tasks = load_task()
    if not tasks:
        click.echo("No tasks found!")
        return
    for index, task in enumerate(tasks, 1):  
        status = "✅" if task["done"] else "❌"
        click.echo(f"{index}. {task['task']} [{status}]")

@click.command()
@click.argument("task_number" , type=int)
def complete(task_number):
    """mark a task as Complete"""
    tasks = load_task()
    if 0 < task_number <= len(tasks):
        tasks[task_number -1]["done"]=True
        save_tasks(tasks)
        click.echo(f"Task {task_number} marked as Complete!")
    else:
        click.echo(f"Invalid task number: {task_number}")

@click.command()
@click.argument("task_number" , type=int)
def remove(task_number):
    """Remove task from Number"""
    tasks = load_task()
    if 0 < task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        click.echo(f"Removed Task: {removed_task}")
    else:
        click.echo(f"Invalid Task Number")

# Register Commands
cli.add_command(add)
cli.add_command(list_tasks) 
cli.add_command(complete) 
cli.add_command(remove)

if __name__ == "__main__":
    cli()
