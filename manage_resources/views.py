from django.shortcuts import render,redirect
from django.contrib import messages
from manage_resources.models import Usuarios,Productos,Carrito,Compras
from werkzeug.security import generate_password_hash,check_password_hash
import datetime 
import time

# Create your views here.

# MAIN PAGE
def renderIndex(request):
    session = request.session.get('user')
    if session:
        usuario=Usuarios.objects.get(id=session)
        productos=Productos.objects.all()
        
        return render(request,'index.html',{'session':session,'usuario':usuario,'productos':productos})
    else:
        productos=Productos.objects.all()
        return render(request,'index.html',{'productos':productos})

# ABOUT US
def renderUs(request):
    session = request.session.get('user')
    if session:
        usuario=Usuarios.objects.get(id=session)
        return render(request,'nosotros.html',{'us':True,'session':session,'usuario':usuario})
    else:    
        return render(request,'nosotros.html',{'us':True})

#CONTACTUS
def renderContact(request):
    session = request.session.get('user')
    if session:
        usuario=Usuarios.objects.get(id=session)
        return render(request,'contactanos.html',{'contactus':True,'session':session,'usuario':usuario})
    else:    
        return render(request,'contactanos.html',{'contactus':True})

# LOGIN
def renderLogin(request):
    session = request.session.get('user')
    if session:
        return redirect('/index/')
    else:
        if request.method=='POST':
            email = request.POST['email']
            password = request.POST['password']
            if email and password:
                user = Usuarios.objects.filter(email=email).get()
                if user:
                    if check_password_hash(user.password,password):
                        request.session['user']=user.id
                        messages.add_message(request,messages.SUCCESS,'Inicio Sesión Correctamente')
                        return redirect('/index/')
                    else:
                        messages.add_message(request,messages.ERROR,'Error, contraseña no coincide')
                else:
                    messages.add_message(request,messages.ERROR,'Correo no registrado')
            else:
                messages.add_message(request,messages.ERROR,'Complete todos los campos')
            return redirect('/login/')
        else:
            return render(request,'login.html',{'login':True})

# CREATE A NEW USER:
def renderRegister(request):
    if request.method=='POST':
        name=request.POST['name']
        lastname=request.POST['lastname']
        email=request.POST['email']
        phone=request.POST['phone']
        address=request.POST['address']
        password=request.POST['password']
        password_confirmed=request.POST['password_confirmed']
        if name and lastname and email and phone and address and password and password_confirmed:
            if len(password)<8:
                messages.add_message(request,messages.ERROR,'La contraseña debe tener al menos 8 caracteres')
            else:
                if password!=password_confirmed:
                    messages.add_message(request,messages.ERROR,'La contraseña no coinciden')
                else:
                    pass_hashed=generate_password_hash(password)
                    newUser = Usuarios(name=name,lastname=lastname,address=address,phone=phone,email=email,password=pass_hashed)
                    newUser.save()
                    messages.add_message(request,messages.SUCCESS,'Registro nuevo usuario satisfactoriamente')
                    return redirect('/login/')
            return redirect('/register/')
        else:
            messages.add_message(request,messages.ERROR,'Complete todos los campos')
            return redirect('/register/')
    else:
        return render(request,'register.html',{'register':True})

#FORMULARIO Y CREATE NEW PRODUCT
def addProduct(request):
    session = request.session.get('user')
    if session:
        if request.method=='POST':
            name=request.POST['name']
            section=request.POST['section']
            price=request.POST['price']
            image_prod=request.POST['image_product']
            amount=request.POST['amount']
            newProduct = Productos(name=name,section=section,price=price,image_url=image_prod,amount=amount)
            newProduct.save()
            messages.add_message(request,messages.SUCCESS,'Nuevo producto agregado con exito')
            return redirect('/index/')
        else:
            usuario = Usuarios.objects.get(id=session)
            return render(request,'user/product-form.html',{'session':session,'usuario':usuario})
    else:
        messages.add_message(request,messages.ERROR,'Inicie Sesión para continuar')


#DELETE PRODUCT:
def deleteProduct(request,id):
    session = request.session.get('user')
    if session:
        producto=Productos.objects.get(id=id)
        producto.delete()
        messages.add_message(request,messages.SUCCESS,'Elimino producto satisfactoriamente')
        return redirect('/index/')
    else:
        messages.add_message(request,messages.ERROR,'Inicie Sesión para continuar')
        return redirect('/login/')

