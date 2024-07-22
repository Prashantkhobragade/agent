from crewai_tools import tool
import json

@tool("output_json")
def output_json(data):
    
    """This function takes any data and attempts to convert it to JSON format using json.dumps. 
    If the data cannot be serialized, it catches the TypeError and returns an error message."""
    
    print(data)
    try:
        json_data = json.dumps(data, indent=4)
        return json_data
    except TypeError as e:
        return f"Error: {e}"