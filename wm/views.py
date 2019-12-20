# from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .forms import MyShortCutForm_input, MyShortCutForm_summer_note , MyShortCutForm_image
from accounts2.models import Profile
from .models import MyShortCut, Type, Category, CategoryNick, CommentForShortCut , TempMyShortCut, TempMyShortCutForBackEnd, CommentForShortCut, RecommandationUserAboutSkillNote
from skilblog.models import SkilBlogTitle, SkilBlogContent
from django.http import HttpResponseRedirect
from datetime import datetime , timedelta
from django.utils import timezone
from django.urls import reverse_lazy


# 1122
def category_plus_1_for_current_user(request):
    # is this possible?
    # for x in range(i, 98)
    #     CategoryNick.obejcts.filter(author=request.user).update("ca"+(x+1)=F('ca'+x))

    ca_num = request.POST['current_ca_num'] # 입력한 ca 번호
    print("ca_num : ", ca_num)
    print("ca_num type :",type(ca_num))

    # data2 = {'ca{}'.format(x+1): F('ca{}'.format(x)) for x in range(int(ca_num), 99)}
    data2 = {'ca{}'.format(x+1): F('ca{}'.format(x)) for x in range(int(ca_num), 120)}

    CategoryNick.objects.filter(
        author=request.user
    ).update(**data2)

    # data1 = {'ca{}'.format(ca_num): "+1 실행 완료" }

    # CategoryNick.objects.filter(
    #     author=request.user
    # ).update(**data1)

    skil_note = MyShortCut.objects.filter(Q(author=request.user)).order_by("created")

    ca_delete=Category.objects.get(name="ca120")
    MyShortCut.objects.filter(Q(author=request.user) & Q(category=ca_delete)).delete()

    for sn in skil_note:
        # if(sn.category.id >= int(ca_num) and sn.category.id != 99):
        if(sn.category.id >= int(ca_num) and sn.category.id != 120):
            print("sn.category.id : ", sn.category.id)
            print("int(sn.category.id)+1 : ", int(sn.category.id)+1)
            ca = Category.objects.get(id=int(sn.category.id)+1)
            MyShortCut.objects.filter(id=sn.id).update(category=ca, created=F('created'))
        else:
            print("sn.category.id : ", sn.category.id)

    return JsonResponse({
        'message': "ca"+ca_num+"부터 ca120까지 +1 성공"
    })


def category_minus_1_for_current_user(request):
    # ca=Category.objects.filter(id=category_num)
    ca_num = request.POST['current_ca_num'] # 입력한 ca 번호

    print("ca_num check : ", ca_num)
    print("ca_num type :",type(ca_num))

    data = {'ca{}'.format(x-1): F('ca{}'.format(x)) for x in range(120,int(ca_num)-1,-1)}
    CategoryNick.objects.filter(
        author=request.user
    ).update(**data)

    skil_note = MyShortCut.objects.filter(Q(author=request.user))

    if(int(ca_num)>1):
        ca_delete_num = int(ca_num)-1

    ca_delete=Category.objects.get(id=ca_delete_num)
    MyShortCut.objects.filter(Q(author=request.user) & Q(category=ca_delete)).delete()
    # MyShortCut.obejcts.filter(Q(id=ca))

    for sn in skil_note:
        # print("sn.category.id : ", sn.category.id)
        if(sn.category.id >= int(ca_num) and sn.category.id != 1):
            # ca=Category.objects.get(id=int(sn.category.id)+1)
            print("sn.category.id : ", sn.category.id)
            print("int(sn.category.id)-1 : ", int(sn.category.id)-1)
            ca = Category.objects.get(id=int(sn.category.id)-1)
            MyShortCut.objects.filter(id=sn.id).update(category=ca, image = F('image'))

    return JsonResponse({
        'message': "ca"+ca_num+"부터 ca120까지 -1 성공"
    })


#     skil_note = MyShortCut.objects.filter(category=ca, author= request.user)
#
# for num in range(10, 98):
# 	ca = "ca"+str(num)
#     MyShortCut.objects.filter(category=plus1, author= request.user)
#
#     for s in skil_note:
#         ca_plus_1= s.category+1
#         s.update(category=ca_plus_1)


def move_to_skil_blog(request):
    title = request.POST['title'] # 어떤 유저에 대해
    shortcut_ids = request.POST.getlist('shortcut_arr[]')

    sbt = SkilBlogTitle.objects.create(title=title, author=request.user)

    if shortcut_ids:
        skill_note_list = MyShortCut.objects.filter(pk__in=shortcut_ids, author=request.user).order_by('-created')
        print('skill_note_lists : ', skill_note_list)

    for p in skill_note_list:
        # print("p : ", p)
        profile = SkilBlogContent.objects.create(
            sbt = sbt,
			author = request.user,
			title = p.title,
			content1 = p.content1,
			content2 = p.content2,
			type_id = p.type_id,
            image = p.image
		)
    return JsonResponse({
        'message': "체크한 항목들을 스킬 블로그로 옮겼습니다."+title,
    })

