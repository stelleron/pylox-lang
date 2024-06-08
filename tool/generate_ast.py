import sys

def define_visitor(file, base_name, types):
    file.write("class " + base_name + "Visitor(ABC):\n")
    for type in types:
        file.write("\t@abstractmethod\n")
        file.write("\tdef visit" + type + "(self, obj):\n")
        file.write("\t\tpass\n\n")

def define_type(file, base_name, class_name, fields):
    file.write("class " + class_name + "(" + base_name + "):\n")
    file.write("\tdef __init__(self, " + ",".join(fields) + "):\n")
    for field in fields:
        file.write("\t\tself." + field.strip() + " = " + field.strip() + "\n")
    
    file.write("\n")
    file.write("\tdef accept(self, visitor):\n")
    file.write("\t\treturn visitor.visit" + class_name + "(self)\n\n")
    file.write("\n")

def define_ast(output_dir, base_name, types):
    f = open(output_dir + "/" + base_name.lower() + ".py", "w")
    f.write("from abc import ABC, abstractmethod\n\n")
    f.write("class " + base_name + "(ABC):\n")
    f.write("\t@abstractmethod\n")
    f.write("\tdef accept(self, visitor):\n")
    f.write("\t\tpass\n\n")

    cnames = []
    for type in types:
        cnames.append(type.split(":")[0].strip())
    define_visitor(f, base_name, cnames)

    for type in types:
        class_name = type.split(":")[0].strip()
        fields = type.split(":")[1].strip().split(",")
        define_type(f, base_name, class_name, fields)



if __name__ == "__main__":
    if not(len(sys.argv) == 2):
        print("Usage: generate_ast <output directory>")
        exit(64)
    define_ast(sys.argv[1], "Expr", [
        "Binary   : left, operator, right",
        "Grouping : expression",
        "Literal  : value",
        "Unary    : operator, right"
    ])