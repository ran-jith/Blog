from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

def post_list(request):
    object_list = Post.published.all()

    #need a template to displaying paginator properly
    paginator = Paginator(object_list, 3) #3 posts in each Page
    page = request.GET.get('page') #current page number
    try:
        posts = paginator.page(page)#get desired page
    except PageNotAnInteger:
        #if page not an integer deliver the first Page
        posts = paginator.page(1)
    except EmptyPage:
        #if page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html',
                  {'page':page,
                  'posts':posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                    status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post':post})


#class based view below
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

#..........
def post_share(request, post_id): #retrieve post by # id
    post = get_object_or_404(Post, id=post_id, status='published')#make sure retrieved post has published status
    sent = False

    if request.method == 'POST':
        #form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #form field passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'ranjithakalurkk@gmail.com', [cd['to']])
            sent = True

            #....send email

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post,
                                                        'form':form,
                                                        'sent':sent })
