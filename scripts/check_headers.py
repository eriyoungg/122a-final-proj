import os
import csv

folder = "test_data_project_122a" 

files_to_check = ["User.csv",
                "AgentCreator.csv",         
                "AgentClient.csv",          
                "InternetService.csv",      
                "BaseModel.csv",            
                "LLMService.csv",           
                "DataStorage.csv",          
                "CustomizedModel.csv",      
                "Configuration.csv",        
                "ModelServices.csv",        
                "ModelConfigurations.csv"
                ]
for filename in files_to_check:
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            print(f"{filename}: {headers}")
    else:
        print(f"Could not find {filename}")