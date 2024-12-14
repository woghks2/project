# src/api_clients/neople_api_client.py

from datetime import datetime, timedelta
from PIL import Image
from io import BytesIO
import pandas as pd
import requests
import pprint

class DNF_API:
    
    """
    ### Summary
        - 던전앤파이터 API와 관련된 요청을 수행하는 클래스입니다.
        - 한글, 특수문자 등 데이터를 입력하는 경우 인코딩 후 사용하는 것을 권장합니다.
        - # ! https://developers.neople.co.kr/contents/apiDocs/df

    ### Args
        - api_key (str) : 네오플에서 발급받은 API Key로, API 요청 시 사용됩니다.
        
    ### Method
        - find_error : response 결과를 반환합니다.
        - character_search : 캐릭터를 검색합니다.
        - get_character_img : 캐릭터의 이미지 정보를 요청합니다.
        - get_creature : 캐릭터의 크리쳐 데이터를 요청합니다.
        - get_equipment : 캐릭터의 장비 데이터를 요청합니다.
        - get_timeline : 캐릭터의 타임라인 로그 데이터를 요청합니다.
        - get_server : DB 업데이트 후 사용하지 않습니다.
        - job_dfs : DB 업데이트 후 사용하지 않습니다.
        - get_jobs : DB 업데이트 후 사용하지 않습니다.
    """     
    
    # -> 각 API KEY 별로 부하를 낮추기 위해 고정 API KEY 대신 여러개의 API KEY 사용
    def __init__(self, api_key):
        self.api_key = api_key

    # error에 맞는 메세지 출력
    def find_error(self, response):
        error_codes = {
            200: ("정상적인 응답", "정상적인 응답입니다."),
            400: ("요청에 대한 유효성 검증 실패 또는 필수 파라미터 에러", "요청에 대한 유효성 검증 실패 또는 필수 파라미터 에러입니다."),
            401: ("인증 오류", "인증 오류가 발생했습니다."),
            404: ("존재하지 않은 리소스 또는 페이지", "존재하지 않은 리소스 또는 페이지입니다."),
            500: ("시스템 오류", "시스템 오류가 발생했습니다."),
            503: ("시스템 점검", "시스템 점검 중입니다.")
        }

        common_errors = {
            "API000": ("API Key 미입력", "API Key가 입력되지 않았습니다."),
            "API001": ("유효하지 않은 게임아이디", "유효하지 않은 게임아이디입니다."),
            "API002": ("API Key 사용량 초과", "API Key의 사용량이 초과되었습니다."),
            "API003": ("유효하지 않은 API Key", "유효하지 않은 API Key입니다."),
            "API004": ("차단된 API Key", "차단된 API Key입니다."),
            "API005": ("해당 게임으로 발급되지 않은 API Key", "해당 게임으로 발급되지 않은 API Key입니다."),
            "API006": ("유효하지 않은 HTTP 헤더 요청", "유효하지 않은 HTTP 헤더 요청입니다."),
            "API007": ("클라이언트 소켓 통신 오류", "클라이언트 소켓 통신 오류가 발생했습니다."),
            "API900": ("유효하지 않은 URL", "유효하지 않은 URL입니다."),
            "API901": ("유효하지 않은 요청 파라미터", "유효하지 않은 요청 파라미터입니다."),
            "API999": ("시스템 오류", "시스템 오류가 발생했습니다.")
        }

        dnf_errors = {
            "DNF000": ("유효하지 않은 서버아이디", "유효하지 않은 서버아이디입니다."),
            "DNF001": ("유효하지 않은 캐릭터 정보", "유효하지 않은 캐릭터 정보입니다."),
            "DNF003": ("유효하지 않은 아이템 정보", "유효하지 않은 아이템 정보입니다."),
            "DNF004": ("유효하지 않은 경매장 및 아바타마켓 상품 정보", "유효하지 않은 경매장 및 아바타마켓 상품 정보입니다."),
            "DNF005": ("유효하지 않은 스킬 정보", "유효하지 않은 스킬 정보입니다."),
            "DNF006": ("타임라인 검색 시간 파라미터 오류", "타임라인 검색 시간 파라미터 오류가 발생했습니다."),
            "DNF007": ("경매장 아이템 검색 갯수 제한", "경매장 아이템 검색 갯수 제한이 초과되었습니다."),
            "DNF008": ("다중 아이템 검색 갯수 제한", "다중 아이템 검색 갯수 제한이 초과되었습니다."),
            "DNF009": ("아바타 마켓 타이틀 검색 갯수 제한", "아바타 마켓 타이틀 검색 갯수 제한이 초과되었습니다."),
            "DNF900": ("유효하지 않은 URL", "유효하지 않은 URL입니다."),
            "DNF901": ("유효하지 않은 요청 파라미터", "유효하지 않은 요청 파라미터입니다."),
            "DNF980": ("시스템 점검", "시스템 점검 중입니다."),
            "DNF999": ("시스템 오류", "시스템 오류가 발생했습니다.")
        }

        status_code = response.status_code
        error_code = response.json().get("code")

        if status_code in error_codes:
            return error_codes[status_code]
        elif error_code in common_errors:
            return common_errors[error_code]
        elif error_code in dnf_errors:
            return dnf_errors[error_code]
        else:
            return ("알 수 없는 오류", "알 수 없는 오류가 발생했습니다.")

    def get_server(self, print_flag=False):
        
        """
        DB에 서버 정보 업데이트 후 사용하지 않습니다.
        """        
        
        url = f'https://api.neople.co.kr/df/servers?apikey={self.api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            server_info = response.json()

            if print_flag:
                pprint.pprint(server_info)
            return pd.DataFrame(server_info['rows'])

    def character_search(self, serverId, characterName, jobId='', jobGrowId='', isAllJobGrow=False, wordType='match', limit=10, print_flag=False):
        
        """
        ### Summary:
            - 던전앤파이터 캐릭터를 검색합니다.
        
        ### Args:
            - serverId (str) : 서버명 (ex: cain, all)
            - characterName (str) : 캐릭터명
            
        ### Returns:
            - df_character_info (pd.DataFrame) : 검색한 캐릭터 정보를 반환합니다.
        """        
        
        url = f'https://api.neople.co.kr/df/servers/{serverId}/characters?characterName={characterName}&jobId={jobId}&jobGrowId={jobGrowId}&isAllJobGrow={isAllJobGrow}&limit={limit}&wordType={wordType}&apikey={self.api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            character_info = response.json()
            df_character_info = pd.DataFrame(character_info['rows'])
            if print_flag:
                pprint.pprint(df_character_info)
            return df_character_info

    def character_img(self, serverId, characterId, imgSize=2):
        
        """
        ### Summary
            - 던전앤파이터 캐릭터의 이미지를 반환합니다.

        ### Args
            - serverId (str) : 서버명 (ex: cain, all)
            - characterId (str): 캐릭터 고유 코드
            - print_flag (bool, optional): 결과 출력 유무

        ### Returns
            - img (PIL.Image) : 검색한 캐릭터의 이미지를 반환합니다.
        """
        
        url = f'https://img-api.neople.co.kr/df/servers/{serverId}/characters/{characterId}?zoom={imgSize}'
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            return img

    def timeline(self, serverId, characterId, 
                 startDate=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M'),
                 endDate=datetime.now().strftime('%Y-%m-%d %H:%M'),
                 limit=10, code='', next='', print_flag=False):
        """
        ### Summary
            - 요청한 캐릭터의 타임라인을 반환합니다.
            
        ### Args
            - serverId (str): 서버명 (ex: cain, all)
            - characterId (str): 캐릭터 고유 코드
            - startDate (str): 시작 날짜를 지정합니다. ex) 2024-08-01 12:00
            - endDate (str): 마지막 날짜를 지정합니다. ex) 2024-08-02 12:00
                - 기간 설정은 최대 90일까지 가능합니다.
            - limit (int, optional): 가져올 타임라인 데이터 수를 지정합니다. (Defaults to 10)
            - code (str, optional): 요청할 타임라인 정보를 작성합니다. (ex: 101,102,103 다중 입력이 가능합니다 sep = ',')
                - https://developers.neople.co.kr/contents/guide/pages/all#%EB%8D%98%ED%8C%8C-%ED%83%80%EC%9E%84%EB%9D%BC%EC%9D%B8-%EC%BD%94%EB%93%9C
                - DB 내 timeline_code 테이블에서도 확인할 수 있습니다.
            - next (str, optional): ? (Defaults to ''.)
            - print_flag (bool, optional): 출력 유무를 결정합니다. (Defaults to False.)

        Returns:
            timeline_info: 타임라인 정보를 반환합니다.
        """ 
               
        url = f'https://api.neople.co.kr/df/servers/{serverId}/characters/{characterId}/timeline?limit={limit}&code={code}&startDate={startDate}&endDate={endDate}&next={next}&apikey={self.api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            timeline_info = response.json()
            if print_flag:
                pprint.pprint(timeline_info)
            return timeline_info

    def equipment(self, serverId, characterId, print_flag=False):
        
        """
        ### Summary
            - 캐릭터가 장착한 장비 정보를 반환합니다.
        
        ### Args
            - serverId (str) : 서버명 (ex: cain, all)
            - characterId (str) : 캐릭터 고유 코드
            - print_flag (bool, optional): 결과 출력 유무

        ### Returns:
            equip_info (json): 캐릭터가 장착한 장비 정보를 반환합니다.
        """
        
        url = f'https://api.neople.co.kr/df/servers/{serverId}/characters/{characterId}/equip/equipment?apikey={self.api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            equip_info = response.json()
            if print_flag:
                pprint.pprint(equip_info)
            return equip_info
        
    def creature(self, serverId: str, characterId: str, print_flag=False):
        
        """
        ### Summary
            - 캐릭터가 장착한 크리처 정보를 반환합니다.

        ### Args
            - serverId (str) : 서버명 (ex: cain, all)
            - characterId (str) : 캐릭터 고유 코드
            - print_flag (bool, optional): 결과 출력 유무

        Returns:
            creature_info (json) : 캐릭터가 장착한 크리처 정보를 반환합니다.
        """        
        
        url = f'https://api.neople.co.kr/df/servers/{serverId}/characters/{characterId}/skill/buff/equip/creature?apikey={self.api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            creature_info = response.json()
            if print_flag:
                pprint.pprint(creature_info)
            return creature_info