import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime


def parse_arguments():
    parser = argparse.ArgumentParser(description="Visualize monitoring data")
    parser.add_argument("--logFile", type=str, required=False, help="Path to the log file")
    return parser.parse_args()


def read_log_file(log_file):
    timestamps = []
    values = []

    with open(log_file, "r") as file:
        for line in file.readlines():
            parts = line.strip().split(", ")
            if len(parts) == 4:
                timestamp, _, _, value = parts
                dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                timestamps.append(dt)
                values.append(float(value))

    return timestamps, values


def plot_data(timestamps, values):
    fig, ax = plt.subplots()
    ax.plot(timestamps, values, marker="o")

    # Format the x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
    plt.xticks(rotation=45)

    plt.xlabel("Timestamp")
    plt.ylabel("Value")
    plt.title("Monitoring Data Visualization")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    args = parse_arguments()
    #log_file = args.logFile
    log_file = r"C:\Users\guemu\PycharmProjects\pythonProject\alarm_log.txt"

    timestamps, values = read_log_file(log_file)
    plot_data(timestamps, values)
