import json

with open("info.json", "r") as file:
    # user with gmail domain
    data: dict = json.load(file)

    print("which domains do you want to see?")

    while True:
        domain = input("gmail, yahoo, other (q to quit): ")
        if domain == "q":
            break
        
        if domain not in data["email domains"]:
            print("invalid domain")
            continue # to go back to the start of the loop
        
        if domain in data["email domains"]:
            for email in data["email domains"][domain].values():
                print(email)