def plus_recommand_for_skillnote_user(request):
    user_pk = request.POST['user_pk'] # 어떤 유저에 대해
    user_id = request.POST['user_id'] # 추천을 누가

    user =  get_object_or_404(User, pk=user_pk)
    print("user : " , user)
    print("user_id : ", user_id)

    recommand_count = RecommandationUserAboutSkillNote.objects.filter(Q(user=user) & Q(author_id=user_id)).count()
    print("recommand_count : ", recommand_count)

    if recommand_count < 1:
        rc = RecommandationUserAboutSkillNote.objects.create(user=user ,author_id=user_id)
        print('추천을 추가')
        recommand_count = RecommandationUserAboutSkillNote.objects.filter(Q(user=user)).count()
        profile = Profile.objects.filter(Q(user=user)).update(skill_note_reputation = recommand_count)

        return JsonResponse({
            'message': "추천 +1",
            "option":"plus",
            "recommand_count":recommand_count
        })

    else:
        RecommandationUserAboutSkillNote.objects.filter(Q(user=user) & Q(author_id=user_id)).delete()
        recommand_count = RecommandationUserAboutSkillNote.objects.filter(Q(user=user)).count()
        profile = Profile.objects.filter(Q(user=user)).update(skill_note_reputation = recommand_count)

        return JsonResponse({
            'message': "추천 -1 ",
            "option":"minus",
            "recommand_count":recommand_count
        })



def copy_to_me_from_user_id(request):

    author = request.POST['author']
    # 나의 노트 모두 지우기
    if( MyShortCut.objects.filter(Q(author=request.user)).count() != 0):
        MyShortCut.objects.filter(Q(author=request.user)).delete()
        CategoryNick.objects.filter(Q(author=request.user)).delete()
        CommentForShortCut.objects.filter(Q(author=request.user)).delete()

    user_id = User.objects.get(username=author).id
    print("user_id : " , user_id)

    wm_list_for_copy = MyShortCut.objects.filter(Q(author=user_id))
    print("wm_list_for_copy : " , wm_list_for_copy);
    MyShortCut.objects.filter(Q(author=request.user)).delete()

    comment_wm_list_for_copy = CommentForShortCut.objects.filter(Q(author=user_id))


    for p in wm_list_for_copy:
        myshortcut = MyShortCut.objects.create(
            author = request.user,
            title = p.title,
            content1 = p.content1,
            content2 = p.content2,
            type_id = p.type_id,
            category = p.category,
            filename = p.filename,
            image=p.image,
            created = p.created,
        )
        # print("myshortcut : " , myshortcut.id)
        for comment in comment_wm_list_for_copy:
            # print("comment.id : ", comment.id)
            # print("myshortcut.id : ", myshortcut.id )
            if comment.shortcut.id == p.id:
                print("댓글 생성 시도 확인")
                wm = MyShortCut.objects.filter(id = comment.id)
                wm_comment = CommentForShortCut.objects.create(
                    author = request.user,
                    title=comment.title,
                    shortcut = myshortcut,
                    content = comment.content,
                    created_at = comment.created_at,
                )

    list_for_copy2 = CategoryNick.objects.filter(Q(author=user_id))
    print("list_for_copy2 : " , list_for_copy2);

    CategoryNick.objects.filter(Q(author=request.user)).delete()

    for p in list_for_copy2:
        CN = CategoryNick.objects.create(
            author = request.user,
            ca1 = p.ca1,
            ca2 = p.ca2,
            ca3 = p.ca3,
            ca4 = p.ca4,
            ca5 = p.ca5,
            ca6 = p.ca6,
            ca7 = p.ca7,
            ca8 = p.ca8,
            ca9 = p.ca9,
            ca10 = p.ca10,
            ca11 = p.ca11,
            ca12 = p.ca12,
            ca13 = p.ca13,
            ca14 = p.ca14,
            ca15 = p.ca15,
            ca16 = p.ca16,
            ca17 = p.ca17,
            ca18 = p.ca18,
            ca19 = p.ca19,
            ca20 = p.ca20,
            ca21 = p.ca21,
            ca22 = p.ca22,
            ca23 = p.ca23,
            ca24 = p.ca24,
            ca25 = p.ca25,
            ca26 = p.ca26,
            ca27 = p.ca27,
            ca28 = p.ca28,
            ca29 = p.ca29,
            ca30 = p.ca30,
            ca31 = p.ca31,
            ca32 = p.ca32,
            ca33 = p.ca33,
            ca34 = p.ca34,
            ca35 = p.ca35,
            ca36 = p.ca36,
            ca37 = p.ca37,
            ca38 = p.ca38,
            ca39 = p.ca39,
            ca40 = p.ca40,
            ca41 = p.ca41,
            ca42 = p.ca42,
            ca43 = p.ca43,
            ca44 = p.ca44,
            ca45 = p.ca45,
            ca46 = p.ca46,
            ca47 = p.ca47,
            ca48 = p.ca48,
            ca49 = p.ca49,
            ca50 = p.ca50,
            ca51 = p.ca51,
            ca52 = p.ca52,
            ca53 = p.ca53,
            ca54 = p.ca54,
            ca55 = p.ca55,
            ca56 = p.ca56,
            ca57 = p.ca57,
            ca58 = p.ca58,
            ca59 = p.ca59,
            ca60 = p.ca60,
            ca61 = p.ca61,
            ca62 = p.ca62,
            ca63 = p.ca63,
            ca64 = p.ca64,
            ca65 = p.ca65,
            ca66 = p.ca66,
            ca67 = p.ca67,
            ca68 = p.ca68,
            ca69 = p.ca69,
            ca70 = p.ca70,
            ca71 = p.ca71,
            ca72 = p.ca72,
            ca73 = p.ca73,
            ca74 = p.ca74,
            ca75 = p.ca75,
            ca76 = p.ca76,
            ca77 = p.ca77,
            ca78 = p.ca78,
            ca79 = p.ca79,
            ca80 = p.ca80,
            ca81 = p.ca81,
            ca82 = p.ca82,
            ca83 = p.ca83,
            ca84 = p.ca84,
            ca85 = p.ca85,
            ca86 = p.ca86,
            ca87 = p.ca87,
            ca88 = p.ca88,
            ca89 = p.ca89,
            ca90 = p.ca90,
            ca91 = p.ca91,
            ca92 = p.ca92,
            ca93 = p.ca93,
            ca94 = p.ca94,
            ca95 = p.ca95,
            ca96 = p.ca96,
            ca97 = p.ca97,
            ca98 = p.ca98,
            ca99 = p.ca99,
        )

    return JsonResponse({
        'message': author+'의 노트 전체를 나의 노트로 복사 했습니다',
    })

