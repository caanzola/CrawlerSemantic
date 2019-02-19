from bs4 import BeautifulSoup
import pandas as pd
import requests

#options
STRINGS_FOR_TEST = ["Computer science","Collaborative Writing", "Machine learning", "Colombia",
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
                    "Physics","Repository", "United States", "Sport",
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
                    "Optimization", "Simulate", "Special", "Input", "Output", "Effect"]


DBLP_BASE_URL = 'http://dblp.uni-trier.de/'
PUB_SEARCH_URL = DBLP_BASE_URL + "search/publ/"


def query_db(pub_string):
    '''
    returns the BeautifulSoup object of a query to DBLP

    :param pub_string: A list of strings of keywords
    :return: BeautifulSoup: A BeautifulSoup Object
    '''
    print("Searching by: "+pub_string)
    resp = requests.get(PUB_SEARCH_URL, params={'q':pub_string})
    return BeautifulSoup(resp.content, "lxml")

def get_pub_data(pub):
    '''
    Extracts the information about a publication from a BeautifulSoup object

    :param pub: A BeautifulSoup Object with Publication Information
    :return: dict: All Information of this Publication
    '''
    ptype = 'nothing'
    link = 'nothing'
    authors = []
    title = 'nothing'
    where = 'nothing'

    if 'year' in pub.get('class'):
        # year is not always scrapable, except for this case. Might be done more elegantly
        return int(pub.contents[0])
    else:
        ptype = pub.attrs.get('class')[1]
        for content_item in pub.contents:
            class_of_content_item = content_item.attrs.get('class', [0])
            if 'data' in class_of_content_item:
                for author in content_item.findAll('span', attrs={"itemprop": "author"}):
                    authors.append(author.text)
                title = content_item.find('span', attrs={"class": "title"}).text
                for where_data in content_item.findAll('span', attrs={"itemprop": "isPartOf"}):
                    found_where = where_data.find('span', attrs={"itemprop": "name"})
                    if found_where:
                        where = found_where.text
            elif 'publ' in class_of_content_item:
                link = content_item.contents[0].find('a').attrs.get('href', "nothing")

    return {'Type': ptype,
            'Link': link,
            'Authors': authors,
            'Title': title,
            'Where': where}

def search(search_string=STRINGS_FOR_TEST):
    '''
    returns the information found in a search query to dblp as a pandas dataframe.
    Shows the following information:
        - Authors
        - Link to Publication
        - Title
        - Type (Article, Proceedings etc.)
        - Where it was published
        - Year of publication
    :param search_string: A List of Strings of Keywords, that should be searched for
    :return: pd.DataFrame: A Dataframe with all data
    '''
    soup = query_db(search_string)
    pub_list_raw = soup.find("ul", attrs={"class": "publ-list"})

    pub_list_data = []
    curr_year = 0
    for child in pub_list_raw.children:
        pub_data = get_pub_data(child)
        if type(pub_data) == int:
            curr_year = pub_data
        else:
            pub_data['Year'] = curr_year
            pub_list_data.append(pub_data)

        
    return pd.DataFrame(pub_list_data)

frames = []

for i in STRINGS_FOR_TEST:
    x = search(i)    
    #print(x)
    frames.append(x)


result = pd.concat(frames)
result.to_csv("csv_DblpCrawler.csv", index=False)
#print(result)