#EDIT PRODUCT:
def updateProduct(request,id):
    session = request.session.get('user')
    if session:
        usuario = Usuarios.objects.get(id=session)
        producto=Productos.objects.get(id=id)
        if request.method=='POST':
            price=request.POST['price']
            image_prod=request.POST['image_product']
            amount=request.POST['amount']
            producto.price=price
            producto.save()
            producto.image_url=image_prod
            producto.save()
            producto.amount= amount
            producto.save()
            messages.add_message(request,messages.SUCCESS,'Producto actualizado Satisfactoriamente')
            return redirect('/index/')
        else:    
            return render(request,'user/product-form.html',{'session':session,'usuario':usuario,'producto':producto,'edit':True})
    else:
        messages.add_message(request,messages.ERROR,'Inicie Sesión para continuar')
        return redirect('/login/')

#SEE ALL USERS
def getUsers(request):
    session = request.session.get('user')
    if session:
        usuario=Usuarios.objects.get(id=session)
        usuarios = Usuarios.objects.all()
        return render(request,'user/contacts-list.html',{'session':session,'usuario':usuario,'usuarios':usuarios})
    else:
        messages.add_message(request,messages.ERROR,'Inicie Sesión para continuar')
        return redirect('/login/')


#RENDER TO CARRITO
def renderCarrito(request):
    session = request.session.get('user')
    if session:
        pedido=[]
        preciototal = 0
        usuario = Usuarios.objects.get(id=session)
        carrito = Carrito.objects.filter(iduser=session).filter(status=False).values()
        for i in range(len(carrito)):
            producto = Productos.objects.get(id=carrito[i]['idproduct'])
            preciototal = preciototal + int(producto.price)*int(carrito[i]['amount'])
            pedido.append({ 'idcarrito':carrito[i]['id'],
                            'idproducto':producto.id,
                            'name':producto.name,
                            'price':producto.price,
                            'image':producto.image_url,
                            'amount':carrito[i]['amount']})
        
        return render(request,'user/carrito.html',{'session':session,'usuario':usuario,'elementos':pedido,'totalprice':preciototal})
    else:
        messages.add_message(request,messages.ERROR,'Inicie Sesión para continuar')
        return redirect('/login/')

def deleteFromCarrito(request,id):
    session = request.session.get('user')
    if session:
        elemento = Carrito.objects.get(id=id)
        producto = Productos.objects.get(id=elemento.idproduct)
        producto.amount = int(producto.amount) + int(elemento.amount)
        producto.save()
        elemento.delete()
        messages.add_message(request,messages.SUCCESS,'Elimino producto del carrito satisfactoriamente')
        return redirect('/carrito/')
    else:
        messages.add_message(request,messages.ERROR,'Inicie Sesión para continuar')
        return redirect('/login/')


def renderProfile(request):
    session = request.session.get('user')
    if session:
        usuario = Usuarios.objects.get(id=session)
        return render(request,'user/profile.html',{'session':session,'usuario':usuario})
    else:
        messages.add_message(request,messages.ERROR,'Inicie Sesión para continuar')
        return redirect('/login/')

def renderChangePassword(request):
    session = request.session.get('user')
    if session:
        usuario = Usuarios.objects.get(id=session)
        if request.method == 'POST':
            password = request.POST['password']
            password_confirmed = request.POST['password_confirmed']
            if password and password_confirmed:
                if password!=password_confirmed:
                    messages.add_message(request,messages.ERROR,'Las contraseñas no coinciden')
                else:
                    if len(password)<8:
                        messages.add_message(request,messages.ERROR,'La contraseña debe tener al menos 8 caracteres')
                    else:
                        usuario.password = generate_password_hash(password)
                        usuario.save()
                        messages.add_message(request,messages.SUCCESS,'Cambio su contraseña satisfactoriamente')
                        del request.session['user']
                        return redirect('/login/')
            else:
                messages.add_message(request,messages.ERROR,'Complete los campos para continuar')
            return redirect('/cambiarcontrasena/')
        else:
            return render(request,'user/reset-pass.html',{'session':session,'usuario':usuario})
    else:
        messages.add_message(request,messages.ERROR,'Inicie Sesión para continuar')
        return redirect('/login/')

