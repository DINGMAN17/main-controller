import csv


class DataPostprocess:
    def __init__(self, log_filename):
        self.log_filename = log_filename
        self.angle_csv = "angle_data.csv"
        self.load_csv = "load_data.csv"

    def process_data(self, time=True, angle=True, pattern="L-D-1"):
        data_list = self.extract_time() if time else []
        count = 0
        if angle:
            pattern = pattern
            header = ["time", "roll", "pitch"] if time else ["roll", "pitch"]
        else:
            pattern = pattern
            header = ["time", "load1", "load2", "load3", "load4"] if time else ["load1", "load2", "load3", "load4"]

        with open(self.log_filename, 'r') as f:
            for line in f:
                idx = line.find(pattern)
                if idx != -1:
                    angle_record = line[idx:].split(",")[1:]
                    angle_record = [float(num) for num in angle_record]
                    if time:
                        data_list[count].extend(angle_record)
                        count += 1
                    else:
                        data_list.append(angle_record)
        if angle:
            DataPostprocess.write_csv(data_list, header, self.angle_csv)
        else:
            DataPostprocess.write_csv(data_list, header, self.load_csv)

    def extract_time(self):
        data_list = []
        with open(self.log_filename, 'r') as f:
            for line in f:
                if "L-D-1" in line:
                    time_str = line.split(" - ")[0].split(" ")[-1]
                    data_list.append([time_str])
        return data_list

    @staticmethod
    def write_csv(data_list, header, csv_filename=None):
        with open(csv_filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data_list)


if __name__ == "__main__":
    filename = "/Users/manding/work/LiftingFrame/software/mainController/log/server_2022_01_20-12_09_29_PM.log"
    data = DataPostprocess(filename)
    data.process_data(angle=True, pattern="L-D-3")