def edit_complete_skill_note_for_backend(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        print("content2 변수 넘어 왔다.")
        content2 = request.POST.get('content2','')
        # content2 = request.POST['content2']

        print('TempMyShortCutForBackEnd text를 ajax로 update textarea')
        print('id : ', id)
        print("content2 : ", content2)
        todo = TempMyShortCutForBackEnd.objects.filter(Q(id=id)).update(content2 = content2)
        print('backend update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')

def edit_complete_skill_note_for_front_end(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        print("content2 변수 넘어 왔다.")
        content2 = request.POST.get('content2','')
        # content2 = request.POST['content2']

        print('shortcut을 ajax로 update textarea')
        print('id : ', id)
        print("content2 : ", content2)
        todo = TempMyShortCut.objects.filter(Q(id=id)).update(content2 = content2)
        print('frontend update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')

def edit_temp_skill_note_using_textarea_for_backend(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        print("content2 변수 넘어 왔다.")
        content2 = request.POST.get('content2','')
        # content2 = request.POST['content2']

        print('TempMyShortCut 을 ajax로 update textarea')
        print('id : ', id)
        print("content2 : ", content2)
        todo = TempMyShortCutForBackEnd.objects.filter(Q(id=id)).update(content2 = content2)
        print('TempMyShortCut update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')

def edit_temp_skill_note_using_input_for_backend(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        content1 = request.POST.get('content1','')

        print('TempMyShortCutForBackEnd 을 ajax로 update input')
        print('id : ', id)
        print("content1 : ", content1)
        todo = TempMyShortCutForBackEnd.objects.filter(Q(id=id)).update(content1 = content1)
        print('update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공 22',
        })
    else:
        return redirect('/todo')

def update_temp_skil_title_for_backend(request,id):
    user = request.user
    title = request.POST['title']

    if request.method == "POST" and request.is_ajax():
        todo = TempMyShortCutForBackEnd.objects.filter(Q(id=id)).update(title=title)
        print('TempMyShortCutForBackEnd update 성공 id : ' , id);

        return JsonResponse({
            'message': 'shortcut 업데이트 성공',
            'title':title
        })
    else:
        return redirect('/todo')

def delete_temp_skill_note_for_backendarea(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        todo = TempMyShortCutForBackEnd.objects.filter(Q(id=id)).delete()
        print('TempMyShortCutForBackEnd delete 성공 id : ' , id);
        return JsonResponse({
            'message': 'shortcut 삭제 성공',
        })
    else:
        return redirect('/todo')

def insert_temp_skill_note_using_input_for_backend(request):
    print("create_new1_input 22 실행")
    ty = Type.objects.get(type_name="input")
    category_id = request.user.profile.selected_category_id
    ca = Category.objects.get(id=category_id)
    title = request.POST['title']

    wm = TempMyShortCutForBackEnd.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        content1 = ""
    )
    print("wm : ", wm)
    return JsonResponse({
        'message': '인풋 박스 추가 성공',
        'shortcut_id':wm.id,
        'shortcut_title':wm.title,
        'shortcut_content':wm.content1,
    })

def insert_temp_skill_note_using_textarea_for_backend(request):
    print("insert_temp_skill_note_for_textarea 실행")
    ty = Type.objects.get(type_name="textarea")
    category_id = request.user.profile.selected_category_id
    ca = Category.objects.get(id=category_id)
    title = request.POST['title']

    wm = TempMyShortCutForBackEnd.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        content2 = ""
    )

    print("wm : ", wm)

    return JsonResponse({
        'message': 'textarea 박스 추가 성공',
        'shortcut_id':wm.id,
        'shortcut_title':wm.title,
        'shortcut_content2':wm.content2,
    })


def temp_skill_list_for_backend(request):
	print("temp_skill_list 실행")
	user = request.user

	object_list = TempMyShortCutForBackEnd.objects.filter(author=user)

	return render(request, 'wm/TempMyShortCutForBackEnd_list.html', {
		'object_list': object_list
	})

def insert_temp_skill_note_for_input(request):
    print("create_new1_input 실행 11")
    ty = Type.objects.get(type_name="input")
    category_id = request.user.profile.selected_category_id
    ca = Category.objects.get(id=category_id)
    title = request.POST['title']

    wm = TempMyShortCut.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        content1 = ""
    )
    print("wm : ", wm)
    return JsonResponse({
        'message': '인풋 박스 추가 성공',
        'shortcut_id':wm.id,
        'shortcut_title':wm.title,
        'shortcut_content':wm.content1,
    })

def edit_temp_skill_note_for_input(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        content1 = request.POST.get('content1','')

        print('TempMyShortCut 을 ajax로 update input')
        print('id : ', id)
        print("content1 : ", content1)
        todo = TempMyShortCut.objects.filter(Q(id=id)).update(content1 = content1)
        print('update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')

def update_temp_skill_note_for_textarea(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        print("content2 변수 넘어 왔다.")
        content2 = request.POST.get('content2','')
        # content2 = request.POST['content2']

        print('TempMyShortCut 을 ajax로 update textarea')
        print('id : ', id)
        print("content2 : ", content2)
        todo = TempMyShortCut.objects.filter(Q(id=id)).update(content2 = content2)
        print('TempMyShortCut update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')

def insert_temp_skill_note_for_textarea(request):
    print("insert_temp_skill_note_for_textarea 실행")
    ty = Type.objects.get(type_name="textarea")
    category_id = request.user.profile.selected_category_id
    ca = Category.objects.get(id=category_id)
    title = request.POST['title']

    wm = TempMyShortCut.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        content2 = ""
    )

    print("wm : ", wm)

    return JsonResponse({
        'message': 'textarea 박스 추가 성공',
        'shortcut_id':wm.id,
        'shortcut_title':wm.title,
        'shortcut_content2':wm.content2,
    })


def delete_temp_memo_by_ajax(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        todo = TempMyShortCut.objects.filter(Q(id=id)).delete()
        print('TempMyShortCut delete 성공 id : ' , id);
        return JsonResponse({
            'message': 'shortcut 삭제 성공',
        })
    else:
        return redirect('/todo')

def update_temp_skil_title(request,id):
    user = request.user
    title = request.POST['title']

    if request.method == "POST" and request.is_ajax():
        todo = TempMyShortCut.objects.filter(Q(id=id)).update(title=title)
        print('TempMyShortCut update 성공 id : ' , id);

        return JsonResponse({
            'message': 'shortcut 업데이트 성공',
            'title':title
        })
    else:
        return redirect('/todo')

def temp_skill_list(request):
	print("temp_skill_list 실행")
	user = request.user

	object_list = TempMyShortCut.objects.filter(author=user)

	return render(request, 'wm/TempMyShortCut_list.html', {
		'object_list': object_list
	})

def copyForCategorySubjectToMyCategory(request):
	author = request.POST['author']
	original_category = request.POST['original_category']
	destination_category = request.POST['destination_category']

	print("author : ", author)
	print("original_category : ", original_category)
	print("destination_category : ", destination_category)

	MyShortCut.objects.filter(Q(author=request.user) & Q(category=destination_category)).delete()

	user_id = User.objects.get(username=author).id
	ca_id = Category.objects.get(name=original_category)

	list_for_copy = MyShortCut.objects.filter(Q(author=user_id) & Q(category = ca_id))

	category = Category.objects.get(id=destination_category)

	for p in list_for_copy:
		profile = MyShortCut.objects.create(
			author = request.user,
			title = p.title,
			content1 = p.content1,
			content2 = p.content2,
			type_id = p.type_id,
            created=p.created,
			category = category,
		)
	return JsonResponse({
		'message': author+'의 '+ original_category +'를 나의 ' +destination_category +'로 복사 했습니다',
	})

def search_by_id_and_word(request):
    search_user_id = request.user
    search_word = request.POST['search_word']
    search_option = request.POST['search_option']
    print("search_user_id : ", search_user_id)
    print("search_word : ", search_word)
    print("search_option : ", search_option)

    user = User.objects.get(username=search_user_id)


    # | Q(content1__icontains=search_word) | Q(content2__icontains=search_word)
    if(search_option == "content+title"):
        object_list = MyShortCut.objects.filter(Q(author = user)).filter(Q(title__icontains=search_word) | Q(content1__icontains=search_word) | Q(content2__icontains=search_word)).order_by('-category')
        print("search content + title ")

        return render(request, 'wm/MyShortCut_list_for_search.html', {
			'object_list': object_list
		})

    elif(search_option == "only_title"):
        search_word = request.POST['search_word']
        object_list = MyShortCut.objects.filter(Q(title__icontains=search_word) & Q(author = user) ).order_by('-category')
        print("search , only_title")

        return render(request, 'wm/MyShortCut_list_for_search.html', {
			'object_list': object_list
		})
    elif(search_option == "content_title_alluser"):
        user = User.objects.get(username=search_user_id)
        search_word = request.POST['search_word']
        object_list = MyShortCut.objects.filter(Q(title__icontains=search_word) | Q(content1__icontains=search_word) | Q(content2__icontains=search_word)).order_by('-category')

        print("search_user_id : ", search_user_id)
        print("search_word : ", search_word)
        print("object_list : ", object_list)

    elif(search_option == "file_history"):
        print("file_history 검색 실행")
        user = User.objects.get(username=search_user_id)
        search_word = request.POST['search_word']
        object_list = MyShortCut.objects.filter(Q(filename__icontains=search_word) & Q(author = user)).order_by('-category')
        print("search_user_id : ", search_user_id)
        print("search_word : ", search_word)
        print("object_list : ", object_list)
        # print("file_history 검색 실행 : " , object_list)

        return render(request, 'wm/MyShortCut_list_for_search.html', {
			'object_list': object_list
		})

    else:
        user = User.objects.get(username=search_user_id)
        search_word = request.POST['search_word']
        object_list = MyShortCut.objects.filter(Q(title__icontains=search_word)).order_by('-category')

        print("search_user_id : ", search_user_id)
        print("search_word : ", search_word)
        print("object_list : ", object_list)

        return render(request, 'wm/MyShortCut_list_for_search.html', {
			'object_list': object_list
		})


def delete_comment_for_my_shortcut(request, shortcut_comment_id):
    print('shortcut_comment_id : ' , shortcut_comment_id)
    co = CommentForShortCut.objects.filter(id=shortcut_comment_id).delete()

    return JsonResponse({
        'message': '댓글 삭제 성공',
    })

def update_comment_for_my_shortcut(request, shortcut_comment_id):
    print('shortcut_comment_id : ' , shortcut_comment_id)
    co = CommentForShortCut.objects.filter(id=shortcut_comment_id).update(
        title= request.POST['title'],
        content = request.POST['content']
    )

    return JsonResponse({
        'message': '댓글 수정 성공',
    })

def new_comment_for_my_shortcut(request, shortcut_id):
    print('shortcut_id : ' , shortcut_id)
    shortcut = MyShortCut.objects.get(id=shortcut_id)
    co = CommentForShortCut.objects.create(
        shortcut= shortcut,
        author = request.user,
        title="default title",
        content = "default content"
    )

    return JsonResponse({
        'message': shortcut.title+ '에 대해 comment 추가 성공 ',
        'comment_id':co.id,
        'comment_title':co.title,
        'comment_content':co.content,
    })

def create_new4_textarea(request):
    print("create_new4_textarea 실행")
    ty = Type.objects.get(type_name="textarea")
    category_id = request.user.profile.selected_category_id
    ca = Category.objects.get(id=category_id)
    # title = request.POST['title']

    wm1 = MyShortCut.objects.create(
        author = request.user,
        title="title1",
        type= ty,
        category = ca,
        content2 = ""
    )
    wm2 = MyShortCut.objects.create(
        author = request.user,
        title="title2",
        type= ty,
        category = ca,
        content2 = ""
    )
    wm3 = MyShortCut.objects.create(
        author = request.user,
        title="title3",
        type= ty,
        category = ca,
        content2 = ""
    )
    wm4 = MyShortCut.objects.create(
        author = request.user,
        title="title4",
        type= ty,
        category = ca,
        content2 = ""
    )
    wm5 = MyShortCut.objects.create(
        author = request.user,
        title="title5",
        type= ty,
        category = ca,
        content2 = ""
    )

    print("wm1 : ", wm1)

    return JsonResponse({
        'message': 'textarea 박스 추가 성공',
        'shortcut_id':wm1.id,
        'shortcut_title':wm1.title,
        'shortcut_content2':wm1.content2,
    })

# myshortcut_row, shorcut_id, shorcut_content
def create_new1_input(request):
    print("create_new1_input 실행 original")
    ty = Type.objects.get(type_name="input")
    category_id = request.user.profile.selected_category_id
    ca = Category.objects.get(id=category_id)
    title = request.POST['title']

    wm = MyShortCut.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        content1 = "",
        created = datetime.now()
    )
    print("wm : ", wm)
    return JsonResponse({
        'message': '인풋 박스 추가 성공',
        'shortcut_id':wm.id,
        'shortcut_title':wm.title,
        'shortcut_content':wm.content1,
    })

def create_new1_input_first(request):
    print("create_new1_input 실행 2222")
    ty = Type.objects.get(type_name="input")
    category_id = request.user.profile.selected_category_id

    current_first = MyShortCut.objects.filter(Q(category=category_id) & Q(author=request.user)).order_by("created").first();
    print("current_first.id : ", current_first.title);

    ca = Category.objects.get(id=category_id)
    title = request.POST['title']

    wm = MyShortCut.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        content1 = "",
        created = current_first.created-timedelta(seconds=10)
    )

    return JsonResponse({
        'message': '인풋 박스 추가 성공',
        'shortcut_id':wm.id,
        'shortcut_title':wm.title,
        'shortcut_content':wm.content1,
    })

# 2244
def create_new1_input_between(request,current_article_id):

    current_article_id = current_article_id
    current_article = MyShortCut.objects.get(id=current_article_id)
    print("current_article_time : " , current_article.created)

    smae_category_for_current_article=MyShortCut.objects.filter(author= current_article.author, category = current_article.category).order_by("created")

    same_category_id_array = []

    for i,p in enumerate(smae_category_for_current_article):
        # print('i',i)
        if (p.created <= current_article.created):
            MyShortCut.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=0))
        else:
            MyShortCut.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=i+1))


    print("create_new1_input 실행")
    ty = Type.objects.get(type_name="input")
    category_id = request.user.profile.selected_category_id
    ca = Category.objects.get(id=category_id)
    title = request.POST['title']

    wm = MyShortCut.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        content1 = "",
        created=current_article.created+timedelta(seconds=1.5)
    )
    print("wm : ", wm)
    return JsonResponse({
        'message': '인풋 박스 추가 성공',
        'shortcut_id':wm.id,
        'shortcut_title':wm.title,
        'shortcut_content':wm.content1,
    })


