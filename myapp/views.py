from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from myapp.models import *


def logout_page(request):
    logout(request)
    return redirect('/myapp/login_page/')

def public_page(request):
    return render(request,'publicpage.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        ob = authenticate(request, username=username, password=password)

        if ob is not None:

            if ob.groups.filter(name="Admin").exists():
                login(request, ob)
                return redirect('/myapp/admin_home/')


            else:
                messages.warning(
                    request,
                    'Invalid Username and password'
                )
                return redirect('/myapp/login_page/')

        messages.warning(
            request,
            'Invalid Person'
        )
        return redirect('/myapp/login_page/')
    return render(request, 'loginpage.html')


def admin_home(request):
    return render(request,'admin/admin_home.html')

def admin_home_sub(request):
    return render(request,'admin/admin_home sub.html')

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if not user.check_password(old_password):
            messages.error(request, 'Old password is incorrect')
            return redirect('/myapp/change_password/')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match')
            return redirect('/myapp/change_password/')

        if len(new_password) < 8:
            messages.error(request, 'Password must contain at least 8 characters')
            return redirect('/myapp/change_password/')

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        messages.success(request, 'Password changed successfully')
        return redirect('/myapp/login_page/')

    return render(request, 'admin/change_password.html')





@login_required
def manage_users(request):
    users = User_Table.objects.select_related('LOGIN').all().order_by('-created_at')

    return render(request, 'admin/manage_users.html', {
        'users': users
    })




@login_required
def view_reels(request):
    reels = Reel.objects.select_related('user').all().order_by('-created_at')

    return render(request, 'admin/view_reels.html', {
        'reels': reels
    })





from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .models import Complaint


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Complaint


@login_required
def view_complaints(request):
    complaints = (
        Complaint.objects
        .select_related('user', 'replied_by')
        .order_by('-created_at')
    )
    return render(request, 'admin/view_complaints.html', {
        'complaints': complaints
    })


@login_required
def reply_complaint(request, complaint_id):
    complaint = get_object_or_404(
        Complaint,
        id=complaint_id,
        status='pending'
    )

    if request.method == 'POST':
        reply = request.POST.get('reply', '').strip()

        if not reply:
            messages.error(request, 'Reply cannot be empty.')
            return redirect('reply_complaint', complaint_id=complaint.id)

        complaint.reply_text = reply
        complaint.status = 'in_progress'
        complaint.replied_by = request.user
        complaint.replied_at = timezone.now()
        complaint.save()

        messages.success(request, 'Reply sent successfully.')
        return redirect('view_complaints')

    return render(request, 'admin/reply_complaint.html', {
        'complaint': complaint
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Feedback


@login_required
def view_feedback(request):
    feedbacks = Feedback.objects.select_related(
        'user'
    ).all().order_by('-created_at')

    return render(request, 'admin/view_feedback.html', {
        'feedbacks': feedbacks
    })








# =============flutter=====================
from django.utils import timezone


def update_location(request):

    lid = request.POST.get("lid")
    lat = request.POST.get("lat")
    lon = request.POST.get("lon")

    if not lid:
        return JsonResponse({
            "status": "error",
            "message": "Login ID missing"
        }, status=400)

    if not lat or not lon:
        return JsonResponse({
            "status": "error",
            "message": "Latitude or longitude missing"
        }, status=400)


    dobj, created = User_Table.objects.get_or_create(
        LOGIN_id=lid,
        defaults={
            "latitude": float(lat),
            "longitude": float(lon),
        }
    )

    if not created:
        dobj.latitude = float(lat)
        dobj.longitude = float(lon)
        dobj.save()

    return JsonResponse({
        "status": "ok",
        "message": "Location updated successfully",
        "latitude": lat,
        "longitude": lon
    })


def app_login(request):
    if request.method != "POST":
        return JsonResponse({
            'status': 'error',
            'message': 'POST method required'
        })

    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '').strip()

    if not username or not password:
        return JsonResponse({
            'status': 'error',
            'message': 'Username and password required'
        })

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is None:
        return JsonResponse({
            'status': 'no',
            'message': 'Invalid username or password'
        })



    if user.groups.filter(name="User").exists():

        login(request, user)

        return JsonResponse({
            'status': 'ok',
            'lid': str(user.id),
            'type': 'User'
        })



    return JsonResponse({
        'status': 'no',
        'message': 'User type not recognized'
    })



def user_register(request):
    name = request.POST['name']
    profile_picture = request.FILES.get('profile_picture')
    region = request.POST['region']
    place = request.POST['place']
    phone = request.POST['phone']
    email = request.POST['email']
    dob = request.POST['dob']
    district = request.POST['district']
    username = request.POST['username']
    password = request.POST['password']
    latitude = request.POST.get('latitude') or None
    longitude = request.POST.get('longitude') or None

    if User.objects.filter(username=username).exists():
        return JsonResponse({'status': 'no'})

    if User.objects.filter(email=email).exists():
        return JsonResponse({'status': 'no'})

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    group = Group.objects.get(name="User")
    user.groups.add(group)

    ert = User_Table()
    ert.LOGIN = user
    ert.profile_picture = profile_picture
    ert.region = region
    ert.status = 'active'
    ert.name = name
    ert.dob = dob
    ert.email = email
    ert.place = place
    ert.district = district
    ert.latitude = latitude
    ert.longitude = longitude
    ert.phone = phone
    ert.save()

    return JsonResponse({'status': 'ok'})



def view_profile(request):
    login_id = request.GET.get('lid')

    if not login_id:
        return JsonResponse({
            'status': 'no',
            'message': 'Login ID required'
        })

    try:
        user = User.objects.get(id=login_id)
        profile = User_Table.objects.get(LOGIN=user)

        profile_picture_url = None

        if profile.profile_picture:
            profile_picture_url = request.build_absolute_uri(
                profile.profile_picture.url
            )

        return JsonResponse({
            'status': 'ok',
            'data': {
                'login_id': user.id,
                'username': user.username,
                'name': profile.name,
                'profile_picture': profile_picture_url,
                'phone': profile.phone,
                'email': profile.email,
                'dob': str(profile.dob) if profile.dob else '',
                'place': profile.place,
                'district': profile.district,
                'region': profile.region,
                'latitude': profile.latitude,
                'longitude': profile.longitude,
                'status': profile.status,
            }
        })

    except (User.DoesNotExist, User_Table.DoesNotExist):
        return JsonResponse({
            'status': 'no',
            'message': 'Profile not found'
        })


def update_profile(request):
    if request.method != 'POST':
        return JsonResponse({
            'status': 'no',
            'message': 'POST method required'
        })

    login_id = request.POST.get('lid')

    if not login_id:
        return JsonResponse({
            'status': 'no',
            'message': 'Login ID required'
        })

    try:
        user = User.objects.get(id=login_id)
        profile = User_Table.objects.get(LOGIN=user)

        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        dob = request.POST.get('dob', '').strip()
        place = request.POST.get('place', '').strip()
        district = request.POST.get('district', '').strip()
        region = request.POST.get('region', '').strip()
        latitude = request.POST.get('latitude', '').strip()
        longitude = request.POST.get('longitude', '').strip()

        if not all([
            name, phone, email, dob,
            place, district, region
        ]):
            return JsonResponse({
                'status': 'no',
                'message': 'Please fill all required fields'
            })

        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                'status': 'no',
                'message': 'Invalid email'
            })

        if User.objects.filter(email__iexact=email).exclude(
            id=user.id
        ).exists():
            return JsonResponse({
                'status': 'no',
                'message': 'Email already exists'
            })

        try:
            lat = float(latitude) if latitude else None
            lon = float(longitude) if longitude else None
        except ValueError:
            return JsonResponse({
                'status': 'no',
                'message': 'Invalid latitude or longitude'
            })

        user.email = email
        user.save()

        profile.name = name
        profile.phone = phone
        profile.email = email
        profile.dob = dob
        profile.place = place
        profile.district = district
        profile.region = region
        profile.latitude = lat
        profile.longitude = lon

        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()

        profile_picture_url = None

        if profile.profile_picture:
            profile_picture_url = request.build_absolute_uri(
                profile.profile_picture.url
            )

        return JsonResponse({
            'status': 'ok',
            'message': 'Profile updated successfully',
            'data': {
                'login_id': user.id,
                'username': user.username,
                'name': profile.name,
                'profile_picture': profile_picture_url,
                'phone': profile.phone,
                'email': profile.email,
                'dob': str(profile.dob) if profile.dob else '',
                'place': profile.place,
                'district': profile.district,
                'region': profile.region,
                'latitude': profile.latitude,
                'longitude': profile.longitude,
                'status': profile.status,
            }
        })

    except (User.DoesNotExist, User_Table.DoesNotExist):
        return JsonResponse({
            'status': 'no',
            'message': 'Profile not found'
        })







