from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import *
from django.db.models import Q
from .models import *


# Create your views here.

def index(request):
    posts = Post.objects.all()
    kategoriler = Kategori.objects.all()
    
    context={
            'kategoriler' :kategoriler,
            'posts' : posts 
        }

    return render(request , 'anasayfa.html' , context)

def filter(request):
    kategoriler = Kategori.objects.all()

    if 'filtre' in request.POST:
        minprice = request.POST['min_price']
        maxprice = request.POST['max_price']
        kategori = request.POST['kategori']
        location = request.POST['location']
        print(minprice,minprice)
        posts = Post.objects.filter(
            Q(fiyat__range = (minprice,maxprice)) &
            Q(location__contains = location ) &
            Q(kategori__isim__contains = kategori ) 
        )
    
    context={
        'kategoriler' :kategoriler,
        'posts' : posts
    }
    return render(request , 'filter.html' , context)

def kategori(request,slug):
    kategoriler = Kategori.objects.all()
    
    posts= Post.objects.filter(kategori__slug=slug)
    # posts = Post.objects.filter()
    context={
            'posts' :posts,
            'kategoriler' : kategoriler
        }
    return render(request , 'kategori.html',context)

def loginregister(request):

    
    if 'üye' in request.POST:
        email = request.POST["email"]
        username = request.POST["username"]
        sifre1 = request.POST["sifre1"]
        sifre2 = request.POST["sifre2"]

        
        if sifre1 ==  sifre2 :
            if User.objects.filter(username = username).exists():
                messages.error(request,'Kullanıcı adı kullanılıyor')
                return redirect("loginregister")
            elif User.objects.filter(email = email).exists():
                messages.error(request,'Email kullanılıyor')
                return redirect("loginregister")
            elif len(sifre1) < 6 :
                messages.error(request , 'Şifre en az 6 karakter olmalıdır')
                return redirect("loginregister")
            else:
                user = User.objects.create_user(username = username , email = email , password = sifre1 )
                Profil.objects.create(
                kullanici = user ,
            )
                user.save()
                messages.success(request,'Kayıt başarı ile gerçekleşti')
                return redirect('anasayfa')
        else :
            messages.error(request,'Şifreler uyuşmuyor')
            return redirect("loginregister")

    if 'giris' in request.POST:
            username1 = request.POST['username1']
            sifre3 = request.POST['sifre3']

            user = authenticate (request , username = username1 , password = sifre3)
            if user is not None :
                login(request , user)
                messages.success(request , 'Giriş')
                return redirect('anasayfa')
                    
            else:
                messages.error(request, "Parola ya da kullanıcı adı yanlış")
                return redirect ("loginregister")

    kategoriler = Kategori.objects.all()
    context = {
        'kategoriler' :kategoriler
    }

    return render(request , 'loginregister.html' ,context)

def logout_request (request):
    logout(request)
    return redirect ('anasayfa')

def profil(request):
    return render(request,'profil.html')


def detay(request , postId):
    postDetay = Post.objects.get(slug = postId)
    context = {
        'postDetay' : postDetay
    }
    return render(request , 'detail.html' ,context)


def host(request):
    return render(request , "host.html")

def postForm(request):
    kategoriler = Kategori.objects.all()

    if request.method == 'POST':
        
        evName = request.POST['evName']
        kategoriId = request.POST['kategori']
        uzaklık = request.POST['uzaklık']
        price = request.POST['price']
        info = request.POST['info']
        country = request.POST['country']
        pic1 = request.FILES['pic1']
        pic2 = request.FILES['pic2']
        pic3 = request.FILES['pic3']
        pic4 = request.FILES['pic4']
        pic5 = request.FILES['pic5']
        kategori = Kategori.objects.get(id =kategoriId)
        post = Post.objects.create( isim = evName , 
                                evsahibi = request.user,
                                kategori=kategori,
                                uzaklik = uzaklık,
                                location = country,
                                fiyat = price,
                                bilgi = info,
                                resim1 = pic1,
                                resim2 = pic2,
                                resim3 = pic3,
                                resim4 = pic4,
                                resim5 = pic5
                                           )
        
        post.save()
        messages.success(request,'Eviniz paylaşıldı')
        return redirect('anasayfa')
    context={
            'kategoriler' :kategoriler,
        }
    return render(request,'postForm.html',context)


def hesap(request):
    return render(request , 'hesap/hesap.html')

def hesapKisisel(request):
    user = request.user.profil
    form = HesapForm(instance=user)
    if request.method == 'POST':
        form = HesapForm(request.POST,request.FILES,instance = user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profil bilgileri güncellendi')
            return redirect('hesap')
    context = {
        'form':form
    }
    return render(request ,'hesap/kisisel-bilgiler.html',context)

def guvenlik(request):
    user = request.user
    if request.method == 'POST':
        eski = request.POST['eski']
        yeni1 = request.POST['yeni1']
        yeni2 = request.POST['yeni2']

        yeni = authenticate(request,username=user,password=eski)

        if yeni is not None:
            if yeni1 == yeni2:
                user.set_password(yeni1)
                user.save()
                messages.success(request,'Şifrenis değiştirildi')
                return redirect('anasayfa')
            else:
                messages.error(request,'Şifreler uyuşmuyor')
        else:
            messages.error(request,'Mevcut şifreniz hatalı')  
    return render(request ,'hesap/güvenlik.html')

def payment(request):
    return render(request,'hesap/ödeme.html')

def vergiler(request):
    return render(request,'hesap/vergiler.html')

def bildirim(request):
    return render(request,'hesap/bildirimler.html')

def gizlilik(request):
    return render(request,'hesap/gizlilik.html')

def tercihler(request):
    return render(request,'hesap/tercihler.html')

def seyehat(request):
    return render(request,'hesap/seyehat.html')

def sahiplik(request):
    return render(request,'hesap/ev-sahipliği.html')

def misafir(request):
    return render(request,'hesap/misafir.html')
