import requests

class DUNDAM_crawler:
    
    """
    ### Summary
        - 던담 크롤러
    """
    
    def __init__(self):
        self.dealer_base_url = 'https://dundam.xyz/dat/dealerRankingData.jsp'
        self.buffer_base_url = 'https://dundam.xyz/dat/bufferRankingData.jsp'
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Whale/3.28.266.14 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Origin': 'https://dundam.xyz',
            'Referer': 'https://dundam.xyz/damage_ranking'
        }
        
        self.default_dealer_params = {
            'page': 1,
            'type': 8,
            'job': '眞 웨펀마스터',
            'baseJob': '귀검사(남)',
            'weaponType': '전체',
            'weaponDetail': '전체'
        }

        self.default_buffer_params = {
            'page': 1,
            'job': 1,
            'type': 1,
            'favor': 1
        }
        
    def dealer_crawling(self, params=None):
        """
        ### Summary
            - 던담 딜러 정보 크롤링
        
        ### Arguments
            - params (dict, optional): API 요청 파라미터. Defaults to None.
                - page (int): 페이지 번호
                - type (int): 타입 코드 (8=고정)
                - job (str): 각성 직업명 (예: '眞 웨펀마스터')
                - baseJob (str): 기본 직업명 (예: '귀검사(남)')
                - weaponType (str): 무기 타입 ('전체' 또는 특정 무기)
                - weaponDetail (str): 상세 무기 타입 ('전체' 또는 특정 무기)
        
        ### Returns
            - dict or None: 
                - ranking (list): 캐릭터 랭킹 정보 리스트
                    - nick (str): 캐릭터명
                    - server (str): 서버명
                    - damage (str): 딜량
                    - weapon (str): 무기명
                    - rank (int): 순위
                    - fame (int): 명성
                    - key (str): 캐릭터 고유 id
        """

        if params is None:
            params = self.default_dealer_params
            
        try:
            response = requests.post(
                self.dealer_base_url,
                params=params,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"요청 실패: {e}")
            return None
        
    def buffer_crawling(self, params=None):
        """
        ### Summary
            - 던담 버퍼 정보 크롤링
        
        ### Arguments
            - params (dict, optional): API 요청 파라미터. Defaults to None.
                - page (int): 페이지 번호
                - job (str): 1~5 (전체 / 여크루 / 남크루 / 인챈 / 뮤즈)
                - type (str): 1~3 (스탯 / 버프력 / 점수)
                - favor (str): 1~2 (편애 / 노편애)
        
        ### Returns
            - dict or None:
                - ranking (list): 캐릭터 랭킹 정보 리스트
                    - nick (str): 캐릭터명
                    - server (str): 서버명
                    - score (str): 버프력
                    - stat (str): 스탯
                    - attack (str): 공격력
                    - rank (int): 순위
                    - fame (int): 명성
                    - key (str): 캐릭터 고유 id
        """
        
        if params is None:
            params = self.default_buffer_params
            
        try:
            response = requests.post(
                self.buffer_base_url,
                params=params,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"요청 실패: {e}")
            return None