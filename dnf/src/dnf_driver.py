from configs.config import CHROME_DRIVER_PATH, CHROME_PATH, CHROME_DRIVER_DOWNLOAD_URL
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib import parse
import time
import pandas as pd
import os
import subprocess
import requests
import zipfile
import re

class DNF_DRIVER:
    
    """
    ### Summary
        - 던전앤파이터 공식 홈페이지 크롤링을 요청하는 클래스입니다.
        
    ### Method
        - initialize_driver : 공식 홈페이지 명성 검색창 실행
        - select_job : 명성 검색 창 내 드랍다운 박스 직업 선택
        - search : 명성 입력 후 검색
        - scrape : 검색 결과 HTML 스크랩
        - processing : 파싱한 데이터 전처리
        - crawling : 하나의 메서드로 통합하여 크롤링
    """
    
    def __init__(self):
        self.url = 'https://df.nexon.com/world/fame'
    
    def version_check(self):

        """
        ### Summary
            - 크롬 드라이버 버전 체크 함수
        """
        
        pattern = re.compile(r'^\d+\.\d+\.\d+\.\d+$')

        # step 1 : CHROME_PATH 버전 확인하기
        chrome_info = os.listdir(os.path.join(CHROME_PATH,'Application'))

        # step 2 : CHROME_PATH 버전 확인하기
        result = subprocess.run([os.path.join(CHROME_DRIVER_PATH,'chromedriver.exe'), '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        chrome_driver_info = result.stdout.strip().split()

        # step 3 : 버전 추출
        chrome_versions = [files.split('.') for files in chrome_info if pattern.match(files)][0]
        chrome_driver_versions = [files.split('.') for files in chrome_driver_info if pattern.match(files)][0]
        chrome_version, chrome_driver_version = chrome_versions[0], chrome_driver_versions[0]

        # step 4 : 업데이트
        if chrome_version != chrome_driver_version:

            response = requests.get(CHROME_DRIVER_DOWNLOAD_URL)
            if response.status_code == 200:
                data = response.json()

                download_url = data['milestones'][chrome_version]['downloads']['chromedriver'][-1]['url']

                # step 5: 드라이버 다운로드 및 덮어쓰기
                if download_url:
                    download_path = os.path.join(os.path.expanduser("~"), 'Downloads', 'chromedriver.zip')
                    with requests.get(download_url, stream=True) as r:
                        with open(download_path, 'wb') as f:
                            f.write(r.content)

                    # 압축 풀기
                    with zipfile.ZipFile(download_path, 'r') as zip_ref:
                        zip_ref.extractall("C:\\")

                    print(f"Chromedriver updated : {chrome_driver_version} -> {chrome_version}")
    
    def initialize_driver(self):
        
        """
        ### Summary
            - 크롬 드라이버 실행 함수
        """
        
        # 1. 버전에 맞는 크롬 드라이버를 다운로드 후, 경로 지정
        chrome_driver_path = os.path.join(CHROME_DRIVER_PATH,'chromedriver.exe')
        
        # 2. 크롬 드라이버 실행 시, 경로에 접근해서 버전에 맞는 드라이버 선택
        service = ChromeService(executable_path=chrome_driver_path)
        
        # 3. 크롬 드라이버 실행
        self.driver = webdriver.Chrome(service=service)
        
        # 4. 크롬 드라이버 실행
        self.driver.get(self.url)
    
    def select_job(self, job_code: str):
        
        """
        ### Summary
            - 페이지 내 드랍다운 영역에서 요청받은 직업을 선택합니다.
            
        ### Args:
            - job_code (str): 직업 코드를 통해 페이지 내 직업을 선택합니다.
        """ 
        
        # 1. 직업 드롭박스 선택 후 클릭 (active 상태)
        self.driver.find_element(By.ID, 'fameSelectedJob').click()
        
        # 2. 직업 코드에 해당하는 드랍박스를 찾기
        job_element = self.driver.find_element(By.XPATH, f"//a[@data-id='{job_code}']")
        
        # 3. 직업 선택
        job_element.click()

    def search(self, fame: int):
        
        """
        ### Summary
            - 페이지 내 최대 명성 입력란에 명성을 입력 후 검색합니다.
        
        ### Args:
            - fame (int): 최대 명성 입력란에 입력할 명성값입니다.
        """
            
        # 1. 검색 창 명성 범위 입력
        input_field = self.driver.find_element(By.ID, 'fame2')
        input_field.clear()
        input_field.send_keys(fame)
        input_field = self.driver.find_element(By.ID, 'fame1')
        input_field.click() 
        
        # 2. 검색 버튼 클릭
        search = self.driver.find_element(By.ID, 'fameSearchBtn')
        search.click()

    def scrape(self):
        
        """
        ### Summary
            - 직업, 명성 범위의 검색 결과를 수집합니다.
        
        ### Returns:
            - characters (list) : 수집한 paragraph들을 반환합니다.
            
        ### Example
            >>> scrape()
                <dl class="">
                    <dt class="searchedCharacter" 
                        data-ch="6ff5c87f4c14667bf97b8dc01a4ba796" 
                        data-nm="*JackFrost*" 
                        data-sv="casillas" 
                        data-svk="카시야스">
                        <img class="lazy" data-src="https://avatar.df.nexon.com/charac/casillas/6ff5c87f4c14667bf97b8dc01a4ba796/stand@2x.png"/>
                    </dt>
                    <dd>
                        <p class="lv">Lv.110</p>
                        <p class="name" data-ch="6ff5c87f4c14667bf97b8dc01a4ba796" data-characname="*JackFrost*" data-svn="5">*JackFrost*</p>
                        <p class="job">眞 빙결사<i></i>카시야스</p>
                        <p class="fame">67,763</p>
                    </dd>
                </dl>

            """        

        # 1. 현재 드라이버의 HTML 불러오기
        html = self.driver.page_source
        time.sleep(1)

        # 2. 현재 HTML 파싱
        soup = BeautifulSoup(html, 'html.parser')
        
        # 3. 캐릭터 결과 불러오기
        article = soup.find('article', class_='charsrch_result')
        
        # 4. 최대 200개의 결과 데이터 캐릭터 별로 파싱하기
        characters = article.find_all('dl')
        return characters
    
    def processing(self, characters: list, job_group: str, job_name_fixed: str):
        
        """
        ### Summary
            - 수집한 데이터들을 전처리합니다.
        
        ### Returns:
            - datas (list) : 캐릭터 데이터들을 전처리하여 반환합니다.
            - fame (int) : 검색 결과 중 가장 낮은 명성을 반환합니다.
        """        
        datas = []
        for character in characters:
            
            # 서버영문, 서버한글, 서버숫자
            sv_eng = character.dt['data-sv'] # cain
            sv_kor = character.dt['data-svk'] # 카인
            
            # 캐릭터 이미지 코드, 캐릭터 이름, 직업명
            cha_img_code = character.dt['data-ch']
            char_name = character.dt['data-nm']
            job_name = character.find('p', class_='job').get_text(strip=True)       
            
            # 명성, 레벨
            lv = character.find('p', class_='lv').get_text(strip=True)
            fame = character.find('p', class_='fame').get_text(strip=True)
            fame = int(fame.replace(",", ""))

            # 딕셔너리로 변경
            row = {'sv_kor': sv_kor,
                   'sv_eng': sv_eng,
                   'char_name': char_name,
                   'char_name_encoded': parse.quote(char_name),
                   'char_img': cha_img_code,
                   'job_group' : job_group,
                   'job_name': job_name_fixed,
                   'lv': int(lv[3:]),
                   'fame': fame}
                # * 진각성을 하지 않고 만렙을 달성한 캐릭터들 다수 존재.
                # job_name': job_name[:-len(sv_kor)].lstrip('眞 '),
            datas.append(row)

        return datas,fame
    
    def crawling(self, job_group: str, job_name: str, job_code:str,
                 min_fame: int, max_fame: int):
        
        """
        ### Summary
            - 검색 직업의 특정 명성 구간 캐릭터 정보들을 크롤링합니다.
        
        ### Args
            - job_group (str): 검색할 직업군
            - job_name (str): 직업
            - job_code (str): 직업코드는 (DB에서 확인)1
            - min_fame (int): 검색할 최소 입력
            - max_fame (int): 검색할 최대 명성

        ### Returns
            - pd.DataFrame : 크롤링한 캐릭터들의 정보를 데이터프레임으로 반환합니다.
        
        ### Example
            >>> crawling('마법사(남)','빙결사','8_2',66480,'66480')
            pd.DataFrame({
                'sv_kor': ['프레이', '프레이'],
                'sv_eng': ['prey', 'prey'],
                'char_img': ['949c8fb4d6ce7f8222af345a43319bdf', '33629349c99201710fef769d10f631f0'],
                'char_name': ['일로시움', 'Nine'],
                'job_name': ['빙결사', '빙결사'],
                'lv': [110, 110],
                'fame': [66499, 66480]}])
                
        """        
        
        # * 웹드라이버 실행
        dnf = DNF_DRIVER()
        dnf.version_check()
        dnf.initialize_driver()
        dnf.select_job(job_code)

        result = []
        fame = max_fame
        while True:
            dnf.search(fame)  # 최대 명성 자리에 명성 입력하게
            characters = dnf.scrape()  # HTML 스크랩
            
            if not characters: # 첫 루프에서 캐릭터 정보를 찾지 못했을 경우
                fame -= 2000
                continue
            
            # 가장 마지막으로 찾은 캐릭터 명성으로 명성구간 좁히기
            datas, fame = dnf.processing(characters, job_group, job_name) # 데이터 파싱
            result.extend(datas)
            
            if fame < min_fame :
                break
            
        # 구간 좁히면서 발생한 중복 데이터들 제거
        df = pd.DataFrame(result)
        df = df.astype({
                        'sv_kor': 'string',
                        'sv_eng': 'string',
                        'char_name': 'string',
                        'char_name_encoded': 'string',
                        'char_img': 'string',
                        'job_group' : 'string',
                        'job_name': 'string',
                        'lv': 'int',
                        'fame': 'int'
                        })

        df = df[df['fame']>=min_fame].drop_duplicates(subset=['sv_eng','char_name'], keep='first')
        print(f'{job_group} : {job_name} 크롤링 완료')
        return df