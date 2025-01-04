import time
import requests
import re
from lxml import etree
import csv
from bs4 import BeautifulSoup
import urllib3
import statistics
import json
import datetime as dt
urllib3.disable_warnings()


s = requests.session()
s.keep_alive = False


headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}


# Specify the desired page number
def getArtUrl(contentNum):
    print("Start crawling the article directory")
    content_ls = []
    artUrl_ls = []
    for num in range(1,contentNum+1):
        contentUrl = f"https://www.nature.com/ncomms/research-articles?searchType=journalSearch&sort=PubDate&type=article&page={num}"
        content_ls.append(contentUrl)

    for contentUrl in content_ls:
        print(f"Crawling article directory pages: {contentUrl}")
        content_text = requests.get(url=contentUrl,headers=headers).text
        contentTree = etree.HTML(content_text)
        artUrl_raw = contentTree.xpath('//h3[@class="c-card__title"]/a/@href')
        for artUrlRaw in artUrl_raw:
            artUrl = "https://www.nature.com" + artUrlRaw
            if artUrl in artUrl_ls:
                print(f'There is a problem with crawling the content {contentUrl}')
                with open('contWrong.txt','a+',encoding='utf-8') as f:
                    f.write(contentUrl)
                    f.write('\n')
            artUrl_ls.append(artUrl)

    return artUrl_ls