# 2244
def create_new2_textarea_first(request):
    print("create_new2_textarea_first")
    ty = Type.objects.get(type_name="textarea")
    category_id = request.user.profile.selected_category_id
    ca = Category.objects.get(id=category_id)
    title = request.POST['title']
    file_name = request.POST['file_name']

    current_first = MyShortCut.objects.filter(Q(category=category_id) & Q(author=request.user)).order_by("created").first();
    print("current_first.id : ", current_first.title);

    wm = MyShortCut.objects.create(
        author = request.user,
        title=title,
        filename=file_name,
        type= ty,
        category = ca,
        created = current_first.created-timedelta(seconds=10),
        content2 = ""
    )
    print("wm : ", wm)
    return JsonResponse({
        'message': 'textarea 박스 추가 성공',
        'shortcut_id':wm.id,
        'shortcut_title':wm.title,
        'shortcut_content2':wm.content2,
        # 'author':wm.author.username,
    })


# summer note 첫번째에 추가 하기
def create_summernote_first(request):
    print("create_summer_note")
    ty = Type.objects.get(type_name="summer_note")
    category_id = request.user.profile.selected_category_id
    ca = Category.objects.get(id=category_id)
    title = request.POST['title']
    file_name = request.POST['file_name']

    current_first = MyShortCut.objects.filter(Q(category=category_id) & Q(author=request.user)).order_by("created").first();
    print("current_first.id : ", current_first.title);

    wm = MyShortCut.objects.create(
        author = request.user,
        title=title,
        filename=file_name,
        type= ty,
        category = ca,
        created = current_first.created-timedelta(seconds=10),
        content2 = ""
    )

    print("wm : ", wm)
    return JsonResponse({
        'message': 'summer note 박스 추가 성공',
        'shortcut_id':wm.id,
        'shortcut_title':wm.title,
        'shortcut_content2':wm.content2,
    })

