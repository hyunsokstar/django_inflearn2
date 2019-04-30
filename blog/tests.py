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

    def test_post_list(self):
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        self.check_navbar(soup)

        self.assertEqual(Post.objects.count(), 0)

        # 33 Post 입력
        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,
        )

        self.assertGreater(Post.objects.count(), 0)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.body
        self.assertNotIn('아직 게시물이 없습니다', body.text)
        self.assertIn(post_000.title , body.text)

    def test_post_detail(self):
        # Post 모델에 row 데이터 1개 입력
        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,
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