# Crawl article classification
# Return phyArt_Dict,earArt_Dict,bioArt_Dict,heaArt_Dict,sciArt_Dict
def getArtType():
    print("Crawling article types, preparing to generate dictionary")
    artType_Dict = {}
    # Physical Science
    phyUrl_Content_ls = []
    phyArtUrl_ls = []
    for num in range(1,250):  # 314
        contentUrl = f"https://www.nature.com/subjects/physical-sciences/ncomms?searchType=journalSearch&sort=PubDate&page={num}"
        phyUrl_Content_ls.append(contentUrl)
    for url in phyUrl_Content_ls:
        print(f"Crawling articles of Physical type: {url}")
        page_text = requests.get(url=url, headers=headers, verify=False).text
        tree = etree.HTML(page_text)
        raw_ArticleUrl = tree.xpath('.//span[@data-test="article.type" and text()="Article"]/../following-sibling::h3[contains(@class,"mb10")]/a/@href')
        for rawUrl in raw_ArticleUrl:
            artUrl = "https://www.nature.com" + rawUrl
            # Determine whether there is a website update or duplicate articles
            if artUrl in phyArtUrl_ls:
                print(f"The content {url} is wrong, please check it in time")
                with open('contWrong.txt','a+',encoding='utf-8') as f:
                    f.write(url)
                    f.write('\n')
            phyArtUrl_ls.append(artUrl)
    artType_Dict["Physical sciences"] = phyArtUrl_ls
    print("Physical Science Articles Crawled Successfully")

    # Earth and environmental sciences
    earUrl_Content_ls = []
    earArtUrl_ls = []
    for num in range(1,56):  # 62
        contentUrl = f"https://www.nature.com/subjects/earth-and-environmental-sciences/ncomms?searchType=journalSearch&sort=PubDate&page={num}"
        earUrl_Content_ls.append(contentUrl)
    for url in earUrl_Content_ls:
        print(f"Crawling articles of Earth type: {url}")
        page_text = requests.get(url=url, headers=headers, verify=False).text
        tree = etree.HTML(page_text)
        raw_ArticleUrl = tree.xpath('.//span[@data-test="article.type" and text()="Article"]/../following-sibling::h3[contains(@class,"mb10")]/a/@href')
        for rawUrl in raw_ArticleUrl:
            artUrl = "https://www.nature.com" + rawUrl
            # Determine whether there is a website update or duplicate articles
            if artUrl in earArtUrl_ls:
                print(f"The content {url} is wrong, please check it in time")
                with open('contWrong.txt','a+',encoding='utf-8') as f:
                    f.write(url)
                    f.write('\n')
            earArtUrl_ls.append(artUrl)
    artType_Dict["Earth and environmental sciences"] = earArtUrl_ls
    print("Earth Articles Crawled Successfully")

    # Biological sciences
    bioUrl_Content_ls = []
    bioArtUrl_ls = []
    for num in range(1,420):  # 509
        contentUrl = f"https://www.nature.com/subjects/biological-sciences/ncomms?searchType=journalSearch&sort=PubDate&page={num}"
        bioUrl_Content_ls.append(contentUrl)
    for url in bioUrl_Content_ls:
        print(f"Crawling articles of Biological type: {url}")
        page_text = requests.get(url=url, headers=headers, verify=False).text
        tree = etree.HTML(page_text)
        raw_ArticleUrl = tree.xpath('.//span[@data-test="article.type" and text()="Article"]/../following-sibling::h3[contains(@class,"mb10")]/a/@href')
        for rawUrl in raw_ArticleUrl:
            artUrl = "https://www.nature.com" + rawUrl
            # Determine whether there is a website update or duplicate articles
            if artUrl in bioArtUrl_ls:
                print(f"The content {url} is wrong, please check it in time")
                with open('contWrong.txt','a+',encoding='utf-8') as f:
                    f.write(url)
                    f.write('\n')
            bioArtUrl_ls.append(artUrl)
    artType_Dict["Biological sciences"] = bioArtUrl_ls
    print("Biological Articles Crawled Successfully")

    # Health sciences
    heaUrl_Content_ls = []
    heaArtUrl_ls = []
    for num in range(1,95):  # 113
        contentUrl = f"https://www.nature.com/subjects/health-sciences/ncomms?searchType=journalSearch&sort=PubDate&page={num}"
        heaUrl_Content_ls.append(contentUrl)
    for url in heaUrl_Content_ls:
        print(f"Crawling articles of Health type:{url}")
        page_text = requests.get(url=url, headers=headers, verify=False).text
        tree = etree.HTML(page_text)
        raw_ArticleUrl = tree.xpath('.//span[@data-test="article.type" and text()="Article"]/../following-sibling::h3[contains(@class,"mb10")]/a/@href')
        for rawUrl in raw_ArticleUrl:
            artUrl = "https://www.nature.com" + rawUrl
            # Determine whether there is a website update or duplicate articles
            if artUrl in heaArtUrl_ls:
                print(f"The content {url} is wrong, please check it in time")
                with open('contWrong.txt','a+',encoding='utf-8') as f:
                    f.write(url)
                    f.write('\n')
            heaArtUrl_ls.append(artUrl)
    artType_Dict["Health sciences"] = heaArtUrl_ls
    print("Health Articles Crawled Successfully")

    # Scientific community and society
    sciUrl_Content_ls = []
    sciArtUrl_ls = []
    for num in range(1,11): # 11
        contentUrl = f"https://www.nature.com/subjects/scientific-community-and-society/ncomms?searchType=journalSearch&sort=PubDate&page={num}"
        sciUrl_Content_ls.append(contentUrl)
    for url in sciUrl_Content_ls:
        print(f"Crawling articles of Scientific type: {url}")
        page_text = requests.get(url=url, headers=headers, verify=False).text
        tree = etree.HTML(page_text)
        raw_ArticleUrl = tree.xpath('.//span[@data-test="article.type" and text()="Article"]/../following-sibling::h3[contains(@class,"mb10")]/a/@href')
        for rawUrl in raw_ArticleUrl:
            artUrl = "https://www.nature.com" + rawUrl
            # Determine whether there is a website update or duplicate articles
            if artUrl in sciArtUrl_ls:
                print(f"The content {url} is wrong, please check it in time")
                with open('contWrong.txt','a+',encoding='utf-8') as f:
                    f.write(url)
                    f.write('\n')
            sciArtUrl_ls.append(artUrl)
    artType_Dict["Scientific community and society"] = sciArtUrl_ls
    print("Scientific Articles Crawled Successfully")

    return artType_Dict