def create_new2_textarea(request):
    print("create_new2_textarea 실행")
    ty = Type.objects.get(type_name="textarea")
    category_id = request.user.profile.selected_category_id
    ca = Category.objects.get(id=category_id)
    title = request.POST['title']
    filename = request.POST['filename']
    author = request.user.username

    print("author : ", author)

    wm = MyShortCut.objects.create(
        author = request.user,
        title=title,
        filename=filename,
        type= ty,
        category = ca,
        created = datetime.now(),
        content2 = ""
    )
    print("wm : ", wm)
    return JsonResponse({
        'message': 'textarea 박스 추가 성공',
        'shortcut_id':wm.id,
        'shortcut_title':wm.title,
        'shortcut_content2':wm.content2,
        'filename':wm.filename,
        'author':author
    })

def create_new2_textarea_between(request,current_article_id):

    current_article_id = current_article_id
    current_article = MyShortCut.objects.get(id=current_article_id)
    print("current_article_time : " , current_article.created)

    smae_category_for_current_article=MyShortCut.objects.filter(author= current_article.author, category = current_article.category).order_by("created")

    same_category_id_array = []

    for i,p in enumerate(smae_category_for_current_article):
        # print('i',i)
        if (p.created <= current_article.created):
            MyShortCut.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=0))
        else:
            MyShortCut.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=i+1))


    print("create_new2_textarea 실행")
    ty = Type.objects.get(type_name="textarea")
    category_id = request.user.profile.selected_category_id
    ca = Category.objects.get(id=category_id)
    title = request.POST['title']

    wm = MyShortCut.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        created=current_article.created+timedelta(seconds=1.5),
        content2 = ""
    )
    print("wm : ", wm)
    return JsonResponse({
        'message': 'textarea 박스 추가 성공',
        'shortcut_id':wm.id,
        'shortcut_title':wm.title,
        'shortcut_content2':wm.content2,
    })

