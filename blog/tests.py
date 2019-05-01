from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category

from django.utils import timezone
from django.contrib.auth.models import User

# Create your tests here.
def create_category(name='life', description=''):
    category, is_created = Category.objects.get_or_create(
        name=name,
        description=description
    )

    category.slug = category.name.replace(' ', '-').replace('/', '')
    category.save()

    return category

def create_post(title, content, author, category=None):
    blog_post = Post.objects.create(
        title=title,
        content=content,
        created=timezone.now(),
        author=author,
        category=category
    )
    return blog_post

# Test Model
class TestModel(TestCase):
    def setUp(self):
        self.client = Client()
        self.author_000 = User.objects.create(username='smith', password='nopassword')

    def test_category(self):
        category = create_category()

        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,
            category=category
        )
        # 카테 고리 모델을 참조하는 post 모델의 정보를
        # category.모델명(소문자).count()를 통해서 가져 올 수 있다.
        self.assertEqual(category.post_set.count(), 1)



    def test_post(self):
        category = create_category()

        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,
            category=category
        )


# 테스트 뷰
class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.author_000 = User.objects.create(username='smith', password='nopassword')

    def check_navbar(self, soup):
        navbar = soup.find('div', id='navbar')
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)

    def test_post_list_no_post(self):
        # post_list 요청 날리기
        response = self.client.get('/blog/')
        # 완료 코드 확인 하기
        self.assertEqual(response.status_code, 200)
        # 내용 확인 하기 (타이틀 태그, 네비게이션바 유무, 게시물이 없습니다 메세지)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title
        self.assertEqual(title.text, 'Blog')
        self.check_navbar(soup)
        self.assertEqual(Post.objects.count(), 0)
        self.assertIn('아직 게시물이 없습니다', soup.body.text)

    # 오른쪽 사이드바 출력 내용에 카테고리 정보 포함되는지 확인
    def check_right_side(self, soup):
        # 카테고리 영역에 id='category-card'를 지정
        category_card = soup.find('div', id='category-card')

        self.assertIn('미분류 (1)', category_card.text)  # 미분류 (1) 있어야 함
        self.assertIn('정치/사회 (1)', category_card.text)  # 정치/사회 (1) 있어야 함


    def test_post_list_with_post(self):
        # post 모델 입력
        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,
        )

        post_001 = create_post(
            title='The second post',
            content='Second Second Second',
            author=self.author_000,
            category=create_category(name='정치/사회')
        )

        # post_list_view 요청 하기
        response = self.client.get('/blog/')
        # 응답 텍스트를 가져오기 위해  soup 객체 생성
        soup = BeautifulSoup(response.content, 'html.parser')
        # soup 객체를 이용해 body 객체 생성
        body = soup.body
        # soup 객체를 이용해 title 태그 객체 생성
        title = soup.title
        # title이 'Blog로 출력되는지 확인'
        self.assertEqual(title.text, 'Blog')
        # nav bar 가 있어야 한다.
        self.check_navbar(soup)
        # Post 모델 개수 확인 하기(0개 이상)
        self.assertGreater(Post.objects.count(), 0)
        # 아직 아직 게시물이 없습니다 문자열이 없어야 한다.
        self.assertNotIn('아직 게시물이 없습니다', body.text)

        # 오른쪽 카테고리 메뉴의 항목이 제대로 출력되는지 테스트
        self.check_right_side(soup)

        # main_div에는
        main_div = soup.find('div', id='main-div')
        self.assertIn('정치/사회', main_div.text)  # '정치/사회' 있어야 함
        self.assertIn('미분류', main_div.text)  # '미분류' 있어야 함

    def test_post_detail(self):
        # Post 모델에 row 데이터 1개 입력
        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,
        )

        post_001 = create_post(
            title='The second post',
            content='Second Second Second',
            author=self.author_000,
            category=create_category(name='정치/사회')
        )

        # post 입력이 제대로 되었는지 확인(게시글이 0개보다 많은지 테스트)
        self.assertGreater(Post.objects.count(), 0)

        # post 객체.getAbsoulte()의 결과값이 예상대로 상세보기 url 인지 확인
        post_000_url = post_000.get_absolute_url()
        self.assertEqual(post_000_url, '/blog/{}/'.format(post_000.pk))

        #  상세 보기 페이지의 타이틀이 입력한 글의 제목-blog 인지 test
        response = self.client.get(post_000_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        self.assertEqual(title.text, '{} - Blog'.format(post_000.title))

        # 네브바 출력에 대해 확인
        self.check_navbar(soup)

        # 오른쪽 카테고리 메뉴의 항목이 제대로 출력되는지에 대해 테스트
        self.check_right_side(soup)

    def test_post_list_by_category(self):
        category_politics = create_category(name='정치/사회')
        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,
        )
        post_001 = create_post(
            title='The second post',
            content='Second Second Second',
            author=self.author_000,
            category=category_politics
        )
        response = self.client.get(category_politics.get_absolute_url())
        print("get_absolute_url : ", category_politics.get_absolute_url())
        print('응답 코드')
        print(response.status_code)
        # 정상적으로 응답 완료 처리 되었는지 확인
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        # posting 목록 중에서
        # 응답 내용중에 '미분류가 없어야 한다.'
        # 응답 내용중에 카테고리 이름이 포함되어 있어야 한다.
        main_div = soup.find('div', id='main-div')
        self.assertNotIn('미분류', main_div.text)
        self.assertIn(category_politics.name, main_div.text)
