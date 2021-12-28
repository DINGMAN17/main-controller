from control.initialisation import Initialisation


class CommandInvoker:
    def execute(self, message, command_queue):
        if "initialisation" in message:
            output = self.run_initialisation()
            command_queue.put(output)
        elif "check" in message:
            output_list = self.run_system_check()
            [command_queue.put(message) for message in output_list]
        elif "levelonce" in message:
            output = self.run_levelling()
            command_queue.put(output)
        elif "continue" in message:
            output = self.run_levelling_continue()
            command_queue.put(output)
        elif "stop" in message:
            output = self.run_Estop()
            command_queue.put(output)

    def run_initialisation(self, ppvc_type="1ton_prototype", pulley_num=6):
        ppvc_init = Initialisation(ppvc_type, pulley_num)
        return ppvc_init.run()

    def run_Estop(self):
        return "cmd01t\n"

    def run_levelling(self):
        message = "cmd01L\n"
        return message

    def run_levelling_continue(self):
        message = "continue\n"
        return message

    def run_system_check(self):
        output_list = []
        return output_list
