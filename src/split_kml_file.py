import re, os, glob
import xml.etree.ElementTree as ET

RESULT_DIR = "./result/"
START = r'<?xml version="1.0" encoding="UTF-8"?>' + "\n" + r'<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">' + "\n\t"
END = "</kml>"

def create_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)

def get_formatted_name(element):
    formattedName = "default"
    nameElement = element.find("{http://www.opengis.net/kml/2.2}name")
    if nameElement is not None: 
        formattedName = nameElement.text
    formattedName = str(formattedName).strip().replace(' ', '_')
    formattedName = re.sub(r'(?u)[^-\w.]', '', formattedName)
    return formattedName

kmlFiles = glob.glob("*.kml")
if kmlFiles:
    create_directory(RESULT_DIR)
    ET.register_namespace('', "http://www.opengis.net/kml/2.2")
    tree = ET.parse(kmlFiles[0])
    root = tree.getroot()  
    
    # needed because there is no parent function in ElementTree
    parent_map = {c: p for p in tree.iter() for c in p} 

    docList = [i for i in root.iter("{http://www.opengis.net/kml/2.2}Document")]
    for kDoc in docList:
        fileName = get_formatted_name(kDoc) + ".kml"
        folderName = RESULT_DIR + get_formatted_name(parent_map[kDoc])
        print(fileName, folderName)
        create_directory(folderName)
        fullPath = folderName + "/" + fileName
        xmlString = START + ET.tostring(kDoc, encoding="unicode") + END
        with open(fullPath, 'w', encoding="utf-8") as f:
            f.write(xmlString)