def user_change_password(request):
    id = request.POST['lid']
    current_password = request.POST['old_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']
    res = User.objects.get(id=id)
    if res.check_password(current_password):
        if new_password == confirm_password:
            res.set_password(new_password)
            res.save()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status': 'no'})

def user_send_feedback(request):
    lid = request.POST['lid']
    feedback_text = request.POST['feedback_text']
    rating = request.POST['rating']

    user = User_Table.objects.get(LOGIN_id=lid)

    Feedback.objects.create(
        user=user,
        feedback_text=feedback_text,
        rating=rating
    )

    return JsonResponse({'status': 'ok'})


def user_send_complaint(request):
    lid = request.POST['lid']
    complaint_text = request.POST['complaint_text']

    user = User_Table.objects.get(LOGIN_id=lid)



    Complaint.objects.create(
        user=user,
        complaint_text=complaint_text,
        reply_text='pending',
    )

    return JsonResponse({'status': 'ok'})

def user_view_complaints(request):
    lid = request.GET.get('lid')

    user = User_Table.objects.get(LOGIN_id=lid)

    complaints = Complaint.objects.filter(
        user=user
    ).order_by('-created_at')

    data = []

    for c in complaints:
        data.append({
            'id': c.id,
            'complaint_text': c.complaint_text,
            'reply_text': c.reply_text,
            'status': c.status,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'replied_at': (
                c.replied_at.strftime('%Y-%m-%d %H:%M:%S')
                if c.replied_at else None
            )
        })

    return JsonResponse({
        'status': 'ok',
        'data': data
    })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import User_Table, Follow


