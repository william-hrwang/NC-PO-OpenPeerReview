import requests
import json
from lxml import etree
import re
import datetime as dt
import time
import csv
import os

s = requests.session()
s.keep_alive = False
# Close unnecessary url

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36"
}



# input the number of content, return article ID list
def getArtUrl(contNum):
    artIdLs = []
    for i in range(1,int(contNum)+1):
        contUrl = f"https://journals.plos.org/plosone/browse?resultView=list&page={i}"
        contText = requests.get(url=contUrl, headers=headers).text
        contTree = etree.HTML(contText)
        urlLs = contTree.xpath('//ul[@id="search-results"]/li/@data-doi')
        artIdLs_temp = list(map(lambda x: x[-7:], urlLs))
        for item in artIdLs_temp:
            if item in artIdLs:
                with open('plosContWrong.txt','a+',encoding='utf-8') as f:
                    f.write(contUrl)
                    f.write('\n')
                artIdLs.append(item)
            else:
                artIdLs.append(item)

    with open('artNum.txt','a+',encoding='utf-8') as f:
        f.write(f'原始数据共{len(artIdLs)}')

        artIdLs = list(set(artIdLs)).sort(key=artIdLs.index)
        print(f"In total, get {len(artIdLs)} articles")
    return artIdLs


# input article Url , return title, artType, citation, receiveDate, acceptDate, publishDate, Re_Ac_Day, Re_Pb_Day, Ac_Pb_Day, Ci_Pu_Day, Peer_Review_csv, OpenAccess_csv
def getArtDetail(urlID):
    url = "https://journals.plos.org/plosone/article?id=10.1371/journal.pone." + str(urlID)
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    # get Title
    Title_Raw = tree.xpath('//h1[@id="artTitle"]')[0]
    title = Title_Raw.xpath('string(.)')

    # get artType
    artType = tree.xpath('//p[@id="artType"]/text()')[0]

    # get Citation
    # citationUrl = 'https://metrics-api.dimensions.ai/doi/10.1371/journal.pone.0254762'
    try:
        citationUrl = "https://metrics-api.dimensions.ai/doi/10.1371/journal.pone." + url[-7:]
        # get article ID
        cite = requests.get(citationUrl, timeout=10, headers=headers).text
        citation = json.loads(cite).get('times_cited')

    except:
        citation = 0


    # get Accept Date, Receive Date, Publish Date, and time compared
    Receive_Search = '<strong>Received:\s</strong>(.*?);\s<strong>'
    Receive_Date = re.findall(Receive_Search, page_text, re.S)
    Receive_Date.append("0")
    if Receive_Date[0] != str(0):
        receiveDate = dt.datetime.strptime(Receive_Date[0], "%B %d, %Y").date()
    else:
        receiveDate = 0
    Accept_Search = '<strong>Accepted:\s</strong>(.*?);\s<strong>'
    Accept_Date = re.findall(Accept_Search, page_text, re.S)
    Accept_Date.append("0")
    if Accept_Date[0] != str(0):
        acceptDate = dt.datetime.strptime(Accept_Date[0], "%B %d, %Y").date()
    else:
        acceptDate = 0
    Publish_Search = '<strong>Published:\s</strong>\s(.*?)</p><p>'
    Publish_Date = re.findall(Publish_Search, page_text, re.S)
    Publish_Date.append("0")
    if Publish_Date[0] != str(0):
        publishDate = dt.datetime.strptime(Publish_Date[0], "%B %d, %Y").date()
    else:
        publishDate = 0
    # Days Between Receive and Accept Date
    try:
        Re_Ac_Day = (acceptDate - receiveDate).days
    except:
        Re_Ac_Day = "none"
    # Days Between Receive and Publish Date
    try:
        Re_Pb_Day = (publishDate - receiveDate).days
    except:
        Re_Pb_Day = 'none'
    # Days Between Accept and Publish Date
    try:
        Ac_Pb_Day = (publishDate - acceptDate).days
    except:
        Ac_Pb_Day = 'none'
    # CitationTime Compared
    now = time.strftime('%Y-%m-%d', time.localtime())
    citationDate = dt.datetime.strptime(now, '%Y-%m-%d').date()
    Ci_Pu_Day = (citationDate - publishDate).days

    # get Peer Review
    Peer_pattern = re.compile('(Peer Review)</a>', re.S)
    Peer_Review = Peer_pattern.search(page_text)
    # print(Peer_Review)
    if str(Peer_Review) != "None":
        Peer_Review_csv = 1
    else:
        Peer_Review_csv = 0

    # get Open Access
    Open_Access_pattern = re.compile('<p class="license-short" id="licenseShort">(Open Access)<\/p>', re.S)
    OpenAccess = Open_Access_pattern.search(page_text)
    # print(OpenAccess)
    if str(OpenAccess) != "None":
        OpenAccess_csv = 1
    else:
        OpenAccess_csv = 0


    return title, artType, citation, receiveDate, acceptDate, publishDate, Re_Ac_Day, Re_Pb_Day, Ac_Pb_Day, Ci_Pu_Day, Peer_Review_csv, OpenAccess_csv

