import io
import sys
import json

# Function to capture printed outputs and return them as JSON
def capture_output_as_json(function_to_run, *args, **kwargs):
    # Create an in-memory file-like object
    output_capture = io.StringIO()
    
    # Save the current stdout
    original_stdout = sys.stdout
    
    try:
        # Redirect stdout to the in-memory file
        sys.stdout = output_capture
        
        # Run the function
        function_to_run(*args, **kwargs)
    finally:
        # Reset stdout back to original
        sys.stdout = original_stdout
    
    # Get the captured output
    captured_output = output_capture.getvalue()
    
    # Convert captured output to JSON (if structured appropriately)
    try:
        output_as_json = json.loads(captured_output)
    except json.JSONDecodeError:
        raise ValueError("Captured output is not valid JSON")
    
    return output_as_json

# Example function that prints JSON
def example_function():
    print('{"key": "value", "number": 42}')

# Capture the output and convert it to JSON
captured_json = capture_output_as_json(example_function)

print("Captured JSON:", captured_json)
