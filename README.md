# :pushpin: Ladder To Wine
![Untitled (2)](https://user-images.githubusercontent.com/104430302/186121208-7565c0cf-35f4-490c-9411-f3941c5f6213.png)
>와인을 잘 모르는 사람들에게 와인을 추천해주는 웹페이지    
>https://github.com/hangunhee94/ladder_to_wine   

</br>

### S.A
[상세 내용 참고](https://www.notion.so/Team-Ladder-6d5dfdecb8454b04bc0a1ffc7c5de825)

## 1. 제작 기간 & 참여 인원
- 2022.6.4 ~ 2022.6.14  
- 팀 프로젝트
- 4인  

</br>

## 2. 사용 기술
#### `Back-end`
  - Django

#### `Front-end`
  - HTML5
  - CSS3
  - JavaScript
  
#### `배포` 
  - EC2 
</br>

## 3. 핵심 기능
>이 프로젝트의 핵심 기능은 와인에 문외한인 사용자들에게 세계의 각종 와인들을 추천해주고 정보를 알려주는 웹페이지입니다.   
>사용자는 각종 와인의 알코올수치, 원산지, 산미 등을 확인하고 비슷한 와인을 추천 받을 수 있습니다.      

### 3.1. 와이어프레임   
![Untitled](https://user-images.githubusercontent.com/104430302/186120803-dff2c6d9-d257-4618-b734-201e1204ae86.png)


### 3.2. ERD    
![Untitled (1)](https://user-images.githubusercontent.com/104430302/186120969-11632428-2828-459d-99b9-84453c76b66d.png)

### 3.3. API
![ladder_to_wine_API](https://user-images.githubusercontent.com/104430302/188553104-0de4ff5f-a2e3-45d8-9b7b-1d5a5221b60d.PNG)

<br>

## 4. 핵심 트러블 슈팅
### 4.1. DB에 저장된 와인 검색 기능 오류

- DB에 저장되어있는 와인들의 이름이 포함된 내용을 검색하였을 때, 값을 받아오지 못하는 이슈

- Django 템플릿 문법의 잘못된 사용으로 값들이 불러와지지 않는 상황

- 와인의 DB에서 이름에 검색어가 포함된 경우를 filter로 뽑은 후, Django 템플릿 문법으로 HTML에 보여지도록 설정
```
def search(request):
        if request.method == 'POST':
            searched = request.POST['searched']        
            winename = WineModel.objects.filter(name__contains=searched)
            return render(request, 'search.html', {'searched': searched, 'winename': winename})
        else:
            return render(request, 'search.html', {})
```
</br>

```

{% block title %}
검색
{% endblock %}
{% block content %}

    {% if searched %}
        <div>
            <div>
                <div>
                    <h2> " {{ searched }} "가 포함된 와인을 검색하였습니다. </h2>
                </div>
                <br>
                {% for WineModel in winename %}
                    <p>
                        <a href="/wine/{{ WineModel.id }}" class="search-wine">- {{ WineModel.name }} {{ WineModel.year}} </a> <br>
                    </p>
                {% endfor %}
            </div>
            <div class="search-height">
                
            </div>
            {% else %}
            <div class="search-content">
                <br>
                <br>
                <h1> 찾고 있는 와인을 검색창에 입력해주세요. </h1>
            </div>
        </div>
            
    {% endif %}

{% endblock %}
```

</br>


## 6. 회고 / 느낀점
>프로젝트 개발 회고 글: https://hee94.tistory.com/41 

---
