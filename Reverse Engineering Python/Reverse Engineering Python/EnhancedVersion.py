import ast
from typing import List, Dict, Optional

class PyToUML:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file
        self.classes: List[Dict[str, Optional[List[str]]]] = []

    def extract_classes(self) -> None:
        """Extracts classes and their members (attributes, methods) from the Python file."""
        try:
            with open(self.input_file, 'r') as file:
                tree = ast.parse(file.read())
        except FileNotFoundError:
            print(f"Error: The file {self.input_file} was not found.")
            return
        except Exception as e:
            print(f"Error while parsing the file: {e}")
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'attributes': [],
                    'methods': [],
                    'parent': []
                }

                # Find the base class(es) if they exist
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        class_info['parent'].append(base.id)

                # Loop through the class body to get attributes and methods
                for class_node in node.body:
                    if isinstance(class_node, ast.FunctionDef):
                        if class_node.name == '__init__':
                            # Extract attributes from __init__
                            for item in class_node.args.args[1:]:  # Skip 'self'
                                class_info['attributes'].append(item.arg)
                        class_info['methods'].append(class_node.name)
                    elif isinstance(class_node, ast.Assign):
                        for target in class_node.targets:
                            if isinstance(target, ast.Attribute):
                                class_info['attributes'].append(target.attr)

                self.classes.append(class_info)

    def generate_uml(self) -> str:
        """Generates the PlantUML class diagram."""
        uml = "@startuml\n"
        
        for class_info in self.classes:
            uml += f"class {class_info['name']} {{\n"
            
            # Add attributes
            for attribute in class_info['attributes']:
                uml += f"  - {attribute}\n"
            
            # Add methods
            for method in class_info['methods']:
                uml += f"  + {method}()\n"
            
            uml += "}\n"
            
            # Add inheritance if applicable
            for parent in class_info['parent']:
                uml += f"{parent} <|-- {class_info['name']}\n"
        
        uml += "@enduml\n"
        return uml

    def save_uml(self, uml: str) -> None:
        """Saves the generated UML to the output file."""
        try:
            with open(self.output_file, 'w') as file:
                file.write(uml)
        except Exception as e:
            print(f"Error while saving UML to {self.output_file}: {e}")

    def run(self) -> None:
        """Runs the process of extracting classes and generating UML."""
        self.extract_classes()
        if not self.classes:
            print("No classes were extracted. Exiting.")
            return
        uml = self.generate_uml()
        self.save_uml(uml)


# Configuration
input_file = "testing.py"  # Python source file (change this as needed)
output_file = "class_diagram.txt"  # Output PlantUML file

# Run the script
uml_generator = PyToUML(input_file, output_file)
uml_generator.run()
