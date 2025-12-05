# CS122A Final Project: Agent Platform CLI

This project implements a command-line program that interacts with a MySQL database to manage the Agent Platform.  
All data is stored in MySQL, and all functionality is triggered through:

`python3 project.py <function name> [param1] [param2] ...`

The program parses CLI arguments, translates them into SQL queries, executes them on the database, and prints the results.

---

## Setup

### 1. Install MySQL Server
Install MySQL and ensure you can log in and run queries locally.

### 2. Install required Python dependencies
`python3 -m pip install mysql-connector-python`

### 3. Configure Database Credentials
Inside `functions.py`, update `DB_CONFIG` to match your MySQL setup:

`DB_CONFIG = {
"host": "localhost",
"user": "root",
"password": "yourpassword",
"database": "myagents"
}`

## Project Structure

**project.py:** Main CLI script\
**functions.py:** SQL logic for each function\
**test_data_project_122a:** Example folder containing CSV files for import\
**README.md:** This file

## Test Database Tables and Variables:

- User.csv: ['uid', 'email', 'username']
- AgentCreator.csv: ['uid', 'bio', 'payout']
- AgentClient.csv: ['uid', 'interests', 'cardholder', 'expire', 'cardno', 'cvv', 'zip']
- InternetService.csv: ['sid', 'provider', 'endpoints']
- BaseModel.csv: ['bmid', 'creator_uid', 'description']
- LLMService.csv: ['sid', 'domain']
- DataStorage.csv: ['sid', 'type']
- CustomizedModel.csv: ['bmid', 'mid']
- Configuration.csv: ['cid', 'client_uid', 'content', 'labels']
- ModelServices.csv: ['bmid', 'sid', 'version']
- ModelConfigurations.csv: ['bmid', 'mid', 'cid', 'duration']


## Run Program

- Every command must be run separately.  
- Each execution performs **one** operation and then exits.

General format:
`python3 project.py <function> [parameters...]`

Example:
`python3 project.py listInternetService 30`

## `import`

This is the **only** function that clears the database and reloads all data.

### Import data from a CSV folder
`python3 project.py import <folderName>`

Example:
`python3 project.py import test_data`

This will:
- Drop existing tables  
- Recreate tables using the schema  
- Load all CSV files in the folder  
- Insert the records into MySQL  

## Function Commands

### 1. Import Dataset
`python3 project.py import <folderName>`

Resets the database and loads all CSV files.

### 2. Insert Agent Client
`python3 project.py insertAgentClient uid username email card_number card_holder expiration_date cvv zip interests`

Adds a new agent client across the relevant tables.  
Outputs **Success** or **Fail**.

### 3. Add Customized Model
`python3 project.py addCustomizedModel mid bmid`

Adds a customized model built on a base model.


### 4. Delete Base Model
`python3 project.py deleteBaseModel bmid`

Deletes a base model.

### 5. List Internet Services
`python3 project.py listInternetService bmid`

Lists all internet services used by the specified base model.  
Output is a table:
`sid,endpoint,provider`

### 6. Count Customized Models
`python3 project.py countCustomizedModel bmid`

Outputs:
`bmid,description,customizedModelCount`

### 7. Top-N Longest Duration Configurations
`python3 project.py topNDurationConfig uid N`

Lists the top N configurations with the longest duration:
`uid,cid,label,content,duration`

### 8. Keyword Search on LLM Services
`python3 project.py listBaseModelKeyWord keyword`

Lists up to 5 base models whose LLM service domain contains the keyword.

### 9. Print NL2SQL Results
`python3 project.py printNL2SQLresult`

Reads your NL2SQL experiment CSV and prints the table: `NLquery_id,NLquery,LLM_model_name,prompt,LLM_returned_SQL_id,LLM_returned_SQL_query,SQL_correct,...`

## Output

- Boolean results → `Success` or `Fail`
- Tables → each row printed on its own line  
- Columns separated by commas (`,`), same as the CSV format

## Notes

- The database **persists** between runs.  
- Only the `import` command resets the database.  
- All other functions read or modify existing database contents.  
- Assume input format is ALWAYS correct.  
- Strings with spaces must be wrapped in quotes: "finance;data analysis"