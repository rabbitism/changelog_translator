import json

def load_configs():
    with open('configurations/configurations.json') as f:
        content = f.read()
        configs = json.loads(content)
        #print(versions) 
        f.close()
    return configs

if __name__ == "__main__":
    configs = load_configs()
    print(configs)