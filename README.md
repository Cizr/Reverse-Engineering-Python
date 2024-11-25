![Black Simple Business Youtube Banner (3)](https://github.com/user-attachments/assets/782ea6ce-7cc2-44ec-b6a0-ed3007cda702)

# Reverse Engineering Python  

This repository provides scripts for analyzing and visualizing Python code through UML diagrams and code metrics. It is designed to aid in reverse engineering efforts by offering insights into code structure and maintainability.  

---

## Files and Features  

### 1. **`pyreverseUML.py`**  
**Purpose**: Generates a UML class diagram using `pyreverse`.  

- **How it works**:  
  - Utilizes the `pyreverse` tool to analyze a Python file and produce class diagrams in PNG format.  
  - Outputs are saved in a specified directory for easy access.  
  - Example: Analyzes relationships between classes and methods to visualize the code's structure.  

- **Key Benefits**:  
  - Quick and efficient generation of class diagrams.  
  - Ideal for understanding code relationships in a project.  

---

### 2. **`plantUML(EnhancedVersionWithSequence).py`**  
**Purpose**: Creates both class and sequence diagrams using `PlantUML`.  

- **How it works**:  
  - Transforms Python code into `PlantUML` format for visualization.  
  - Users can generate class diagrams to understand structure and sequence diagrams to map the flow of interactions.  
  - Requires `PlantUML`installed on the system.  

- **Key Benefits**:  
  - Offers additional sequence diagrams for a deeper analysis of program flow.  
  - Flexible and supports custom UML needs.  

---

### 3. **`code_metrics.py`**  
**Purpose**: Calculates cyclomatic complexity, maintainability index, and other metrics.  

- **How it works**:  
  - Analyzes a Python file to compute:  
    - **Lines of Code (LOC)**: Total lines in the file.  
    - **Cyclomatic Complexity**: Measures code complexity for readability and maintainability.  
    - **Maintainability Index (MI)**: Indicates how easy the code is to maintain.  
    - **Halstead Metrics**: Analyzes operations and operands in the code.  
  - Saves results in a JSON file for review.  

- **Key Benefits**:  
  - Helps in assessing the quality and maintainability of code.  
  - Useful for identifying areas that may need refactoring.  

---

## Setup and Requirements  

1. **Python Dependencies**:  
   Install required Python packages using `pip`:  
   ```bash  
   pip install pylint plantuml radon  