# get article detail
# return artTitle,OpenAccess_csv,citation,citation_time,Peer_Review_csv,receiveDate,acceptDate,publishDate,addInformatin
def getArtDetail(url):
    articleText = requests.get(url=url, headers=headers).text
    articleTree = etree.HTML(articleText)
    # get Title
    title_Search = "<title>([\s\S]*?)\| Nature Communications</title>"
    artTitle = re.findall(title_Search, articleText, re.S)[0]

    # get Open Access
    try:
        openAccess_Search = '<li class=\"c-article-identifiers__item\">[\s\n\r]*<span class=\"c-article-identifiers__open\" data-test=\"open-access\">(.*?)</span>'
        openAccess = re.findall(openAccess_Search, articleText, re.S)
        OpenAccess_csv = 1
    except:
        OpenAccess_csv = 0

    # 获取 Citation
    try:
        citation = articleTree.xpath('//span[text()="Citations"]/../text()')[0]
        citation_time = time.strftime('%Y-%m-%d', time.localtime())
    except:
        citation = 0
        citation_time = time.strftime('%Y-%m-%d', time.localtime())

    # get Open Peer Review
    try:
        peer_review = articleTree.xpath("//*[@class='print-link' and contains(text(),'Peer Review File')]/@href")[0]
        Peer_Review_csv = 1
    except:
        Peer_Review_csv = 0

    # get Receive Date
    try:
        receiveDate_Search = '<p>Received<span class=\"u-hide\">: </span><span class=\"c-bibliographic-information__value\"><time datetime=\"(.*?)\">'
        reDate = re.findall(receiveDate_Search, articleText, re.S)[0]
        receiveDate = dt.datetime.strptime(reDate, "%Y-%m-%d").date()
    except:
        receiveDate = 0

    # get Accept Date
    try:
        acceptDate_Search = '<p>Accepted<span class=\"u-hide\">: </span><span class=\"c-bibliographic-information__value\"><time datetime=\"(.*?)\">'
        acDate = re.findall(acceptDate_Search, articleText, re.S)[0]
        acceptDate = dt.datetime.strptime(acDate, "%Y-%m-%d").date()
    except:
        acceptDate = 0

    # get Publish Date
    try:
        publishDate_Search = '<p>Published<span class=\"u-hide\">: </span><span class=\"c-bibliographic-information__value\"><time datetime=\"(.*?)\">'
        puDate = re.findall(publishDate_Search, articleText, re.S)[0]
        publishDate = dt.datetime.strptime(puDate, "%Y-%m-%d").date()
    except:
        publishDate = 0


    # get Additional Information to encode Open Identity
    try:
        addInformation_raw = articleTree.xpath("//div[@id='peer-review-content']/p//text()")
        str = ' '
        addInformation = str.join(addInformation_raw)
        if addInformation != "":
            addInformation = str.join(addInformation_raw)
        elif addInformation == "":
            try:
                addInformation_raw = articleTree.xpath('//*[@id="additional-information-content"]')[0]
                addInformation = addInformation_raw.xpath('string(.)')
                if addInformation != "":
                    addInformation = addInformation_raw.xpath('string(.)')
                elif addInformation == "":
                    try:
                        addInformation_raw = articleTree.xpath("//h2[text()='Additional information']/..//div//text()")
                        str = ' '
                        addInformation = str.join(addInformation_raw)
                    except:
                        addInformation = 0
            except:
                try:
                    addInformation_raw = articleTree.xpath("//h2[text()='Additional Information']/..//div//text()")
                    str = ' '
                    addInformation = str.join(addInformation_raw)
                    if addInformation != "":
                        addInformation = str.join(addInformation_raw)
                    elif addInformation == '':
                        addInformation = 0
                except:
                    addInformation = 0
    except:
        addInformation = 0

    return artTitle,OpenAccess_csv,citation,citation_time,Peer_Review_csv,receiveDate,acceptDate,publishDate,addInformation


# get articles metrics
# return metrics,metricsTime,altMetricsUrl
def getArtMetrics(url):
    metricsUrl = url + "/metrics"

    # get metrics value and time
    try:
        metricsPage_text = requests.get(url=metricsUrl, headers=headers, timeout=25).text
        metricsTree = etree.HTML(metricsPage_text)
        metrics_Search = "<div.*class=\"c-article-metrics__image\">[\s\r\n]*<img.*alt=\"Altmetric\s*score\s*(.*?)\""
        metrics = re.findall(metrics_Search, metricsPage_text, re.S)[0]
        metricsTime_Search = "<li\sclass=\"c-article-identifiers__item\">Last\supdated:\s.*?,\s(.*?)\s\d{0,2}:"
        metricsTime = re.findall(metricsTime_Search, metricsPage_text, re.S)[0]
    except:
        metricsPage_text = requests.get(url=metricsUrl, headers=headers, timeout=25).text
        metricsTime_Search = "<li\sclass=\"c-article-identifiers__item\">Last\supdated:\s.*?,\s(.*?)\s\d{0,2}:"
        metricsTime = re.findall(metricsTime_Search, metricsPage_text, re.S)[0]
        metrics = 0


    # get altmetric url
    try:
        metricsPage_text = requests.get(url=metricsUrl, headers=headers, timeout=25).text
        metricsTree = etree.HTML(metricsPage_text)
        altMetricsUrl = metricsTree.xpath("//div[@class='c-article-metrics__altmetric-context-score']/p/a/@href")[0]
    except:
        altMetricsUrl = "none"

    return metrics,metricsTime,altMetricsUrl


