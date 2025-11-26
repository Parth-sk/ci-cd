def add_task(task_list, task):
    task_list.append(task)
    return task_list

def remove_task(task_list, task):
    if task in task_list:
        task_list.remove(task)
    return task_list

if __name__ == "__main__":
    import sys
    task_list = []
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "add":
            print(add_task(task_list, sys.argv[2]))
        elif action == "remove":
            print(remove_task(task_list, sys.argv[2]))
