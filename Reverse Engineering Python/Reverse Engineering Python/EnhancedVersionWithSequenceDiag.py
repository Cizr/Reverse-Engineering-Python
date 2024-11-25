import ast
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PyToUML:
    """Class to convert Python source code to UML diagrams."""

    def __init__(self, input_file: str, output_file: str) -> None:
        """
        Initializes the PyToUML object with input and output file paths.

        :param input_file: Path to the Python source file.
        :param output_file: Path to the output file where UML will be saved.
        """
        #for classes/sequences (the list is to store information since DICT contains details like name,att's and methods
        #[] to start as empty, for sequence(method name and interactions)
        self.input_file = input_file
        self.output_file = output_file
        self.classes: List[Dict[str, Optional[List[str]]]] = []
        self.sequence_diagrams: List[Dict[str, str]] = []

    def extract_classes(self) -> None:
        """
        Extracts class definitions, including attributes and methods, from the Python source file.
        """
        try:
            with open(self.input_file, 'r') as file:
                tree = ast.parse(file.read()) #open and ast it
        except FileNotFoundError:
            logging.error(f"File not found: {self.input_file}")
            return
        except Exception as e:
            logging.error(f"Error parsing file {self.input_file}: {e}")
            return

        for node in ast.walk(tree): #inspection of every class,func and statement (Iterates thru nodes)
            if isinstance(node, ast.ClassDef): #ast.classdef (if current node is class)
                class_info = {
                    'name': node.name,
                    'attributes': [],
                    'methods': [],
                    'parent': []
                }
                            #store details about class

                class_info['parent'] = [base.id for base in node.bases if isinstance(base, ast.Name)]
                #parent classes in inheritance (ast.name simple id)


                for class_node in node.body: #over methods'atts of class
                    if isinstance(class_node, ast.FunctionDef):
                        if class_node.name == '__init__':
                            class_info['attributes'] = [item.arg for item in class_node.args.args[1:]]  # Skip self
                        class_info['methods'].append(class_node.name)
                    elif isinstance(class_node, ast.Assign): #check self att= value
                        for target in class_node.targets:
                            if isinstance(target, ast.Attribute):
                                class_info['attributes'].append(target.attr)

                self.classes.append(class_info)

                            #Parses the Python file into an AST.
                            #Identifies classes and extracts their details:
                            #Attributes (via __init__ or assignments).
                            #Methods.
                            #Parent Classes (inheritance)

    def extract_sequence_diagrams(self) -> None:
        """
        Extracts method interactions for sequence diagrams.
        """
        try:
            with open(self.input_file, 'r') as file:
                tree = ast.parse(file.read())
        except Exception as e:
            logging.error(f"Error parsing file for sequence diagrams: {e}")
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                interactions = []
                for stmt in node.body:
                    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                        if isinstance(stmt.value.func, ast.Attribute) and isinstance(stmt.value.func.value, ast.Name):
                            #extract caller & callee
                            caller = stmt.value.func.value.id
                            callee = stmt.value.func.attr
                            interactions.append((caller, callee))
                            #store interactions for methods that have calls
                if interactions:
                    self.sequence_diagrams.append({'method': node.name, 'interactions': interactions})

    def generate_class_uml(self) -> str:
        """
        Generates a UML class diagram from the extracted class information.

        :return: The PlantUML formatted string for the class diagram.
        """
        uml = "@startuml\n"
        #itterate thru classes created
        for class_info in self.classes:
            uml += f"class {class_info['name']} {{\n"
            #add class att's
            for attribute in class_info['attributes']:
                uml += f"  - {attribute}\n"
                
            for method in class_info['methods']:
                uml += f"  + {method}()\n"
            
            uml += "}\n"
            
            for parent in class_info['parent']:
                uml += f"{parent} <|-- {class_info['name']}\n"
        
        uml += "@enduml\n"
        return uml

    def generate_sequence_uml(self) -> str:
        """
        Generates UML sequence diagrams based on the extracted method interactions.

        :return: The PlantUML formatted string for the sequence diagram.
        """
        uml = "@startuml\n"
            #thru collected method interraction
        for seq in self.sequence_diagrams:
            uml += f"activate {seq['method']}\n"
            #representation of call (from caller/calee)!
            for caller, callee in seq['interactions']:
                uml += f"{caller} -> {callee}: call\n"
            uml += f"deactivate {seq['method']}\n" #signals that the object or method has completed its action
        
        uml += "@enduml\n"
        return uml

    def save_uml(self, uml: str, filename: str) -> None:
        """
        Saves the generated UML string to the specified file.

        :param uml: The UML string to save.
        :param filename: The filename to save the UML to.
        """
        try:
            with open(filename, 'w') as file:
                file.write(uml)
            logging.info(f"UML diagram saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving UML to {filename}: {e}")

    def run(self) -> None:
        """
        Runs the menu-driven interface to generate and save UML diagrams.
        """
        while True:
            print("\n--- UML Diagram Generator ---")
            print("1. Generate Class Diagram")
            print("2. Generate Sequence Diagram")
            print("3. Generate Both")
            print("4. Exit")
            
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                self.extract_classes()
                if not self.classes:
                    logging.warning("No classes found in the source file.")
                    continue
                class_uml = self.generate_class_uml()
                self.save_uml(class_uml, self.output_file)
            
            elif choice == '2':
                self.extract_sequence_diagrams()
                if not self.sequence_diagrams:
                    logging.warning("No sequence interactions found in the source file.")
                    continue
                sequence_uml = self.generate_sequence_uml()
                sequence_output_file = self.output_file.replace(".txt", "_sequence.txt")
                self.save_uml(sequence_uml, sequence_output_file)
            
            elif choice == '3':
                self.extract_classes()
                self.extract_sequence_diagrams()

                if self.classes:
                    class_uml = self.generate_class_uml()
                    self.save_uml(class_uml, self.output_file)
                else:
                    logging.warning("No classes found to generate a class diagram.")

                if self.sequence_diagrams:
                    sequence_uml = self.generate_sequence_uml()
                    sequence_output_file = self.output_file.replace(".txt", "_sequence.txt")
                    self.save_uml(sequence_uml, sequence_output_file)
                else:
                    logging.warning("No sequence interactions found to generate a sequence diagram.")
            
            elif choice == '4':
                logging.info("Exiting the UML Diagram Generator.")
                break
            
            else:
                logging.warning("Invalid choice. Please try again.")


input_file = "test2.py"
output_file = "class_diagram.txt"


uml_generator = PyToUML(input_file, output_file)
uml_generator.run()