# get alterMetrics detail
# return mentionDict,citationDict,readerDict,twGeo_Table_Dict,twDemo_Table_Dict,menGeo_Table_Dict
def getAltMetrics_Details(altMetricsUrl):
    altMetricsPage_text = requests.get(url=altMetricsUrl, headers=headers, verify=False,timeout=25).text
    altMetricsTree = etree.HTML(altMetricsPage_text)
    pageBs = BeautifulSoup(altMetricsPage_text, 'lxml')

    # get Mentioned By
    mentionDict = {}
    menCounts = []
    menCountsRaw = altMetricsTree.xpath("//*[@class='mention-counts']//a//text()")
    for item in menCountsRaw:
        item = item.lstrip()
        menCounts.append(item)
    for i in range(0,len(menCounts)):
        if i % 2 == 0:
            mentionDict[menCounts[i + 1]] = menCounts[i]

    # get Citation
    citationDict = {}
    citationCounts = []
    citationCountsRaw = altMetricsTree.xpath("//*[@class='scholarly-citation-counts']//a//text()")
    for item in citationCountsRaw:
        item = item.lstrip()
        citationCounts.append(item)
    for i in range(0,len(citationCounts)):
        if i % 2 == 0:
            citationDict[citationCounts[i + 1]] = citationCounts[i]

    #  get reader-counts
    readerDict = {}
    readCounts = []
    readCountsRaw = altMetricsTree.xpath("//*[@class='reader-counts']//a//text()")
    for item in readCountsRaw:
        item = item.lstrip()
        readCounts.append(item)
    for i in range(0,len(readCounts)):
        if i % 2 == 0:
            readerDict[readCounts[i + 1]] = readCounts[i]

    # get Twitter Geographical breakdown=
    twGeo_Table_Dict = {}
    tw_Table_Choice_Raw = pageBs.select(".twitter ")
    if len(tw_Table_Choice_Raw) != 0:
        tw_Table_Choice_Raw = pageBs.select(".twitter ")[0]
        twGeo_TableChoice = str(tw_Table_Choice_Raw .select(" .geo > table ")[0])
        # get Geographical country
        twGeo_Table_Country_pattern = re.compile("<td>([^0-9]*)</td>",re.S)
        twGeo_Table_Country = twGeo_Table_Country_pattern.findall(twGeo_TableChoice)

        twGeo_Table_Num_pattern = re.compile(r'<td class=\"num\">(\d+)</td>',re.S)
        twGeo_Table_Num = twGeo_Table_Num_pattern.findall(twGeo_TableChoice)

        twGeo_Table_Percentage_pattern = re.compile('<td class=\"num\">(\d+%)</td>',re.S)
        twGeo_Table_Percentage = twGeo_Table_Percentage_pattern.findall(twGeo_TableChoice)

        if len(twGeo_Table_Country) == len(twGeo_Table_Num) and len(twGeo_Table_Country) == len(twGeo_Table_Percentage):
            twGeo_Table_Length = len(twGeo_Table_Country)

            for i in range(0,twGeo_Table_Length):
                twGeo_Table_Dict[ twGeo_Table_Country[i] ] = {"count":twGeo_Table_Num[i],"percentage":twGeo_Table_Percentage[i]}

    # get Twitter Demographic breakdown
    twDemo_Table_Dict = {}
    twDemo_Table_Choice_Raw = pageBs.select(".twitter ")
    if len(twDemo_Table_Choice_Raw) != 0:
        twDemo_Table_Choice_Raw = pageBs.select(".twitter ")[0]
        twDemo_TableChoice = str(twDemo_Table_Choice_Raw .select(" .users > table ")[0])  # Bs 定位第一个图表

        twDemo_Table_Country_pattern = re.compile("<td>([^0-9]*)</td>",re.S)
        twDemo_Table_Country = twDemo_Table_Country_pattern.findall(twDemo_TableChoice)

        twDemo_Table_Num_pattern = re.compile(r'<td class=\"num\">(\d+)</td>',re.S)
        twDemo_Table_Num = twDemo_Table_Num_pattern.findall(twDemo_TableChoice)

        twDemo_Table_Percentage_pattern = re.compile('<td class=\"num\">(\d+%)</td>',re.S)
        twDemo_Table_Percentage = twDemo_Table_Percentage_pattern.findall(twDemo_TableChoice)

        if len(twDemo_Table_Country) == len(twDemo_Table_Num) and len(twDemo_Table_Country) == len(twDemo_Table_Percentage):
            twDemo_Table_Length = len(twDemo_Table_Country)

            for i in range(0,twDemo_Table_Length):
                twDemo_Table_Dict[ twDemo_Table_Country[i] ] = {"count":twDemo_Table_Num[i],"percentage":twDemo_Table_Percentage[i]}

    # get Mendeley Geographical
    menGeo_Table_Dict = {}
    men_Table_Choice_Raw = pageBs.select(".mendeley ")
    if len(men_Table_Choice_Raw) != 0:
        men_Table_Choice_Raw = pageBs.select(".mendeley ")[0]
        menGeo_TableChoice = str(men_Table_Choice_Raw .select(" .geo > table ")[0])  # Bs 定位第一个图表

        menGeo_Table_Country_pattern = re.compile("<td>([^0-9]*)</td>",re.S)
        menGeo_Table_Country = menGeo_Table_Country_pattern.findall(menGeo_TableChoice)

        menGeo_Table_Num_pattern = re.compile(r'<td class=\"num\">(\d+)</td>',re.S)
        menGeo_Table_Num = menGeo_Table_Num_pattern.findall(menGeo_TableChoice)

        menGeo_Table_Percentage_pattern = re.compile('<td class=\"num\">(\d+%)</td>',re.S)
        menGeo_Table_Percentage = menGeo_Table_Percentage_pattern.findall(menGeo_TableChoice)

        if len(menGeo_Table_Country) == len(menGeo_Table_Num) and len(menGeo_Table_Country) == len(menGeo_Table_Percentage):
            menGeo_Table_Length = len(menGeo_Table_Country)

            for i in range(0,menGeo_Table_Length):
                menGeo_Table_Dict[ menGeo_Table_Country[i] ] = {"count":menGeo_Table_Num[i],"percentage":menGeo_Table_Percentage[i]}

    return mentionDict,citationDict,readerDict,twGeo_Table_Dict,twDemo_Table_Dict,menGeo_Table_Dict


