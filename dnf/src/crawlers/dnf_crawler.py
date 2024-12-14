import requests

class DNF_crawler:

    """
    ### Summary
        - 던전앤파이터 공식 홈페이지 크롤러
    """
        
    def __init__(self):
        
        """
        ### Summary
            - 크롤링에 필요한 url, headers, params 초기화
        """
        
        self.base_url = 'https://df.nexon.com/world/fame/fetch'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Whale/3.28.266.14 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://df.nexon.com/world/fame',
            'Origin': 'https://df.nexon.com'
        }

        self.default_params = {
            'characJob': 99,
            'growType': 99,
            'fame1': None,
            'fame2': None,
            'buffer': 'true',
            'dealer': 'true'
        }

    def crawling(self, params=None):
        
        """
        ### Summary
            - 던전앤파이터 공식 홈페이지 크롤링 함수
        
        ### Arguments
            - params (dict, optional): API 요청 파라미터. Defaults to None.
                - characJob (int): 직업군 코드 (0-16, 99=전체)
                - growType (int): 직업 코드 (0-5, 99=전체)
                - fame1 (int, optional): 최소 명성치
                - fame2 (int, optional): 최대 명성치
                - buffer (str): 버퍼 여부 ('true'/'false')
                - dealer (str): 딜러 여부 ('true'/'false')
        
        ### Returns
            - Response Type:
                message: str
                success: int
                body: List[Dict[str, Any]]
                    - characterId: str     # 캐릭터 ID
                    - characterName: str   # 캐릭터 이름
                    - level: int          # 레벨
                    - jobGrowName: str    # 전직 이름
                    - serverNo: int       # 서버 번호
                    - serverName: str     # 서버 영문명
                    - serverNameKor: str  # 서버 한글명
                    - fame: str          # 명성치
                    - lounge6BG: int     # 라운지 배경
        
        ### Example
        >>>  [{'characterId': '캐릭터 고유 id',
            'characterName': '캐릭터 닉네임',
            'fame': '명성',
            'jobGrowName': '眞 웨펀마스터',
            'level': 레벨,
            'lounge6BG': False,
            'serverName': '서버 영문',
            'serverNameKor': '서버 한글',
            'serverNo': 서버 넘버}]
        """

        if params is None:
            params = self.default_params

        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"요청 실패: {e}")
            return None