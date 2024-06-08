import sys
import scanner

class Lox():
    had_error = False

    def report(line, where, message):
        print("[line " + str(line) + "] Error" + where + ": " + message)
        Lox.had_error = True

    def error(line, message):
        Lox.report(line, "", message)

    def run(code):
        scan = scanner.Scanner(code)
        tokens = scan.scan_tokens()
        for token in tokens:
            print(token)

    def run_file(path):
        try:
            file = open(path, "r")
        except OSError:
            print("ERROR: Could not open file")
            sys.exit()
        
        source = file.read()
        file.close()
        Lox.run(source)
        
        if (Lox.had_error):
            exit(65)

    def run_prompt():
        while True:
            line = input("> ")
            if (line == ""):
                break;
            Lox.run(line)
            Lox.had_error = False

    def main():
        if len(sys.argv) > 2:
            print("Usage: plox [script]")
        elif len(sys.argv) == 2:
            Lox.run_file(sys.argv[0])
        else:
            Lox.run_prompt()


if __name__ == "__main__":  
    Lox.main()