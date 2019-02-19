import urllib.request
import urllib.parse
import json
import pprint
import csv
import pandas as pd

STRINGS_FOR_TEST = ["Computer","Collaborative", "Machine", "Colombia",
                    "Universidad","Colombian","Health", "Technology", "Web", "Algorithm"
                    "Data", "Business", "Develop", "Healthcare", "Internet", "Network", "Blockchain"
                    "Architecture", "Map", "Artificial", "Intelligence", "Security", "Music",
                    "Wave", "Mobile", "App", "Deep", "Learning", "Natural", "Language","Neuronal",
                    "Net", "Protocol", "Analytics", "Visualization", "science", "System", "Design",
                    "Software", "Hardware", "Memory", "Structure", "Programming", "Model",
                    "Diagram", "Frame", "Java", "Interface", "Mathematics", "Biology", "Pictures",
                    "Pixels", "Bits", "Bytes", "Disk", "Transaction", "Socket", "Port", "Html", 
                    "Performance", "Salability", "Authentication", "Foreing", "Index", "Electronic",
                    "Energy", "Availability", "Conection", "Time",
                    "Physics","Repository", "United", "Sport",
                    "Social","Comunication","Skills", "Nanotechnology", "Cuantic", "Cell"
                    "Fiction", "Video", "Audio", "RGB", "Color", "Shape", "Flavor"
                    "Need", "Localization", "Path", "Integrity", "Efficient", "Display",
                    "Emotion", "Feeling", "Finger", "Book", "Word", "People", "Race","Right",
                    "Law", "Punish", "Backend", "Frontend", "iPhone", "Mac", "Windows",
                    "Microsoft", "Apple", "Code", "Android", "iOS", "Operative",
                    "Camera", "Library", "Javascript", "CSS", "Python", "Water", "Function",
                    "Light", "Space", "Button", "Click", "GUI", "Experience", "kernel", "Linux", 
                    "Unix", "Core", "Stack", "Queue", "Heap", "Sort",
                    "Merge", "Chemistry", "Collection", "Set",
                    "Room","Synchorize", "Serializable", "Germany",
                    "College","University","School", "Research", "Asynchronus", "Pipe"
                    "Filter", "Sound", "Developer", "Test", "Boss", "Package", "Project"
                    "Country", "Blood", "Device", "Robot", "Machine", "Animal",
                    "Food", "Cancer", "Vacine", "Pattern", "Teach", "Recognize", "Pedagogy","Government",
                    "Heart", "Atom", "Mouth", "Liquid", "Astrology", "Gravity", "Soccer",
                    "TV", "Cast", "Dream", "Team", "Soft", "Believe",
                    "Evolution", "Care", "IoT", "Interfaz", "Math", "Geology", "Server",
                    "Client", "Wrapper", "Style", "Agile", "Method", "Websocket", "Car", "Engine", 
                    "Fire", "Sell", "Computer", "Videogames", "Smile", "Root",
                    "History", "Spain", "Clothes", "Contact",
                    "Wood","Writing", "Material", "China",
                    "Product","Innovation","Start", "Technologic", "Page", "Voice"
                    "Command", "Row", "Column", "Print", "3D", "Cinema", "Serie"
                    "Speech", "Presentation", "Persistence", "Save", "Import", "Export",
                    "Fun", "Remember", "Aplication", "Program", "Tool", "Nature", "File","Explorer",
                    "Discover", "Geography", "Channel", "Watch", "Name", "Like", "Links",
                    "Update", "Version", "Control", "Quick", "Speed", "Modeling",
                    "Draw", "License", "Loop", "Wiki", "Tone", "Beat", "Pdf",
                    "Calculate", "Create", "Hands", "Arms", "Army", "Weapon", "War", "Child", 
                    "Old", "Disability", "Blind", "Size", "Length", "Drop",
                    "Table", "Relation", "Stop", "Shoes",
                    "Poor","Poverty", "Speak", "Assistance",
                    "Pull","Push","Font", "Label", "Field", "Clasification"
                    "Question", "Answer", "Argue", "Proof", "Cold", "Weather", "World"
                    "Optimization", "Simulate", "Special", "Input", "Output", "Effect",]

with open('out.json','w') as fp:
    for i in STRINGS_FOR_TEST:
        print("Searching by: " + i)
        url = 'https://core.ac.uk:443/api-v2/articles/search/'+i+'?Here the API key'
        print(url)
        with urllib.request.urlopen(url) as response:
            resp = response.read()
            result_as_json = json.loads(resp.decode('utf-8'))
            print(result_as_json)
            json.dump(result_as_json,fp)

 