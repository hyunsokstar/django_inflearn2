from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category, Tag
from django.utils import timezone
from django.contrib.auth.models import User

# Create your tests here.
def create_tag(name='some_tag'):
    tag, is_created = Tag.objects.get_or_create(
        name=name
    )
    tag.slug = tag.name.replace(' ', '-').replace('/', '')
    tag.save()

    return tag


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
        # self.author_000 = User.objects.create_user(username='smith', password='nopassword')
        self.author_000 = User.objects.create(username='smith')
        self.author_000.set_password('1234')
        self.author_000.save()

        # self.user_obama = User.objects.create_user(username='obama', password='1234')

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

    def test_tag(self):
        tag_000 = create_tag(name='bad_guy')
        tag_001 = create_tag(name='america')

        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,
        )
        post_000.tags.add(tag_000)
        post_000.tags.add(tag_001)
        post_000.save()

        post_001 = create_post(
            title='Stay Fool, Stay Hungry',
            content='Story about Steve Jobs',
            author=self.author_000
        )
        post_001.tags.add(tag_001)
        post_001.save()

        self.assertEqual(post_000.tags.count(), 2)   # post는 여러개의 tag를 가질 수 있다.
        self.assertEqual(tag_001.post_set.count(), 2)   # 하나의 tag는 여러개의 post에 붙을 수 있다.
        self.assertEqual(tag_001.post_set.first(), post_000)    # 하나의 tag는 자신을 가진 post들을 불러올 수 있다.
        self.assertEqual(tag_001.post_set.last(), post_001) # 하나의 tag는 자신을 가진 post들을 불러올 수 있다.



# 테스트 뷰
class TestView(TestCase):
    def setUp(self):
        # print("setup 실행")
        self.client = Client()
        self.author_000 = User.objects.create(username='smith')
        self.author_000.set_password('1234')
        self.author_000.save()

        self.author_001 = User.objects.create(username='obama')
        self.author_001.set_password('1234')
        self.author_001.save()

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

        # post 객체.Absoulte()의 결과값이 예상대로 상세보기 url 인지 확인
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
        # print('응답 코드')
        # print(response.status_code)
        # 정상적으로 응답 완료 처리 되었는지 확인
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        # posting 목록 중에서
        # 응답 내용중에 '미분류가 없어야 한다.'
        # 응답 내용중에 카테고리 이름이 포함되어 있어야 한다.
        main_div = soup.find('div', id='main-div')
        self.assertNotIn('미분류', main_div.text)
        self.assertIn(category_politics.name, main_div.text)

    def test_post_list_about_tag_info(self):
        tag_america = create_tag(name='america')

        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,
        )
        post_000.tags.add(tag_america)
        post_000.save()

        post_001 = create_post(
            title='The second post',
            content='Second Second Second',
            author=self.author_000,
            category=create_category(name='정치/사회')
        )
        post_001.tags.add(tag_america)
        post_001.save()

        self.assertGreater(Post.objects.count(), 0)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.body

        # main_div에는
        main_div = soup.find('div', id='main-div')

        # Tag
        post_card_000 = main_div.find('div', id='post-card-{}'.format(post_000.pk))
        self.assertIn('#america', post_card_000.text) # Tag가 해당 post의 card마다 있다.

    def test_post_list_about_serachByTag(self):
        tag_000 = create_tag(name='bad_guy')
        tag_001 = create_tag(name='america')

        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,
        )
        post_000.tags.add(tag_000)
        post_000.tags.add(tag_001)
        post_000.save()

        post_001 = create_post(
            title='Stay Fool, Stay Hungry',
            content='Story about Steve Jobs',
            author=self.author_000
        )

        post_001.tags.add(tag_001)
        post_001.save()

        response = self.client.get(tag_000.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', id='main-div')

        # posting 상단에 h1 태그이면서 속성값이 id="blog-list-title"인 태그를 찾아서
        # 그 태그의 text로 blog_000.text 즉 클릭한 태그 이름이 출력되는지 확인
        blog_h1 = main_div.find('h1', id='blog-list-title')
        self.assertIn('#{}'.format(tag_000.name), blog_h1.text)
        #
        # 해당 태그 정보(클릭한 태그)에 대한 posting은 출력
        # 아닌 posting은 출력되면 안됨
        self.assertIn(post_000.title, main_div.text)
        self.assertNotIn(post_001.title, main_div.text)

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

    # post_detail page 출력시에
    # 카테고리 정보 태그 정보에디트 버튼 출력에 대해 테스트
    def test_post_detail_about_output_of_categoryInfo_and_editButton(self):
        # Post 모델에 row 데이터 1개 입력
        category_politics = create_category(name='정치/사회')

        # Post 모델에 데이터 2개 입력
        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,
            category=category_politics
        )

        post_001 = create_post(
            title='The second post',
            content='Second Second Second',
            author=self.author_000,
            category=create_category(name='취미/생활')
        )

        # post_000에 태그 정보 추가
        tag_america = create_tag(name='america')
        post_000.tags.add(tag_america)
        post_000.save()

        # 상세 보기 url 가져오기
        post_000_url = post_000.get_absolute_url()
        # 상세 보기 url 요청
        response = self.client.get(post_000_url)
        # 응답 완료 확인
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.body
        main_div = body.find('div', id='main-div')
        # 카테 고리 정보는 출력
        self.assertIn(category_politics.name, main_div.text)
        # edit 버튼은 미출력
        self.assertNotIn('EDIT', main_div.text)
        # tags 정보 출력 확인
        self.assertIn('#america', main_div.text)
        # print("유저 : " ,User.objects.all())

        # login을 한 경우,
        login_success = self.client.login(username='smith', password='1234')
        self.assertTrue(login_success)

        response = self.client.get(post_000_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', id='main-div')
        # print("post_000.author : ", post_000.author)
        # print("self.author_000 : ", self.author_000)

        self.assertEqual(post_000.author, self.author_000)

        # EDIT 버튼이 있다.
        self.assertIn('EDIT', main_div.text)

        # 다른 사람인 경우에는 없다.
        login_success = self.client.login(username='obama', password='1234')
        self.assertTrue(login_success)

        response = self.client.get(post_000_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', id='main-div')

        self.assertEqual(post_000.author, self.author_000)
        self.assertNotIn('EDIT', main_div.text)

    def test_post_update(self):
        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,
        )

        self.assertEqual(post_000.get_update_url(), post_000.get_absolute_url() + 'update/')

        response = self.client.get(post_000.get_update_url())
        self.assertEqual(response.status_code, 200)
