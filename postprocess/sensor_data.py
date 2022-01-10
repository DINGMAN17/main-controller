import csv


class DataPostprocess:
    def __init__(self, log_filename=None):
        self.log_filename = log_filename if log_filename is not None else "../server.log"
        self.angle_csv = "angle_data.csv"
        self.load_csv = "load_data.csv"

    def process_angle(self, time=True):
        angle_list = self.extract_time() if time else []
        count = 0
        with open(self.log_filename, 'r') as f:
            for line in f:
                if "LD1" in line:
                    angle_record = line.strip().split("-")[-1].split(",")[1:]
                    if time:
                        angle_list[count].extend(angle_record)
                        count += 1
                    else:
                        angle_list.append(angle_record)

        angle_header = ["time", "roll", "pitch"] if time else ["roll", "pitch"]
        DataPostprocess.write_csv(angle_list, angle_header, self.angle_csv)

    def process_load(self, time=True):
        load_list = self.extract_time() if time else []
        count = 0
        with open(self.log_filename, 'r') as f:
            for line in f:
                load_record = None
                if line.startswith("LD2"):
                    load_record = line.strip().split(",")[1:]
                elif "LD2" in line:
                    load_record = line.strip().split("-")[-1].split(",")[1:]
                if load_record is not None:
                    if time:
                        load_list[count].extend(load_record)
                        count += 1
                    else:
                        load_list.append(load_record)

        load_header = ["time", "load1", "load2", "load3", "load4"] if time else ["load1", "load2", "load3", "load4"]
        DataPostprocess.write_csv(load_list, load_header, self.load_csv)

    def extract_time(self):
        data_list = []
        with open(self.log_filename, 'r') as f:
            for line in f:
                if "INFO" in line:
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
    data = DataPostprocess()
    data.process_angle()
