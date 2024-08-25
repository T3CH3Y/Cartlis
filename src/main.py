import os
import yaml
from agents import APICrew

api_key = os.environ['OPENAI_API_KEY']
model_name = os.environ['OPENAI_MODEL_NAME']
api_base = os.environ['OPENAI_API_BASE']

print(model_name)


def load_yaml_files(folder_path):
    raw_data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".yaml"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                raw_data[filename] = yaml.safe_load(file)
    return raw_data

def convert_yaml_to_text(raw_data):
    text_data = {}
    for filename, yaml_content in raw_data.items():
        try:
            # Convert YAML content to a text string
            yaml_text = yaml.dump(yaml_content, default_flow_style=False)
            text_data[filename] = yaml_text
        except Exception as e:
            print(f"Error converting {filename}: {e}")
            text_data[filename] = None
    return text_data

def load_text_files(folder_path):
    text_data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r') as file:
                    text_data[filename] = file.read()
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                text_data[filename] = None
    return text_data

if __name__ == "__main__":
    folder_path = "data_sources"
    raw_yaml_data = load_yaml_files(folder_path)
    yaml_data = convert_yaml_to_text(raw_yaml_data)
    text_data = load_text_files(folder_path)
    
    api_spec = yaml_data["apispec.yaml"]
    rules = yaml_data["rules.yaml"]
    industry = text_data["industry.txt"]
    violations = text_data["violations.txt"]

    
    
    api_crew = APICrew(api_spec=api_spec, industry=industry, rules=rules, violations=violations)
    api_crew.crew_kickoff()