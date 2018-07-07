from django.shortcuts import render, get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.db.models import Count
from haystack.query import SearchQuerySet


def post_list(request, tag_slug=None):#tag_slug parametr come in url
    object_list = Post.published.all()#query
    tag = None

    if tag_slug: #if any data retrieve from above query
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])#filter list of posts that containing the tags

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
                   'posts':posts,
                   'tag':tag})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                    status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)

    #list of active comments for this post
    comments = post.comments.filter(active=True) #retrive all comments for ths post

    if request.method == 'POST':
        #a comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #create comment object but dont save to db yet
            new_comment = comment_form.save(commit=False)
            #assign the current post to comment
            new_comment.post = post
            #save the comment to db
            new_comment.save()
    else:
        comment_form = CommentForm()

    #List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)#get all posts contain same tag excluding the current one
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]



    return render(request,
                  'blog/post/detail.html',
                  {'post':post,
                   'comments':comments,
                   'comment_form':comment_form,
                   'similar_posts':similar_posts})


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


def post_search(request):
    form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all()
            #count total results
            total_results = results.count()
        return render(request, 'blog/post/search.html', {'form':form, 'cd':cd, 'results':results, 'total_results':total_results})
    return render(request, 'blog/post/search.html', {'form': form,})