def getArtMetrics(urlID):
    try:
        url = "https://journals.plos.org/plosone/article?id=10.1371/journal.pone." + str(urlID)
        URL_json = "https://api.altmetric.com/v1/doi/10.1371/journal.pone." + str(urlID)
        r_1 = requests.get(URL_json, headers=headers)

        try:
            altmetric_img = json.loads(r_1.text).get('images')
            almetric_Search = 'size=.*&score=(.*?)&types'
            almetric = re.findall(almetric_Search, altmetric_img["small"], re.S)[0]
            altmetric_csv = almetric

        except:
            altmetric_csv = 0
            altmetric_json = r_1.status_code
            with open("metricsWrong1.txt", "a+", encoding="utf-8") as f:
                f.write(url)
                f.write("\n")

    except:
        url = "https://journals.plos.org/plosone/article?id=10.1371/journal.pone." + str(urlID)
        altmetric_csv = 0
        altmetric_json = "Fail Connected"
        with open("metricsWrong2.txt", "a+", encoding="utf-8") as f:
            f.write(url)
            f.write("\n")

    return altmetric_csv

# input url and Peer review , return open Identity
# None open Peer Review ——> 0
# Open Peer Review but without attitude towards open Identity ——> 1
# Open Peer Review and totally refuse open Identity which means anonymous——> 2
# Open Peer Review and partly open Identity ——> 3
# Open Peer Review and totally open Identity ——> 4
def artOpenId(urlID,Peer_Review_csv):
    if Peer_Review_csv == 0:
        openIdentity = 0
    else:
        url = 'https://journals.plos.org/plosone/article/peerReview?id=10.1371/journal.pone.' + str(urlID)
        text = requests.get(url=url, headers=headers).text
        Tree = etree.HTML(text)
        PeerReview = Tree.xpath(
            '//strong[text()="Do you want your identity to be public for this peer review?"]/../following-sibling::p[contains(text(),"Reviewer")]//text()')
        PeerReviewLs = list(map(lambda x: x.replace("\xa0", ""), PeerReview))
        haveAnonyId_Ls = []
        haveOpenId_Ls = []
        for item in PeerReviewLs:
            if 14 <= len(item) <= 16 and ": No" in item:
                haveAnonyId_Ls.append(1)
            if 14 <= len(item) <= 16 and ":No" in item:
                haveAnonyId_Ls.append(1)
            if len(item) >= 16 and "Yes:" in item:
                haveOpenId_Ls.append(1)

        if len(haveOpenId_Ls) == 0:
            haveOpenId = 0
            if "Yes:" in PeerReviewLs:
                haveOpenId = 1
        else:
            haveOpenId = 1
        if len(haveAnonyId_Ls) != 0:
            haveAnonyId = 1
        else:
            haveAnonyId = 0


        if haveOpenId == 1 and haveAnonyId == 1:
            openIdentity = 3
        elif haveOpenId == 0 and haveAnonyId == 1:
            openIdentity = 2
        elif haveOpenId == 1 and haveAnonyId == 0:
            openIdentity = 4

        else:
            openFirst_Ls = Tree.xpath('//strong[text()="Do you want your identity to be public for this peer review?"]/text()')
            if len(openFirst_Ls) == 0:
                openIdentity = 1
            else:
                # Handle accidents in advance (Results from Preliminary investigation)
                outExpect = {
                    "https://journals.plos.org/plosone/article/peerReview?id=10.1371/journal.pone.0261860": 1,
                    "https://journals.plos.org/plosone/article/peerReview?id=10.1371/journal.pone.0255338": 1,  # none attitude
                    "https://journals.plos.org/plosone/article/peerReview?id=10.1371/journal.pone.0249801": 3,  # partly open
                    "https://journals.plos.org/plosone/article/peerReview?id=10.1371/journal.pone.0249079": 2,  # anonymous
                    "https://journals.plos.org/plosone/article/peerReview?id=10.1371/journal.pone.0248274": 2,  # anonymous
                    "https://journals.plos.org/plosone/article/peerReview?id=10.1371/journal.pone.0245921": 2,  # anonymous
                    "https://journals.plos.org/plosone/article/peerReview?id=10.1371/journal.pone.0245171": 1,  # none attitude
                    "https://journals.plos.org/plosone/article/peerReview?id=10.1371/journal.pone.0242193": 3,  # partly open
                    "https://journals.plos.org/plosone/article/peerReview?id=10.1371/journal.pone.0241927": 4,  # totally open
                    "https://journals.plos.org/plosone/article/peerReview?id=10.1371/journal.pone.0233699": 2,  # anonymous
                    "https://journals.plos.org/plosone/article/peerReview?id=10.1371/journal.pone.0264595": 3,  # partly open
                }
                if url in list(outExpect.keys()):
                    openIdentity = str(outExpect[url])
                else:
                    print(f"{url} have problem")
                    openIdentity = 5
                    with open('identityWrong.txt', 'a+', encoding='utf-8') as f:
                        f.write(url)
                        f.write('\n')

    return openIdentity