# get alterMetrics Mendeley Demographic Professional Content
# return menDemo_Table_Pro_Dict
def getAltMetrics_Men_Demo_Pro(altMetricsUrl):
    altMetricsPage_text = requests.get(url=altMetricsUrl, headers=headers, verify=False,timeout=25).text
    altMetricsTree = etree.HTML(altMetricsPage_text)
    pageBs = BeautifulSoup(altMetricsPage_text, 'lxml')

    menDemo_Table_Pro_Dict = {}
    men_Table_Choice_Raw = pageBs.select(".mendeley ")
    if len(men_Table_Choice_Raw) != 0:
        men_Table_Choice_Raw = pageBs.select(".mendeley ")[0]
        menDemo_Table_Pro_Choice = str(men_Table_Choice_Raw.select(" .users > table ")[0])  # Bs 定位第一个图表
        # 定位Demographic内的国家
        menDemo_Table_Country_pattern = re.compile("<td>([^0-9]*)</td>", re.S)
        menDemo_Table_Country_Raw = menDemo_Table_Country_pattern.findall(menDemo_Table_Pro_Choice)
        menDemo_Table_Country = []
        for item in menDemo_Table_Country_Raw:
            item = item.replace("&gt;",">")
            menDemo_Table_Country.append(item)

        menDemo_Table_Num_pattern = re.compile(r'<td class=\"num\">(\d+)</td>', re.S)
        menDemo_Table_Num = menDemo_Table_Num_pattern.findall(menDemo_Table_Pro_Choice)

        menDemo_Table_Percentage_pattern = re.compile('<td class=\"num\">(\d+%)</td>', re.S)
        menDemo_Table_Percentage = menDemo_Table_Percentage_pattern.findall(menDemo_Table_Pro_Choice)

        if len(menDemo_Table_Country) == len(menDemo_Table_Num) and len(menDemo_Table_Country) == len(menDemo_Table_Percentage):
            menDemo_Table_Length = len(menDemo_Table_Country)

            for i in range(0, menDemo_Table_Length):
                menDemo_Table_Pro_Dict[menDemo_Table_Country[i]] = {"count":menDemo_Table_Num[i],"percentage":menDemo_Table_Percentage[i]}
    return menDemo_Table_Pro_Dict


