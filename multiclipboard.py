import sys
import clipboard
import json
import os


def main():
    clipboard_controller = ClipboardController("clipboard.json")
    if len(sys.argv) >= 2:
        if not clipboard_controller.check_file():
            clipboard_controller.create_file()
        clipboard_controller.input_convert(sys.argv[1:])
    else:
        print("No command entered")


class ClipboardController:

    def __init__(self, filepath):
        self.filepath = filepath
        if not self.check_file():
            self.create_file()
        self.data = self.load_json()

    def input_convert(self, arguments):
        para = arguments[0]
        if para == "save":
            self.save()
        elif para == "load":
            self.load()
        elif para == "list":
            self.list_elements()
        elif para == "remove":
            self.remove()
        else:
            print("Unknown command")

    def check_file(self):
        return os.path.isfile(self.filepath)

    def create_file(self):
        with open(self.filepath, "x") as file:
            json.dump({}, file)

    def save_element(self):
        with open(self.filepath, "w") as file:
            json.dump(self.data, file)

    def replace_element(self, key):
        print("Key existed (" + self.data[key] + ")")
        print("Do you want to replace it? (Y/N)")
        replace_response = input("> ")
        if replace_response == "Y":
            self.data[key] = clipboard.paste()
            self.save_element()
            print("Data replaced in clipboard")
        elif replace_response == "N":
            print("Decline replacement")
        else:
            print("Invalid response")

    def load_json(self):
        with open(self.filepath, "r") as file:
            data = json.load(file)
            return data

    def save(self):
        key = input("Enter your key \n > ")
        if key in self.data:
            self.replace_element(key)
        else:
            self.data[key] = clipboard.paste()
            self.save_element()
            print("Data saved in clipboard")

    def load(self):
        key = input("Enter your key \n > ")
        if key in self.data:
            clipboard.copy(self.data[key])
            print("Data copied in clipboard")
        else:
            print("Key doesn't exist.")

    def remove(self):
        remove_element = input("Enter your key \n > ")
        found = False
        for x, key in enumerate(self.data):
            if key == remove_element:
                self.data.pop(key)
                found = True
        if found:
            self.save_element()
            print("Data removed from clipboard")
        else:
            print("Key doesn't exist")

    def list_elements(self):
        print("=============================================")
        for key in self.data:
            print("Key: " + key + " || Data: " + self.data[key])
        print("=============================================")


main()