# return artTypeDict and artContentType_dict
def artType():
    # article content
    artTypeContent_Dict = {
        'Biology_and_life_sciences': ['https://journals.plos.org/plosone/browse/biology_and_life_sciences?resultView=list&page=', '8050'],  # 8050
        'Computer_and_information_sciences': ['https://journals.plos.org/plosone/browse/computer_and_information_sciences?resultView=list&page=', '1350'],  # 1350
        'Earth_sciences': ['https://journals.plos.org/plosone/browse/computer_and_information_sciences?resultView=list&page=', '1400'],  # 1400
        'Ecology_and_environmental_sciences': ['https://journals.plos.org/plosone/browse/ecology_and_environmental_sciences?resultView=list&page=', '900'],  # 900
        'Engineering_and_technology': ['https://journals.plos.org/plosone/browse/engineering_and_technology?resultView=list&page=', '1500'],  # 1500
        'Medicine_and_health_sciences': ['https://journals.plos.org/plosone/browse/medicine_and_health_sciences?resultView=list&page=', '7000'],  # 7000
        'People_and_places': ['https://journals.plos.org/plosone/browse/people_and_places?resultView=list&page=', '2300'],  # 2300
        'Physical_sciences': ['https://journals.plos.org/plosone/browse/physical_sciences?resultView=list&page=', '3500'],  # 3500
        'Research_and_analysis_methods': ['https://journals.plos.org/plosone/browse/research_and_analysis_methods?resultView=list&page=', '4550'],  # 4550
        'Science_policy': ['https://journals.plos.org/plosone/browse/science_policy?resultView=list&page=', '150'],  # 150
        'Social_sciences': ['https://journals.plos.org/plosone/browse/social_sciences?resultView=list&page=', '2800'],  # 2800
    }

    # article content dictionary
    artTypeDict = {
        'Biology_and_life_sciences': [],
        'Computer_and_information_sciences': [],
        'Earth_sciences': [],
        'Ecology_and_environmental_sciences': [],
        'Engineering_and_technology': [],
        'Medicine_and_health_sciences': [],
        'People_and_places': [],
        'Physical_sciences': [],
        'Research_and_analysis_methods': [],
        'Science_policy': [],
        'Social_sciences': []
    }

    for item in list(artTypeContent_Dict.keys()):
        for i in range(1, int(artTypeContent_Dict[item][1])+1):
            artTypeContentUrl = artTypeContent_Dict[item][0] + str(i)
            contText = requests.get(url=artTypeContentUrl, headers=headers).text
            contTree = etree.HTML(contText)
            urlLs = contTree.xpath('//ul[@id="search-results"]/li/@data-doi')
            artIdLs = list(map(lambda x: x[-7:], urlLs))
            artTypeDict[item] = artTypeDict[item] + artIdLs

    with open('artNum.txt', 'a+', encoding='utf-8') as f:
        for item in list(artTypeContent_Dict.keys()):
            artTypeDict[item] = list(set(artTypeDict[item])).sort(key=artTypeDict[item].index)
            f.write(f'Discipline: {item} have {len(artTypeDict[item])} articles')

    return artTypeDict,artTypeContent_Dict


