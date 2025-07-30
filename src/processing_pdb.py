from dataclasses import dataclass, asdict
from typing import List
import requests
from bs4 import BeautifulSoup
import gzip
import io
import json
import threading
import queue


base_url = 'https://files.wwpdb.org/pub/pdb/data/structures/all/pdb/'

@dataclass
class RelevantDate:
    date:str
    dateType:str
    
    def to_dict(self):
        return asdict(self)

        

@dataclass
class PDB:
    pdb:str
    title:str
    authors:List[str]
    doi:str
    pmid:str
    date:str
    revDate:str = List[RelevantDate]
    
    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict())
    
    
    
    

def get_first_page():
    response = requests.get(base_url)
    with open('index.html', 'w') as f:
        f.write(response.text)


def extract_list_download():
    html_content =open("index.html").read()
    soup = BeautifulSoup(html_content, 'lxml')
    links = soup.find_all('a')
    for link in links:
        data = link.get('href')
        if data.endswith('.ent.gz'):
            yield data


def download_file(url):
    response = requests.get(url)
    print(f"Downloading {url}")
    with gzip.open(io.BytesIO(response.content), 'rt') as f:
        return extract_info(f)
        
  
def worker(q, idx):
    with gzip.open(f"{idx}.gz", 'wb') as f:
        while True:
            url = q.get()
            if url is None:
                break
            pdb = download_file(url)
            f.write(pdb.to_json().encode("utf-8"))
            f.write("\n".encode("utf-8"))
            f.flush()
            q.task_done()      

def extract_info(f):
    title = []
    date = None
    pdb = None
    authors =[]
    doi = None
    pmid =None
    relevantDates = []
   
    for line in f:
        if line.startswith('HEADER'):
            d = line.strip().split()
            pdb = d[-1]
            date = d[-2]
        elif line.startswith('TITLE'):
            title.append(line.strip()[10:].strip())
        elif line.startswith('AUTHOR'):
            authors = line[6:].strip().split(',')
        elif line.startswith('JRNL'):
            if 'DOI' in line:
                doi = line[19:].strip()
            if 'PMID' in line:
                pmid = line[19:].strip()
        elif line.startswith('REVDAT'):
            d = line[10:].strip().split()
            relevantDates.append(RelevantDate(date=d[0],dateType= d[-1]))
        elif line.startswith('REMARK'):
            return PDB(pdb, " ".join(title), authors, doi, pmid, date, relevantDates)



if __name__ == '__main__':
    q = queue.Queue()
    num_threads = 10

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(q,i,))
        t.start()
        threads.append(t)

    # get_first_page()
    print("Extracting list of download links")
    for item in extract_list_download():
        q.put(f"{base_url}{item}")

    q.join()

    for i in range(num_threads):
        q.put(None)
    for t in threads:
        t.join()

    # get_first_page()
    # print("Extracting list of download links")
    # for item in extract_list_download():
    #     download_file(f"{base_url}{item}")
    #     break