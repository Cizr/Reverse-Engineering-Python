import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_uml_diagram(input_file: str) -> None:
    """
    Generates a UML class diagram from the specified Python file using pyreverse.

    Parameters:
        input_file (str): The path to the Python file for which the UML diagram will be generated.
    """


    if not os.path.isfile(input_file):
        logging.error(f"The file {input_file} does not exist.")
        return

    output_dir = "uml_output" #UML diagram will be stored
    os.makedirs(output_dir, exist_ok=True)

    pyreverse_path = "C:/Users/dadyk/AppData/Roaming/Python/Python312/Scripts/pyreverse.exe"

    try:
        subprocess.run([
            pyreverse_path, #executable file for pyreverse
            '--output=png',
            '--project=MyProject',
            '--output-dir', output_dir,
            input_file
        ], check=True) #ensures that if the pyreverse command fails it raises a subprocess.CalledProcessError

                #(e)=exception object, holds information like the error message type and sometimes a traceback
        logging.info(f"The UML diagram has been generated in the {output_dir} directory.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error generating the UML diagram: {e}")
    except Exception as e:
        logging.exception("An unexpected error occurred.")

if __name__ == "__main__":
    input_file = "testing.py"
    generate_uml_diagram(input_file)
