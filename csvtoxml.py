# -*- coding: utf-8 -*-
from lxml import etree
import pandas as pd
import datetime as dt

df = pd.DataFrame.from_csv('')

##MODS namespace variables
mods_ns='http://www.loc.gov/mods/v3'
xsi_ns='http://www.w3.org/2001/XMLSchema-instance'
mods_schema_location='http://www.loc.gov/standards/mods/v3/mods-3-6.xsd'
ns_map = {None: mods_ns, 'xsi': xsi_ns}
    

##change nan values to type string
df['Subject 1'] = df['Subject 1'].astype(str)
df['Subject 2'] = df['Subject 2'].astype(str)
df['Subject 3'] = df['Subject 3'].astype(str)
df['Date'] = df['Date'].astype(str)
df['Job'] = df['Job'].astype(str)
df['Id'] = df['Id'].astype(str)

##iterate through rows in the DataFrame
for index, series in df[:].iterrows():
    mods = etree.Element('{'+ mods_ns +'}mods', version = '3.6', attrib={'{'+ xsi_ns +'}schemaLocation' : mods_schema_location}, 
                         nsmap=ns_map)
                         
    titleInfo_a = etree.SubElement(mods, 'titleInfo')
    title_a = etree.SubElement(titleInfo_a, 'title')
    if series['Title'].startswith('The ' or 'A ' or 'An ' ):
        title_a.text = ' '.join(series['Title'].split()[1:])
        nonSort = etree.SubElement(titleInfo_a, 'nonSort')
        nonSort.text = series['Title'].split()[0]
    else:
        title_a.text = series['Title']
        
    name_a = etree.SubElement(mods, 'name', type='personal')
    namePart_a = etree.SubElement(name_a, 'namePart')
    namePart_a.text = 'Skinner, David M., 1921-2009' 
    
    typeOfResource = etree.SubElement(mods,'typeOfResource')
    typeOfResource.text = 'still image'
    
    genre = etree.SubElement(mods, 'genre', authority='lctgm', authorityURI='http://id.loc.gov/vocabulary/graphicMaterials', valueURI='http://id.loc.gov/vocabulary/graphicMaterials/tgm007721')
    genre.text = 'Photographs'
    
    originInfo = etree.SubElement(mods, 'originInfo')
    place = etree.SubElement(originInfo, 'place')
    placeterm = etree.SubElement(place, 'placeTerm', type='text')
    placeterm.text = 'Charlottesville, Va.'
    publisher = etree.SubElement(originInfo, 'publisher', supplied='yes')        
    publisher.text = 'The Rectors and Visitors of the University of Virginia'
    
    dateCreated = etree.SubElement(originInfo, 'dateCreated', encoding='edtf', keyDate='yes')
    dateCreated.text = series['Date'].rstrip()
    
    physicalDescription = etree.SubElement(mods, 'physicalDescription')
    internetMediaType = etree.SubElement(physicalDescription, 'internetMediaType')
    internetMediaType.text = 'image/tiff'
    extent = etree.SubElement(physicalDescription, 'extent')
    extent.text = '1 photograph'
    digitalOrigin = etree.SubElement(physicalDescription, 'digitalOrigin')
    digitalOrigin.text = 'reformatted digital'
    
    note_a = etree.SubElement(mods, 'note', displayLabel='staff')
    note_a.text = 'Original photographs and negatives arranged in sequence by file numbers, not the original job orders stamped on them.'
    note_b = etree.SubElement(mods, 'note', displayLabel='staff')   
    note_b.text = 'From the non-portrait file of David Skinner, photographer for the University of Virginia Graphic Communications Services.'
    note_c = etree.SubElement(mods, 'note', displayLabel='staff')
    note_c.text = 'Additional non-digitized items from the collection are available by patron request in the Special Collections Reading Room.' 
    
    for i in df.loc[:, 'Subject 1':'Subject 3']:       
        topical_term = series[i]
        if topical_term == 'nan':
            topical_term = ''
        elif topical_term.startswith('Special'):
            authority_URI = 'http://id.worldcat.org/fast/'
            subject = etree.SubElement(mods, 'subject', authority = 'fast', authorityURI=authority_URI)
            subject_data = topical_term.split('|')
            subject_data = [i.strip(' ') for i in subject_data]
            topic = etree.SubElement(subject, 'topic', valueURI=authority_URI + subject_data[1])
            topic.text = subject_data[0]
        else:
            authority_URI = 'http://id.loc.gov/vocabulary/graphicMaterials/'
            valueURIprefix = 'http://id.loc.gov/vocabulary/graphicMaterials/'
            subject = etree.SubElement(mods, 'subject', authority = 'lctgm', authorityURI=authority_URI)
            subject_data = topical_term.split('|')
            subject_data = [i.strip(' ') for i in subject_data]
            topic = etree.SubElement(subject, 'topic', valueURI=authority_URI + subject_data[1])
            topic.text = subject_data[0]
    subject_4 = etree.SubElement(mods, 'subject', authority='lcsh', authorityURI='http://id.loc.gov/authorities/subjects')
    name_4 = etree.SubElement(subject_4, 'name', type='corporate', authority='naf', authorityURI='http://id.loc.gov/authorities/names', valueURI='http://id.loc.gov/authorities/names/n79053979')
    namePart_4 = etree.SubElement(name_4, 'namePart')
    namePart_4.text = 'University of Virginia'
    
    subject_5 = etree.SubElement(mods, 'subject', authority='tgn')
    hierarchicalGeographic = etree.SubElement(subject_5, 'hierarchicalGeographic')
    country = etree.SubElement(hierarchicalGeographic, 'country', valueURI='http://vocab.getty.edu/tgn/7012149')
    country.text = 'United States'
    state = etree.SubElement(hierarchicalGeographic, 'state', valueURI='http://vocab.getty.edu/tgn/2030538')
    state.text = 'Virginia'
    city = etree.SubElement(hierarchicalGeographic, 'city', valueURI='http://vocab.getty.edu/tgn/7013585')
    city.text = 'Charlottesville'
    relatedItem_a = etree.SubElement(mods, 'relatedItem', type='series', displayLabel='Part of')
    titleInfo_b = etree.SubElement(relatedItem_a, 'titleInfo')
    title_b = etree.SubElement(titleInfo_b, 'title')
    title_b.text = 'University of Virginia Printing Services photograph file'
    
    relatedItem_b = etree.SubElement(mods, 'relatedItem', type='series', displayLabel='Part of')
    titleInfo_c = etree.SubElement(relatedItem_b, 'titleInfo')
    title_c = etree.SubElement(titleInfo_c, 'title')
    title_c.text = 'University of Virginia Visual History Collection'
    
    identifier_a = etree.SubElement(mods, 'identifier', type='legacy', displayLabel='Retrieval ID') 
    if series['Job'] == 'nan':
        identifier_a.text = ''
    else:
        identifier_a.text = str(series['Job'])
    identifier_b = etree.SubElement(mods, 'identifier', type='accession number')
    identifier_b.text = series['Call']
    identifier_c = etree.SubElement(mods, 'identifier', type='pid', displayLabel='UVA Library Fedora repository PID')
    identifier_c.text = series['Pid']
    identifier_d = etree.SubElement(mods, 'identifier', type='local', displayLabel='File name')
    identifier_d.text = series['Filename']
    identifier_e = etree.SubElement(mods, 'identifier', type='local', displayLabel='Master file ID')  
    identifier_e.text = series['Id']
    
    location = etree.SubElement(mods, 'location')
    physicalLocation = etree.SubElement(location, 'physicalLocation')
    physicalLocation.text = 'Special Collections Library, University of Virginia Libraries, Charlottesville, Va.'
    shelfLocation = etree.SubElement(location, 'shelfLocator')
    shelfLocation.text = series['Location']
    
    recordInfo = etree.SubElement(mods, 'recordInfo')
    recordContentSource = etree.SubElement(recordInfo, 'recordContentSource', authority='marcorg')
    recordContentSource.text = 'viu'
    recordCreationDate = etree.SubElement(recordInfo, 'recordCreationDate', encoding='edtf')
    today = dt.datetime.today().strftime('%Y-%m-%d')    
    recordCreationDate.text = today
    languageOfCataloging = etree.SubElement(recordInfo, 'languageOfCataloging')
    languageTerm = etree.SubElement(languageOfCataloging, 'languageTerm', type='code', authority='iso639-2b')
    languageTerm.text = 'eng'
    descriptionStandard = etree.SubElement(recordInfo, 'descriptionStandard')
    descriptionStandard.text = 'dacs'
    
    filename = series['Filename']
    filename = filename[0:14]
    with open(filename +'.xml', 'wb') as f:
        f.write(etree.tostring(mods, xml_declaration=True, encoding='utf-8', pretty_print=True))
    
    