def update_category_by_ajax(request):
    shortcut_ids = request.POST.getlist('shortcut_arr[]')
    category = request.POST['category']
    # datetime.now()
    # if shortcut_ids:
    #     MyShortCut.objects.filter(pk__in=shortcut_ids, author=request.user).update(category=category, created = datetime.now())
    #     print('카테고리 수정 success')
    for i, sn in enumerate(shortcut_ids):
        MyShortCut.objects.filter(id=sn, author=request.user).update(category=category, created = datetime.now()+timedelta(seconds=i),image=F('image'))

    return redirect('/wm/myshortcut')

def delete_myshortcut_by_ajax(request):
    shortcut_ids = request.POST.getlist('shortcut_arr[]')
    if shortcut_ids:
        MyShortCut.objects.filter(pk__in=shortcut_ids, author=request.user).delete()

    return redirect('/wm/myshortcut')


def update_my_shortcut_subject(request):
    if request.method == "POST" and request.is_ajax():
        shortcut_subject = request.POST['shortcut_subject']

        print('update shortcut_subject : ',shortcut_subject)
        pf = Profile.objects.filter(user=request.user).update(subject_of_memo = shortcut_subject)

        print('shortcut_subject success : ' , shortcut_subject);

        return JsonResponse({
            'message': 'shortcut_subject update 성공 : ' +shortcut_subject
        })
    else:
        return redirect('/wm/shortcut')


def favorite_user_list_for_skillnote(request):
    if request.method == 'GET':
        print("user_list_for_memo 실행")

        my_favorite = []
        ru = RecommandationUserAboutSkillNote.objects.filter(author_id=request.user)

        for x in ru:
            print("내가 추천한 user_id : ",x.user_id)
            my_favorite.append(x.user_id)

        object_list = User.objects.filter(id__in=my_favorite).order_by('-profile__skill_note_reputation');

        print("object_list : ", object_list)


        return render(request, 'wm/favorite_user_list_for_skilnote.html', {
            "object_list" : object_list,
        })
    else:
        return HttpResponse("Request method is not a GET")


class user_list_for_memo_view(ListView):
    paginate_by = 10

    def get_template_names(self):
        if self.request.is_ajax():
            return ['wm/_user_list_for_memo.html']
        return ['wm/user_list_for_memo.html']

    def get_queryset(self):
        print("user_list_for_memo_view 확인")
        object_list = User.objects.all().order_by('-profile__skill_note_reputation');
        print("result : ", object_list)
        return object_list


def update_shortcut_nick(request):
    if request.method == "POST" and request.is_ajax():
        ca_id = int(request.POST['ca_id'])
        field = request.POST['field']
        ca_nick_update = request.POST['ca_nick_update']

        print('update id : ',ca_id)
        print('update field  : ',field)
        print('update value : ',ca_nick_update)
        cn = CategoryNick.objects.filter(id=ca_id).update(**{field: ca_nick_update})
        # .update(field = ca_nick_update)

        # print('update success : ' , update.id);

        return JsonResponse({
            'message': 'shortcut category nick name update 성공 ' +ca_nick_update,
        })
    else:
        return redirect('/wm/shortcut')

