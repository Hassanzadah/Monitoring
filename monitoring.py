import socket
import sys
import argparse
import time
import psutil
from alarm import Alarm


def get_disk_space():
    return psutil.disk_usage('/').percent


def get_number_of_processes():
    return len(psutil.pids())


def main(args):
    metric = args.function
    soft_limit = args.softLimit
    hard_limit = args.hardLimit
    message_text = args.messageText
    interval = args.interval
    iterations = args.iterations
    use_interval = args.useInterval
    log_file_path = args.logFile

    alarm = Alarm(soft_limit, hard_limit, message_text, log_file_path)

    counter = 0

    while not use_interval or (iterations is None or counter < iterations):
        if metric == "disk_space":
            current_value = get_disk_space()
        elif metric == "processes":
            current_value = get_number_of_processes()
        else:
            print("Invalid metric.")
            sys.exit(1)

        network_name = socket.gethostname()
        alarm.check_value(current_value, network_name)

        if use_interval:
            time.sleep(interval)
            counter += 1
        else:
            break


def parse_arguments():
    parser = argparse.ArgumentParser(description="Monitoring script")
    parser.add_argument("--function", choices=["disk_space", "processes"], required=True,
                        help="Function to monitor")
    parser.add_argument("--softLimit", type=int, required=True, help="Soft limit for the selected function")
    parser.add_argument("--hardLimit", type=int, required=True, help="Hard limit for the selected function")
    parser.add_argument("--messageText", type=str, required=True, help="Message text for the alarm")
    parser.add_argument("--interval", type=int, default=60, help="Interval between checks in seconds")
    parser.add_argument("--iterations", type=int, default=None, help="Number of iterations to run before stopping ("
                                                                     "None for infinite)")
    parser.add_argument("--useInterval", action="store_true", help="Use script interval instead of Task Scheduler "
                                                                   "interval")
    parser.add_argument("--logFile", type=str, default=None, help="Path to the log file")

    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_arguments()
    #arguments.function = "disk_space"
    #arguments.softLimit = 30
    #arguments.hardLimit = 30
    #arguments.messageText = "Test"
    main(arguments)