# get alterMetrics Mendeley Demographic Discipline
# return menDemo_Table_Dis_Dict
def getAltMetrics_Men_Demo_Dis(altMetricsUrl):
    altMetricsPage_text = requests.get(url=altMetricsUrl, headers=headers, verify=False).text
    altMetricsTree = etree.HTML(altMetricsPage_text)
    pageBs = BeautifulSoup(altMetricsPage_text, 'lxml')

    menDemo_Table_Dis_Dict = {}
    men_Table_Choice_Raw = pageBs.select(".mendeley ")
    if len(men_Table_Choice_Raw) != 0:
        men_Table_Choice_Raw = pageBs.select(".mendeley ")[0]
        menDemo_Table_Dis_Choice = str(men_Table_Choice_Raw.select(" .users > table ")[1])

        menDemo_Table_Country_pattern = re.compile("<td>([^0-9]*)</td>", re.S)
        menDemo_Table_Country = menDemo_Table_Country_pattern.findall(
            menDemo_Table_Dis_Choice)

        menDemo_Table_Num_pattern = re.compile(r'<td class=\"num\">(\d+)</td>', re.S)
        menDemo_Table_Num = menDemo_Table_Num_pattern.findall(menDemo_Table_Dis_Choice)

        menDemo_Table_Percentage_pattern = re.compile('<td class=\"num\">(\d+%)</td>', re.S)
        menDemo_Table_Percentage = menDemo_Table_Percentage_pattern.findall(menDemo_Table_Dis_Choice)

        if len(menDemo_Table_Country) == len(menDemo_Table_Num) and len(
                menDemo_Table_Country) == len(menDemo_Table_Percentage):
            menDemo_Table_Length = len(menDemo_Table_Country)

            for i in range(0, menDemo_Table_Length):
                menDemo_Table_Dis_Dict[menDemo_Table_Country[i]] = {"count":menDemo_Table_Num[i], "percentage":menDemo_Table_Percentage[i]}
    return menDemo_Table_Dis_Dict


# get Twitter Detail
# return twitterFollow,twFanAverage
def getTwitterFollow(altMetricsUrl):
    twitterFollow = {}
    twFanAverage = 0
    try:
        targetUrl = altMetricsUrl + "/twitter"
        twitter_page_text = requests.get(url=targetUrl,headers=headers,verify=False).text
        twitterTree = etree.HTML(twitter_page_text)

        fansRaw = twitterTree.xpath('//*[@class="post twitter"]//div[@class="follower_count"]/span/text()')
        if len(fansRaw) != 0:

            fanLs = []
            for item in fansRaw:
                item = int(item.replace(",", ""))
                fanLs.append(item)

            nameRaw = twitterTree.xpath('//*[@class="post twitter"]//div[@class="handle"]/text()')
            nameLs = []
            for item in nameRaw:
                item = item.lstrip("@")
                nameLs.append(item)

            timeRaw = twitterTree.xpath('//time/a/text()')
            timeLs = []
            for item in timeRaw:
                timeLs.append(item)

            if len(fanLs) == len(nameLs):
                for i in range(0,len(fanLs)):
                    twitterFollow["tweet "+str(i+1)] = {
                        "nickName":nameLs[i],
                        "followers":fanLs[i],
                        "time":timeLs[i]
                    }

            # calculate twitter fans average
            twFanAverage = int(round(statistics.mean(fanLs),0))
    except:
        twFanAverage = 0

    return twitterFollow,twFanAverage


