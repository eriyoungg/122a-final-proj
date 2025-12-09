import sys
from functions import (
    import_data,
    insertAgentClient,
    addCustomizedModel,
    deleteBaseModel,
    listInternetService,
    countCustomizedModel,
    topNDurationConfig,
    listBaseModelKeyWord,
    printNL2SQLresult
)

def convert_params(params):
    result = []
    for p in params:
        if p == "NULL":
            result.append(None)
        else:
            result.append(p)
    return result 

def output(result):
    if isinstance(result, bool):
        if result:
            print("Success")
        else:
            print("Fail")
    elif isinstance(result, list):
        for row in result:
            print(",".join(str(x) for x in row))

def main():
    # Assume input will ALWAYS be in correct format
    args = sys.argv[1:]
    if len(args) == 0:
        return

    cmd = args[0]
    params = convert_params(args[1:])

    if cmd == "import":
        result = import_data(*params)

    elif cmd == "insertAgentClient":
        result = insertAgentClient(*params)

    elif cmd == "addCustomizedModel":
        result = addCustomizedModel(*params)

    elif cmd == "deleteBaseModel":
        result = deleteBaseModel(*params)

    elif cmd == "listInternetService":
        result = listInternetService(*params)

    elif cmd == "countCustomizedModel":
        result = countCustomizedModel(*params)

    elif cmd == "topNDurationConfig":
        result = topNDurationConfig(*params)
        print("uid,cid,label,content,duration")

    elif cmd == "listBaseModelKeyWord":
        result = listBaseModelKeyWord(*params)

    elif cmd == "printNL2SQLresult":
        result = printNL2SQLresult()

    else:
        print("Fail")
        return

    output(result)

if __name__ == "__main__":
    main()