# input articleId ,return article Type
def artTypeMatch(id, artTypeContent_Dict, artTypeDict):
    # match subject
    url = "https://journals.plos.org/plosone/article?id=10.1371/journal.pone." + str(id)
    urlId = url[-7:]
    is_notArtSubjectLs = []
    for item in list(artTypeContent_Dict.keys()):
        if urlId in artTypeDict[item]:
            is_notArtSubjectLs.append('1')
            artTypeDict[item].remove(urlId)
            with open(f'/home/Plos_One/subject/{item}/{item}_Plos_One_Data.csv', 'a+', newline='', encoding='utf-8_sig') as sub_csvfile:
                subjectWriter = csv.writer(sub_csvfile)
                subjectWriter.writerow([url, title, citation, altMetrics, OpenAccess_csv, Peer_Review_csv, receiveDate, acceptDate, publishDate, Re_Ac_Day, Re_Pb_Day, Ac_Pb_Day, Ci_Pu_Day, openIdentity])
        else:
            is_notArtSubjectLs.append('0')
    if '1' not in is_notArtSubjectLs:
        is_notArtSubject = True
        with open('wrongSubject.txt','a+',encoding='utf-8') as f:
            f.write(url)
            f.write('\n')
            print(f'{url} belong to no discipline')


artTitle_temp = []
with open('PlosOneData_(5.16).csv','a+',newline='',encoding='utf-8_sig') as csvfile:
    # write the head
    writer = csv.writer(csvfile)
    writer.writerow(['Url','Title','Citation','Metrics','Open_Access','Peer_Review','Receive_Data','Accept_Data','Publish_Data','Re_Ac_Day','Re_Pb_Day','Ac_Pb_Day','Ci_Pu_Day','open Identity'])

    artIdLs = getArtUrl(9200)  # get artIdLs   #9200
    with open('articleUrl.txt','a+',encoding='utf-8') as f:
        for urlID in artIdLs:
            url = "https://journals.plos.org/plosone/article?id=10.1371/journal.pone." + str(urlID)
            f.write(url)
            f.write('\n')

    artTypeDict, artTypeContent_Dict = artType()  # get article Type
    json_str = json.dumps(artTypeDict, indent=4)
    with open('artType.json', 'a+') as json_file:
        json_file.write(json_str)

    for item in list(artTypeContent_Dict.keys()):
        path = f'/home/Plos_One_5_16/subject/{item}/'
        os.makedirs(path)

    for urlID in artIdLs:
        url = "https://journals.plos.org/plosone/article?id=10.1371/journal.pone." + str(urlID)
        print(f'Crawler {url}')
        try:
            title, artType, citation, receiveDate, acceptDate, publishDate, Re_Ac_Day, Re_Pb_Day, Ac_Pb_Day, Ci_Pu_Day, Peer_Review_csv, OpenAccess_csv = getArtDetail(urlID)
            openIdentity = artOpenId(urlID,Peer_Review_csv)
            altMetrics = getArtMetrics(urlID)

            wrongArtTitle = ["Correction:", "Retraction: ", "Correction to Expression of Concern on:", "Expression of Concern:", "Correction draft:", "Correction draft:", "Correction to Retraction of:", "Correction to Expression of Concern:"]
            for item in wrongArtTitle:
                if item not in str(title):
                    is_artTitle = True
                else:
                    is_artTitle = False

            is_artType = True
            if artType not in ['Research Article', 'Article']:
                is_artType = False

            if is_artTitle and is_artType:
                writer.writerow([url, title, citation, altMetrics, OpenAccess_csv, Peer_Review_csv, receiveDate, acceptDate, publishDate, Re_Ac_Day, Re_Pb_Day, Ac_Pb_Day, Ci_Pu_Day, openIdentity])
                artTypeMatch(urlID, artTypeContent_Dict, artTypeDict)
            else:
                artIdLs.remove(urlID)

        except:
            with open('plosOneWrong.txt','a+',encoding='utf-8') as f:
                f.write(url)
                f.write('\n')
                print(f'{url} have problems')


print('Finish running the project.')