def update_shortcut_nick2(request):
    if request.method == "POST" and request.is_ajax():
        ca_id = CategoryNick.objects.get(author=request.user).id
        field = request.POST['field']
        ca_nick_update = request.POST['ca_nick_update']

        print('update id : ',ca_id)
        print('update field  : ',field)
        print('update value : ',ca_nick_update)

        cn = CategoryNick.objects.filter(id=ca_id).update(**{field: ca_nick_update})
        # .update(field = ca_nick_update)

        # print('update success : ' , update.id);

        return JsonResponse({
            'message': 'shortcut category nick name update 성공 ' +ca_nick_update,
        })
    else:
        return redirect('/wm/shortcut')


def CategoryNickListByUserId(request, user_name):
    if request.method == 'GET':
        print("user_name : ", user_name)
        user = User.objects.get(username=user_name)

        cn = CategoryNick.objects.get_or_create(
            author=user,
        )
        print("cn : ", cn)

        cn_my = CategoryNick.objects.get(author=user.id)
        print("cn_my : ", cn_my)

        return render(request, 'wm/categorynick_list.html', {
            "category" : cn_my
        })
    else:
        return HttpResponse("Request method is not a GET")

class modify_myshortcut_by_summer_note(UpdateView):
    model = MyShortCut
    form_class = MyShortCutForm_summer_note

    # def form_valid(self, form):
    #     form = form.save(commit=False)
    #     form.save()
    #     return super().form_valid(form)

    def get_template_names(self):
        return ['wm/myshortcut_summernote_form.html']


# 나의 shorcut id를 user list에서 클릭한 id로 교체
def update_shorcut_id_for_user(request, id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        user_id = request.POST['user_id']
        original_userId = id
        option=""
        original_user = ""

        print("id :", id)
        print("user_id : ", user_id)

        user_exist = User.objects.filter(username = user_id)
        original_user = user_id
        print("user_exist : ", user_exist)

        if user_exist:
            option = "메모장 유저를 " + user_id + "로 업데이트 하였습니다."
            todo = Profile.objects.filter(Q(user=request.user)).update(shortcut_user_id = user_id)
            print("메모장 유저를 {}로 교체 ".format(user_id))
        else:
            original_user = User.objects.get(id = original_userId).username
            print("original_user : ", original_user)
            option = user_id+ "유저가 없으므로 업데이트를 하지 않았습니다."
            print("유저를 업데이트 하지 않았습니다.")

        return JsonResponse({
            'message': option,
            'original_id': original_user
        })
    else:
        return redirect('/todo')

def update_shortcut1_ajax(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        content1 = request.POST.get('content1','')

        print('shortcut을 ajax로 update input')
        print('id : ', id)
        print("content1 : ", content1)
        todo = MyShortCut.objects.filter(Q(id=id)).update(content1 = content1)
        print('update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')

def update_shortcut2_ajax(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        print("content2 변수 넘어 왔다.")
        content2 = request.POST.get('content2','')
        # content2 = request.POST['content2']

        print('shortcut을 ajax로 update textarea')
        print('id : ', id)
        print("content2 : ", content2)
        todo = MyShortCut.objects.filter(Q(id=id)).update(content2 = content2)
        print('update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')


def myfunc():
    print("myfunc 실행")

class MyShortcutListByCategory(ListView):

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        pf = Profile.objects.filter(Q(user=self.request.user)).update(selected_category_id = category.id)
        print('category id update 성공')


        user = User.objects.get(Q(username = self.request.user.profile.shortcut_user_id))

        print('user : ' , user)

        return MyShortCut.objects.filter(category=category, author=user).order_by('created')

    def get_context_data(self, *, object_list=None, **kwargs):
        user = User.objects.get(Q(username = self.request.user.profile.shortcut_user_id))

        context = super(type(self), self).get_context_data(**kwargs)
        context['posts_without_category'] = MyShortCut.objects.filter(category=None,author=user).count()
        context['category_list'] = Category.objects.all()

        slug = self.kwargs['slug']
        if slug == '_none':
            context['category'] = '미분류'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category
            context['category_nick'] = CategoryNick.objects.values_list(slug, flat=True).get(author=user)

        return context


def delete_shortcut_ajax(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        todo = MyShortCut.objects.filter(Q(id=id)).delete()
        print('MyShortCut delete 성공 id : ' , id);
        return JsonResponse({
            'message': 'shortcut 삭제 성공',
        })
    else:
        return redirect('/todo')

def update_shortcut_ajax(request,id):
    user = request.user
    title = request.POST['title']

    if request.method == "POST" and request.is_ajax():
        todo = MyShortCut.objects.filter(Q(id=id)).update(title=title)
        print('MyShortCut update 성공 id : ' , id);
        return JsonResponse({
            'message': 'shortcut 업데이트 성공',
            'title':title
        })
    else:
        return redirect('/todo')

def update_skil_note_file_name(request,id):
    user = request.user
    file_name = request.POST['file_name']

    if request.method == "POST" and request.is_ajax():
        sn = MyShortCut.objects.filter(Q(id=id)).update(filename=file_name)
        print('filename update 성공 id : ' , sn);
        return JsonResponse({
            'message': 'file_name 업데이트 성공',
            'file_name':file_name
        })
    else:
        return redirect('/todo')

class MyShortCutListView(LoginRequiredMixin,ListView):
    model = MyShortCut
    paginate_by = 20
    user = 0

    def get_queryset(self):
        user = self.request.user.profile.shortcut_user_id
        # print("user : ", user)
        print("self.request.user : ", self.request.user)

        if user == "me":
            user = self.request.user
        else:
            user = User.objects.get(username=user)

        print("user : ", user)

        if self.request.user.is_anonymous:
            return MyShortCut.objects.filter(author=self.request.user).order_by('created')
        else:
            selected_category_id = self.request.user.profile.selected_category_id
            return MyShortCut.objects.filter(Q(author=user, category = selected_category_id)).order_by('created')

    def get_context_data(self, *, object_list=None, **kwargs):

            cn = CategoryNick.objects.get_or_create(
                author=self.request.user,
            )

            context = super(MyShortCutListView, self).get_context_data(**kwargs)
            context['category_list'] = Category.objects.all()

            category = Category.objects.get(id=self.request.user.profile.selected_category_id)
            context['category'] = category
            context['category_nick'] = CategoryNick.objects.values_list(category.slug, flat=True).get(author=self.request.user)

            context['posts_without_category'] = MyShortCut.objects.filter(category=None, author=self.request.user).count()
            # context['comments_list'] = CommentForShorCut.objects.all()

            return context

class MyShortCutCreateView_input(LoginRequiredMixin,CreateView):
    model = MyShortCut
    form_class = MyShortCutForm_input
    # fields = ['title','content1','category']

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행11")
        ty = Type.objects.get(type_name="input")
        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.type= ty
        category_id = self.request.user.profile.selected_category_id
        ca = Category.objects.get(id=category_id)
        ms.category = ca

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wm:my_shortcut_list')


class SkilNoteCreateView_image_through(LoginRequiredMixin,CreateView):
    model = MyShortCut
    form_class = MyShortCutForm_image

    def form_valid(self, form):
        print("through 입력 확인")

        # current_category_id = self.request.user.profile.selected_category_id
        current_article_id = self.kwargs['current_article_id']
        current_article = MyShortCut.objects.get(id=current_article_id)
        print("current_article_time : " , current_article.created)

        smae_category_for_current_article=MyShortCut.objects.filter(author= current_article.author, category = current_article.category).order_by("created")

        same_category_id_array = []

        for i,p in enumerate(smae_category_for_current_article):
            # print('i',i)
            if (p.created <= current_article.created):
                MyShortCut.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=0))
            else:
                MyShortCut.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=i+1))


        print("완료 명단 입력 뷰 실행2")
        ty = Type.objects.get(type_name="image")
        print("ty : ", ty)
        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.created=current_article.created+timedelta(seconds=1.5)
        ms.type= ty
        category_id = self.request.user.profile.selected_category_id
        ca = Category.objects.get(id=category_id)
        ms.category = ca

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wm:my_shortcut_list')