# 1. View Other Users
def view_other_users(request):
    if request.method == 'GET':
        lid = request.GET.get('lid')

        if not lid:
            return JsonResponse({
                'status': 'error',
                'message': 'Login ID is required'
            })

        try:
            current_user = User_Table.objects.get(LOGIN_id=lid)
        except User_Table.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User not found'
            })

        users = User_Table.objects.exclude(
            id=current_user.id
        ).order_by('name')

        data = []

        for u in users:
            is_following = Follow.objects.filter(
                follower=current_user,
                following=u
            ).exists()

            follows_you = Follow.objects.filter(
                follower=u,
                following=current_user
            ).exists()

            if is_following:
                button = 'Following'
            elif follows_you:
                button = 'Follow Back'
            else:
                button = 'Follow'

            data.append({
                'id': u.id,
                'login_id': u.LOGIN_id,
                'name': u.name,
                'profile_picture': request.build_absolute_uri(
                    u.profile_picture.url
                ) if u.profile_picture else '',
                'region': u.region,
                'place': u.place,
                'district': u.district,
                'is_following': is_following,
                'follows_you': follows_you,
                'button': button
            })

        return JsonResponse({
            'status': 'ok',
            'count': len(data),
            'data': data
        })

    return JsonResponse({
        'status': 'error',
        'message': 'GET method required'
    })


