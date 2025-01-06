# Challenge 1 City suggestion API
# Problem

![Reese  Infrastructure Interview](https://github.com/user-attachments/assets/31734cfd-8abe-4111-aa84-a2cb0380560e)

# Basics and Usage
This is a API that "processs" text files. By appending the word Processed to them.

Ex when running locally:

    http://127.0.0.1:8000/trigger

    Body= {
        Files:[
            {
                "FileUri": "Some file location"
                "OutUri": "Some file Destination"
            },
            ...
            {
                "FileUri": "Another file location"
                "OutUri": "Another file Destination"
            }
        ]
    }    
The api will then return a Job Id

        { 
            job_id:
        }

# Read me TODO
- [x] Trigger example
- [ ] Status example
- [ ] Retreive example
- [ ] Describe FileProcessor Middle where
- [ ] integrate with cellary for pub sub
- [ ] add Dev postgres db creation file
