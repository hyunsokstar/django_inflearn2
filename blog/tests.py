from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
# 11 timezone 유틸리티
#    User model 임포트
from django.utils import timezone
from django.contrib.auth.models import User


# Create your tests here.

# 테스트 뷰
class TestView(TestCase):
    # 초기화 함수
    def setUp(self):
        # client 객체 초기화
        self.client = Client()
        # 22 유저 객체 생성
        self.author_000 = User.objects.create(username='smith', password='nopassword')

    # post_list view 에 대한 테스트 뷰
    def test_post_list(self):
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        navbar = soup.find('div', id='navbar')
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)

        self.assertEqual(Post.objects.count(), 0)

        # 33 Post 입력
        post_000 = Post.objects.create(
            title='The title post',
            content='Hello World We are the world',
            created=timezone.now(),
            author=self.author_000
        )

        # 44 Post 모델의 게시글 수가 0개 이상인지 테스트
        self.assertGreater(Post.objects.count(), 0)

        # 아직 게시물이 없습니다라는 문자열이 body 태그내에 없다는것을 test
        # 입력한 글의 제목이 body 태그 내에 존재 해야 한다.
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.body
        self.assertNotIn('아직 게시물이 없습니다', body.text)
        self.assertIn(post_000.title , body.text)
        
