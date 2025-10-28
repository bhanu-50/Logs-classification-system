import os
from processor_regex import classify_with_regex
from processor_bert import classify_with_bert
from processor_llm import classify_with_llm

def classify(logs):
    labels = []
    for source, log_msg in logs:
        label = classify_log(source,log_msg)
        labels.append(label)
    return labels

def classify_log(source,log_msg):
    if source == 'LegacyCRM':
        label = classify_with_llm(log_msg)
    else:
        label = classify_with_regex(log_msg)
        if not label:
            label = classify_with_bert(log_msg)
    return label

def classify_csv(input_file):
    import pandas as pd
    
    # Get the script's directory to make paths relative to it
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Handle both Unix-style and Windows-style paths
    input_file = input_file.replace('/', os.path.sep)
    
    # Construct absolute paths
    input_path = os.path.join(script_dir, input_file)
    
    # Read CSV with more flexible parsing
    df = pd.read_csv(input_path, skipinitialspace=True)
    
    # Clean up source and message columns
    df['source'] = df['source'].str.strip()
    df['log_message'] = df['log_message'].str.strip().str.strip('"')
    
    # Perform classification
    df["target_label"] = classify(list(zip(df["source"], df["log_message"])))

    # Save the modified file
    output_file = os.path.join(script_dir, "Resorces", "output.csv")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure output dir exists
    df.to_csv(output_file, index=False)
    
    return output_file

if __name__ == '__main__':
    classify_csv("Resorces/input.csv")