1. 
    python -m venv venv  
    venv/Scripts/activate.bat  
    pip install -r requirements.txt

2.  블로그들의 포스팅을 한눈에 모아서 보여주는 허브 사이트, TIL(Today I Learend) Card 형태로 링크를 등록  
    Slack과 연동하여 해당 포스팅 유저와 1:1 질문 상담 가능 (워크 스페이스)  
    카드 위 질문하기 버튼를 누르면 Slack Bot이 DM을 생성함  
    카드 위 대화수집 버튼을 누르면 Slack Bot에서 1:1방의 대화 내용을 받아와서 CRUD 게시판에 등록( 비공개 가능 )  
    받은 좋아요로 베스트 TIL 나열  
    마이 페이지에서 현재까지 받은 좋아요 수와 작성한 TIL 카드 수와 활동 일자를 볼 수 있음  
    회원 가입 시 메일 발송  
    슬랙 워크스페이스 초대 시 Slack userID를 DB에 수집 및 사용하여 DM 생성
    
    &nbsp;
    
    #Login Page  
    <img width="1904" height="1008" alt="login" src="https://github.com/user-attachments/assets/1840cbaf-8479-4adc-aea0-a330a6cd16de" />
        
    &nbsp;
    
    #Main Page  
    <img width="1338" height="1016" alt="home_new" src="https://github.com/user-attachments/assets/f78dd557-9ea5-4cc6-b1fd-6de33b548ff7" />
    
    &nbsp;
    
    #My Page  
    <img width="1095" height="1014" alt="mypage" src="https://github.com/user-attachments/assets/7143b35f-becf-4a2b-9f78-a71335c4ff5a" />
    <img width="1361" height="772" alt="my_post_list" src="https://github.com/user-attachments/assets/663d081b-3b3d-4550-81ca-57a580c50752" />
        
    &nbsp;
    
    #Slack DM 1:1 Q&A  
    <img width="611" height="358" alt="slack_ask_good" src="https://github.com/user-attachments/assets/831b8e13-fd2a-4ee4-b39e-0d5dc057f601" />
    
    &nbsp;
    
    #DM -> Q&A CRUD  
    <img width="1363" height="450" alt="qna_1" src="https://github.com/user-attachments/assets/3d1c7c27-8084-4f8c-a486-108d46440d63" />
    <img width="774" height="535" alt="qna_2" src="https://github.com/user-attachments/assets/6903addf-5a1e-45ed-867e-4fe7987b74a6" />