def renderEditProfile(request):
    session = request.session.get('user')
    if session:
        usuario = Usuarios.objects.get(id=session)
        if request.method == 'POST':
            email = request.POST['email']
            phone = request.POST['phone']
            address = request.POST['address']
            if email and phone and address:
                usuario.email = email
                usuario.save()
                usuario.phone = phone
                usuario.save()
                usuario.address = address
                usuario.save()
                messages.add_message(request,messages.SUCCESS,'Cambio sus datos satisfactoriamente')
                return redirect('/perfil/')
            else:
                messages.add_message(request,messages.ERROR,'Complete los campos para continuar')
                return redirect('/editarperfil/')
        else:
            return render(request,'user/edit-profile.html',{'session':session,'usuario':usuario})
    else:
        messages.add_message(request,messages.ERROR,'Inicie Sesión para continuar')
        return redirect('/login/')

#ADD CARBUY
def addCarrito(request,id):
    session = request.session.get('user')
    if session:
        producto = Productos.objects.get(id=id)
        amount=request.POST['amount']
        if amount and producto:
            carrito = Compras.objects.filter(date=datetime.date.today()).filter(iduser=session)
            if carrito:
                messages.add_message(request,messages.INFO,'Solo puede realizar una compra por día')
                return redirect('/index/')
            else:
                carrito = Carrito(iduser=session,idproduct=producto.id,amount=amount,date=datetime.date.today())
                carrito.save()
                diffamount = int(producto.amount)-int(amount)
                producto.amount = diffamount
                producto.save()
                messages.add_message(request,messages.SUCCESS,'Elemento agregado al carrito')
        else:
            messages.add_message(request,messages.ERROR,'Seleccione la cantidad para continuar')
        return redirect('/index/')
    else:
        messages.add_message(request,messages.ERROR,'Inicie Sesión para poder adquirir producto')
        return redirect('/index/')


def finalizarPedido(request):
    session = request.session.get('user')
    if session:
        if request.method == 'POST':
            price = request.POST['totalprice']
            compra = Compras(iduser=session,totalprice=price,date=datetime.date.today(),hour=time.strftime('%H:%M:%S'))
            compra.save()
            carrito = Carrito.objects.filter(iduser=session).filter(date=datetime.date.today())
            for elemento in carrito:
                elemento.status = True
                elemento.save()
            messages.add_message(request,messages.SUCCESS,'Compra finalizada, Puede realizar otro compra despues de 24 horas')
            return redirect('/index/')
    else:
        messages.add_message(request,messages.ERROR,'Inicie Sesión para continuar')
        return redirect('/login/')


def renderHistory(request):
    session = request.session.get('user')
    if session:
        usuario = Usuarios.objects.get(id=session)
        compras = Compras.objects.filter(iduser=session)
        return render(request,'user/historial.html',{'session':session,'usuario':usuario,'compras':compras})
    else:
        messages.add_message(request,messages.ERROR,'Inicie Sesión para continuar')
        return render('/login/')

def renderCompraHecha(request,date):
    session = request.session.get('user')
    if session:
        elementos=[]
        usuario = Usuarios.objects.get(id=session)
        carrito = Carrito.objects.filter(date=date).filter(iduser=session).filter(status=True).values()
        compra = Compras.objects.filter(date=date).filter(iduser=session).get()
        for i in range(len(carrito)):
            productos = Productos.objects.filter(id=carrito[i]['idproduct'])
            for producto in productos:
                elementos.append({  'name':producto.name,
                                    'price':producto.price,
                                    'urlimage':producto.image_url,
                                    'cantidad':carrito[i]['amount']})
        return render(request,'user/compra-hecha.html',{'session':session,'usuario':usuario,'elementos':elementos,'totalprice':compra.totalprice})
    else:
        messages.add_message(request,messages.ERROR,'Inicie Sesión para continuar')
        return redirect('/login/')
#LOGOUT SESSION
def logout(request):
    session = request.session.get('user')
    if session:
        del request.session['user']
        messages.add_message(request,messages.SUCCESS,'Cerro Sesión Correctamente')
        return redirect('/login/')
    else:
        messages.add_message(request,messages.ERROR,'Aún no ha iniciado sesión')
        return redirect('/login/')