with open("natureCom_Data(5.1).csv", "a+", newline='', encoding="utf-8_sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "articleUrl","Open Access", "Citation", "CitationDate","Additional Information","Peer review", "Receive Date", "Accept Date", "Publish Date", "Metrics", "MetricsTime", "alMetricsUrl", "tweeterFollowerAverage", "Receive-Accept Time Difference", "Publish-Accept Time Difference", "Publish-Receive Time Difference", "metrics-Publish Time Difference", "citation-Publish Time Difference"])
    contentNum = 1670  # input how many page you want

    wrongLs = []

    artUrlLs = getArtUrl(contentNum)
    print(f"Get {len(artUrlLs)} articles")

    artType_Dict = getArtType()
    artType_json = json.dumps(artType_Dict, indent=4, ensure_ascii=False)
    with open('natureCom_Article_Type.json', 'w', encoding="utf-8") as json_file:
        json_file.write(artType_json)
    print(f"The article classification dictionary is generated")

    for url in artUrlLs:
        try:
            artDict = {}
            artTitle, OpenAccess_csv, citation, citationTime, Peer_Review_csv,receiveDate,acceptDate,publishDate,addInfo = getArtDetail(url)
            metrics, metricsTime, altMetricsUrl = getArtMetrics(url)


            citation_timeCsv = dt.datetime.strptime(citationTime, '%Y-%m-%d').date()
            metrics_timeCsv = dt.datetime.strptime(metricsTime, '%d %b %Y').date()
            Re_Ac_Day = (acceptDate - receiveDate).days
            Pu_Ac_Day = (publishDate - acceptDate).days
            Pu_Re_Day = (publishDate - receiveDate).days
            Me_Pu_Day = (metrics_timeCsv - publishDate).days
            Ci_Pu_Day = (citation_timeCsv - publishDate).days


            if altMetricsUrl != "none":
                mention, citationDict, reader, twitterGeographical_Dict, twitterDemographic_Dict, mendeleyGeographical_Dict = getAltMetrics_Details(altMetricsUrl)
                mendeleyDemographic_Professional_Dict = getAltMetrics_Men_Demo_Pro(altMetricsUrl)
                mendeleyDemographic_Discipline_Dict = getAltMetrics_Men_Demo_Dis(altMetricsUrl)
                twitterFollow, twitterFanAverage = getTwitterFollow(altMetricsUrl)
                print(f"{url} get altMetrics detail successfully")

                artDict[url] = {
                    "title": artTitle,
                    "mention": mention,
                    "citation": citationDict,
                    "reader": reader,
                    "twitterGeographical": twitterGeographical_Dict,
                    "twitterDemographic": twitterDemographic_Dict,
                    "mendeleyGeographical": mendeleyGeographical_Dict,
                    "mendeleyDemographic_Professional": mendeleyDemographic_Professional_Dict,
                    "mendeleyDemographic_Discipline": mendeleyDemographic_Discipline_Dict,
                    "twitterFollow": twitterFollow,
                    "twitterFollow_Average": twitterFanAverage,
                    "scrapyTime": citationTime
                }

                with open('altmetricsTry.txt', 'a+', encoding='utf-8') as f:
                    jsonTest = json.dumps(artDict, ensure_ascii=False, indent=4)
                    jsonTest = jsonTest.lstrip("{")
                    jsonTest = jsonTest.rstrip("}")
                    f.write(jsonTest)
                    f.write(",")
                print("txt finished")

            else:
                twitterFanAverage = 0
                print(f"{url} have no altmetrics")

            writer.writerow([artTitle, url, OpenAccess_csv, citation, citationTime, addInfo, Peer_Review_csv, receiveDate, acceptDate, publishDate,metrics, metricsTime, altMetricsUrl, twitterFanAverage, Re_Ac_Day, Pu_Ac_Day, Pu_Re_Day, Me_Pu_Day,Ci_Pu_Day])

            # Determine whether there are articles that do not belong to any subject classification
            if url not in artType_Dict["Physical sciences"] and url not in artType_Dict["Earth and environmental sciences"] and url not in artType_Dict["Biological sciences"] and url not in artType_Dict["Health sciences"] and url not in artType_Dict["Scientific community and society"]:
                with open("natureCom_type_over_expectations.txt", "a+", encoding="utf-8") as f:
                    f.write(url)
                    f.write('\n')
                    print(f"{url}Do not belong to any discipline，please view these articles in natureCom_type_over_expectations.txt")

            if url in artType_Dict["Physical sciences"]:
                artType_Dict["Physical sciences"].remove(url)
                with open("physical_NatureCom(5.1).csv","a+",newline='', encoding="utf-8_sig") as sub_csvfile:
                    subjectWriter = csv.writer(sub_csvfile)
                    subjectWriter.writerow([artTitle, url, OpenAccess_csv, citation, citationTime, addInfo, Peer_Review_csv, receiveDate, acceptDate, publishDate,metrics, metricsTime, altMetricsUrl, twitterFanAverage, Re_Ac_Day, Pu_Ac_Day, Pu_Re_Day, Me_Pu_Day,Ci_Pu_Day])
            if url in artType_Dict["Earth and environmental sciences"]:
                artType_Dict["Earth and environmental sciences"].remove(url)
                with open("earth_NatureCom(5.1).csv","a+",newline='', encoding="utf-8_sig") as sub_csvfile:
                    subjectWriter = csv.writer(sub_csvfile)
                    subjectWriter.writerow([artTitle, url, OpenAccess_csv, citation, citationTime, addInfo, Peer_Review_csv, receiveDate, acceptDate, publishDate,metrics, metricsTime, altMetricsUrl, twitterFanAverage, Re_Ac_Day, Pu_Ac_Day, Pu_Re_Day, Me_Pu_Day,Ci_Pu_Day])
            if url in artType_Dict["Biological sciences"]:
                artType_Dict["Biological sciences"].remove(url)
                with open("biological_NatureCom(5.1).csv","a+",newline='', encoding="utf-8_sig") as sub_csvfile:
                    subjectWriter = csv.writer(sub_csvfile)
                    subjectWriter.writerow([artTitle, url, OpenAccess_csv, citation, citationTime, addInfo, Peer_Review_csv, receiveDate, acceptDate, publishDate,metrics, metricsTime, altMetricsUrl, twitterFanAverage, Re_Ac_Day, Pu_Ac_Day, Pu_Re_Day, Me_Pu_Day,Ci_Pu_Day])
            if url in artType_Dict["Health sciences"]:
                artType_Dict["Health sciences"].remove(url)
                with open("health_NatureCom(5.1).csv","a+",newline='', encoding="utf-8_sig") as sub_csvfile:
                    subjectWriter = csv.writer(sub_csvfile)
                    subjectWriter.writerow([artTitle, url, OpenAccess_csv, citation, citationTime, addInfo, Peer_Review_csv, receiveDate, acceptDate, publishDate,metrics, metricsTime, altMetricsUrl, twitterFanAverage, Re_Ac_Day, Pu_Ac_Day, Pu_Re_Day, Me_Pu_Day,Ci_Pu_Day])
            if url in artType_Dict["Scientific community and society"]:
                artType_Dict["Scientific community and society"].remove(url)
                with open("scientific_NatureCom(5.1).csv","a+",newline='', encoding="utf-8_sig") as sub_csvfile:
                    subjectWriter = csv.writer(sub_csvfile)
                    subjectWriter.writerow([artTitle, url, OpenAccess_csv, citation, citationTime, addInfo, Peer_Review_csv, receiveDate, acceptDate, publishDate,metrics, metricsTime, altMetricsUrl, twitterFanAverage, Re_Ac_Day, Pu_Ac_Day, Pu_Re_Day, Me_Pu_Day,Ci_Pu_Day])

        except:
            print(f"{url} failed to access")
            wrongLs.append(url)
            with open("natureCom_wrong.txt", "a+", encoding="utf-8") as f:
                f.write(url)
                f.write('\n')
            print("The error message has been written, please check")
    # json_str = json.dumps(artDict, indent=4, ensure_ascii=False)
    # with open('natureCom_Metrics.json', 'a+', encoding="utf-8") as json_file:
    #     json_file.write(json_str)
        
    with open("natureCom_wrongFinal.txt", "a+", encoding="utf-8") as f:
        for url in wrongLs:
            f.write(url)
            f.write('\n')
        print(f"A total of {len(wrongLs)} pages have a problem with the URL, check the URL in natureCom_wrongFinal.txt")

    print("Finish the project!")