# 2. Follow / Follow Back
def user_follow(request):
    if request.method == 'POST':
        lid = request.POST.get('lid')
        user_id = request.POST.get('user_id')

        if not lid or not user_id:
            return JsonResponse({
                'status': 'error',
                'message': 'lid and user_id are required'
            })

        try:
            follower = User_Table.objects.get(LOGIN_id=lid)
            following = User_Table.objects.get(id=user_id)
        except User_Table.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User not found'
            })

        if follower.id == following.id:
            return JsonResponse({
                'status': 'error',
                'message': 'You cannot follow yourself'
            })

        obj, created = Follow.objects.get_or_create(
            follower=follower,
            following=following
        )

        return JsonResponse({
            'status': 'ok',
            'message': 'Followed successfully' if created
                       else 'Already following',
            'is_following': True,
            'button': 'Following'
        })

    return JsonResponse({
        'status': 'error',
        'message': 'POST method required'
    })


# 3. Unfollow
def user_unfollow(request):
    if request.method == 'POST':
        lid = request.POST.get('lid')
        user_id = request.POST.get('user_id')

        if not lid or not user_id:
            return JsonResponse({
                'status': 'error',
                'message': 'lid and user_id are required'
            })

        try:
            current_user = User_Table.objects.get(LOGIN_id=lid)
        except User_Table.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User not found'
            })

        deleted_count, _ = Follow.objects.filter(
            follower=current_user,
            following_id=user_id
        ).delete()

        return JsonResponse({
            'status': 'ok',
            'message': 'Unfollowed successfully'
                       if deleted_count else 'You are not following this user',
            'is_following': False,
            'button': 'Follow'
        })

    return JsonResponse({
        'status': 'error',
        'message': 'POST method required'
    })



def view_followers(request):
    if request.method == 'GET':
        lid = request.GET.get('lid')

        if not lid:
            return JsonResponse({
                'status': 'error',
                'message': 'Login ID is required'
            })

        try:
            current_user = User_Table.objects.get(LOGIN_id=lid)
        except User_Table.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User not found'
            })

        follows = Follow.objects.filter(
            following=current_user
        ).select_related('follower').order_by('-created_at')

        data = []

        for f in follows:
            u = f.follower

            is_following = Follow.objects.filter(
                follower=current_user,
                following=u
            ).exists()

            data.append({
                'id': u.id,
                'login_id': u.LOGIN_id,
                'name': u.name,
                'profile_picture': request.build_absolute_uri(
                    u.profile_picture.url
                ) if u.profile_picture else '',
                'is_following': is_following,
                'follows_you': True,
                'button': 'Following' if is_following else 'Follow Back'
            })

        return JsonResponse({
            'status': 'ok',
            'count': len(data),
            'data': data
        })

    return JsonResponse({
        'status': 'error',
        'message': 'GET method required'
    })



def view_following(request):
    if request.method == 'GET':
        lid = request.GET.get('lid')

        if not lid:
            return JsonResponse({
                'status': 'error',
                'message': 'Login ID is required'
            })

        try:
            current_user = User_Table.objects.get(LOGIN_id=lid)
        except User_Table.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User not found'
            })

        follows = Follow.objects.filter(
            follower=current_user
        ).select_related('following').order_by('-created_at')

        data = []

        for f in follows:
            u = f.following

            data.append({
                'id': u.id,
                'login_id': u.LOGIN_id,
                'name': u.name,
                'profile_picture': request.build_absolute_uri(
                    u.profile_picture.url
                ) if u.profile_picture else '',
                'is_following': True,
                'follows_you': Follow.objects.filter(
                    follower=u,
                    following=current_user
                ).exists(),
                'button': 'Unfollow'
            })

        return JsonResponse({
            'status': 'ok',
            'count': len(data),
            'data': data
        })

    return JsonResponse({
        'status': 'error',
        'message': 'GET method required'
    })



def view_follow_counts(request):
    if request.method == 'GET':
        lid = request.GET.get('lid')

        if not lid:
            return JsonResponse({
                'status': 'error',
                'message': 'Login ID is required'
            })

        try:
            current_user = User_Table.objects.get(LOGIN_id=lid)
        except User_Table.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User not found'
            })

        followers_count = Follow.objects.filter(
            following=current_user
        ).count()

        following_count = Follow.objects.filter(
            follower=current_user
        ).count()

        return JsonResponse({
            'status': 'ok',
            'followers_count': followers_count,
            'following_count': following_count
        })

    return JsonResponse({
        'status': 'error',
        'message': 'GET method required'
    })