class MyShortCutCreateView_image(LoginRequiredMixin,CreateView):
    model = MyShortCut
    form_class = MyShortCutForm_image
    # fields = ['title','content1','category']

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행2")
        ty = Type.objects.get(type_name="image")
        print("ty : ", ty)
        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.created=timezone.now()
        ms.type= ty
        category_id = self.request.user.profile.selected_category_id
        ca = Category.objects.get(id=category_id)
        ms.category = ca

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wm:my_shortcut_list')


class MyShortCutCreateView_textarea(LoginRequiredMixin,CreateView):
    model = MyShortCut
    fields = ['title','content2']

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행2")

        ty = Type.objects.get(type_name="textarea")

        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.type= ty

        category_id = self.request.user.profile.selected_category_id
        ca = Category.objects.get(id=category_id)
        ms.category = ca

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wm:my_shortcut_list')

class MyShortCutCreateView_textarea_summer_note(LoginRequiredMixin,CreateView):
    model = MyShortCut
    form_class = MyShortCutForm_summer_note

    def get_template_names(self):
        return ['wm/myshortcut_summernote_form.html']

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행4")

        ty = Type.objects.get(type_name="summer_note")

        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.type= ty
        ms.created = timezone.now()

        category_id = self.request.user.profile.selected_category_id
        ca = Category.objects.get(id=category_id)
        ms.category = ca

        return super().form_valid(form)

    # def get_success_url(self):
    #     return self.post.get_absolute_url()+'#skil-note-id-{}'.format(self.obejcts.pk)



class SkilNoteCreateView_summernote_through(LoginRequiredMixin,CreateView):
    model = MyShortCut
    form_class = MyShortCutForm_summer_note

    def get_template_names(self):
        return ['wm/myshortcut_summernote_form.html']

    def form_valid(self, form):
        print("through 입력 확인")

        # current_category_id = self.request.user.profile.selected_category_id
        current_article_id = self.kwargs['current_article_id']
        current_article = MyShortCut.objects.get(id=current_article_id)
        print("current_article_time : " , current_article.created)

        smae_category_for_current_article=MyShortCut.objects.filter(author= current_article.author, category = current_article.category).order_by("created")

        same_category_id_array = []

        for i,p in enumerate(smae_category_for_current_article):
            # print('i',i)
            if (p.created <= current_article.created):
                MyShortCut.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=0))
            else:
                MyShortCut.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=i+1))


        print("same_category_id_array : ",same_category_id_array)

        ty = Type.objects.get(type_name="summer_note")

        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.created=current_article.created+timedelta(seconds=1.5)
        ms.type= ty

        category_id = self.request.user.profile.selected_category_id
        ca = Category.objects.get(id=category_id)
        ms.category = ca

        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('wm:my_shortcut_list')
