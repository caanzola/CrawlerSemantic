import urllib.request
import urllib.parse
import json
import pprint
import csv

class CoreApiRequestor:

    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint
        self.api_key = api_key
        #defaults
        self.pagesize = 100
        self.page = 1
        url = self.get_method_query_request_url('/articles/search', 'deep AND learning', False, 1)
        #url = self.get_up_to_20_pages_of_query('/articles/search', 'deep AND learning', False)
        result = self.request_url(url)

    def parse_response(self, decoded):
        res = []
        for item in decoded['data']:
            doi = None
            if 'identifiers' in item:
                for identifier in item['identifiers']:
                    if identifier and identifier.startswith('doi:'):
                        doi = identifier
                        break
            res.append([item['title'], doi])

        print("res ...............")
        print(res)
        print("res ...............")
        return res

    def request_url(self, url):
        with urllib.request.urlopen(url) as response:
            html = response.read()

        s = str(html, encoding = 'utf-8')
        print(s)

        arr = s.split('{"id":"')
        arr2 = {}
        i = 0
        j = 0
        while i < arr.__len__(): 
            if i % 2 == 1:
                print()
                a = arr[i]+arr[i+1]
                print(a)
                print()
                arr2[j] = a
                j=j+1
            i=i+1
        
        columnas = {}
        valores = {}
        l = 0
        for x in arr2:
                print()
                cad = arr2[x]
                arr3 = cad.split(":")
                for q in arr3:
                    print(q)
                    arr4 = q.split(",")
                    if arr4.__len__()>1:
                        columnas[l]= arr4[arr4.__len__()-1]
                        valores[l] = arr4[0]
                        if columnas[l]=='"repositories"':
                            columnas[l]='idRepo'
                            print('CAMBIOO')
                            print(columnas[l])
                            print(l)
                        l=l+1
                    if arr4.__len__()==0:
                        if arr4[0]=='{"pdfStatus"':
                            columnas[l] = 'pdfStatus'
                            l=l+1
                    #employee_writer.writerow([q])
                    print()

        c1 = "id"+","+columnas[0].split('"')[1] + ","+columnas[1].split('"')[1]+","+columnas[2].split('"')[1]+","+columnas[3].split('"')[1]+","+columnas[4].split('"')[1]+","+columnas[5].split('"')[1]+","+columnas[6]+","+columnas[7].split('"')[1]+","+columnas[8].split('"')[1]
        c2 = c1+ ","+columnas[9].split('"')[1]+ "," +columnas[10].split('"')[1]+ "," +columnas[11].split('"')[1]+ "," +columnas[12].split('"')[1]+ "," +columnas[13].split('"')[1]+ "," +columnas[14].split('"')[1]+ "," +columnas[15].split('"')[1]+ "," +columnas[16].split('"')[1]+ "," +columnas[17].split('"')[1]
        c3 = c2 + ","+columnas[18].split('"')[1]+ ","+columnas[19].split('"')[1]+ ","+columnas[20].split('"')[1]+ ","+columnas[21].split('"')[1]+ ","+columnas[22].split('"')[1]+ ","+columnas[23].split('"')[1]+ ","+columnas[24].split('"')[1]+ ","+columnas[25].split('"')[1]
        c4 = c3  + ","+columnas[26].split('"')[1]+ ","+columnas[27].split('"')[1]+ ","+columnas[28].split('"')[1]+ ","+columnas[29].split('"')[1]+ ","+columnas[30].split('"')[1]+ ","+columnas[31].split('"')[1]+ ","+columnas[32].split('"')[1]+ ","+columnas[33].split('"')[1]+ ","+columnas[34].split('"')[1]+ ","+columnas[35].split('"')[1]

        d1 = ''
        h = 0
        for f in valores:
            if f == 0:
                d1 = valores[f]
            else:
                d1 = d1+","+valores[f]
            if f % 36 == 0:
                d1 = d1+ "?"

        arr6 = d1.split("?")

        with open('csv_CoreCrawler.csv', mode='w') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)            
            employee_writer.writerow([c4])
            for g in arr6:
                employee_writer.writerow([g])
            

        #with open('x.json','w') as fp:
         #   json.dump(s,fp)

        #outfile = open('resutl.csv','w')
        #inputFile = open('x.json','r')
        
        #writer = csv.writer(outfile)
        #for row in json.loads(inputFile):
         #   writer.writerow(row)

        print('html.......')
        return html

    def get_method_query_request_url(self,method,query,fullText,page):
        if (fullText):
            fullText = 'true'
        else:
            fullText = 'false'
        params = {
            'apiKey':self.api_key,
            'page':page,
            'pageSize':self.pagesize,
            'fulltext':fullText
        }
        print('get_method_query_request_url...........')
        print(self.endpoint + method + '/' + urllib.parse.quote(query) + '?' + urllib.parse.urlencode(params))
        print()
        return self.endpoint + method + '/' + urllib.parse.quote(query) + '?' + urllib.parse.urlencode(params)

    def get_up_to_20_pages_of_query(self,method,query,fulltext):
        url = self.get_method_query_request_url(method,query,fulltext,1)
        all_articles=[]
        resp = self.request_url(url)
        result = json.loads(resp.decode('utf-8'))
        all_articles.append(result)
        if (result['totalHits']>100):
            numOfPages = int(result['totalHits']/self.pagesize)  #rounds down
            if (numOfPages>20):
                numOfPages=20
            for i in range(2,numOfPages):
                url = self.get_method_query_request_url(method,query,False,i)
                print(url)
                resp =self.request_url(url)
                all_articles.append(json.loads(resp.decode('utf-8')))
        print('all articles........')
        print(all_articles)
        print('all articles........')
        return all_articles


x = CoreApiRequestor('https://core.ac.uk/api-v2', 'Here the API key')