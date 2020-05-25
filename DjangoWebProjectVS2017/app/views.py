"""
Definition of views.
"""

from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http.response import HttpResponse, Http404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Pregunta,Respuesta,User
from django.template import loader
from django.core.urlresolvers import reverse
from app.forms import QuestionForm, ChoiceForm,UserForm,ChoiceForm1,IndexForm
from django.shortcuts import redirect
import json


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Autor de la web',
            'message':'Datos de contacto',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


def detail(request, question_id):
     question = get_object_or_404(Pregunta, pk=question_id)
     return render(request, 'polls/detail.html', {'title':'Respuestas asociadas a la pregunta:','question': question})


def results(request, question_id,correct):
    question = get_object_or_404(Pregunta, pk=question_id)
    aux = Respuesta.objects.get(id=correct)
    if aux.correct == 0:
        return render(request, 'polls/results.html', {'title':'Respuesta incorrecta intentalo otra vez','question': question}) 
    else:
        return  render(request, 'polls/results.html', {'title':'Respuesta Correcta','question': question}) 

def vote(request, question_id):
    p = get_object_or_404(Pregunta, pk=question_id)
    b =  request.POST.get("choice")
    try:
       selected_choice= Respuesta.objects.get(id=b)
    except (KeyError, Respuesta.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "ERROR: No se ha seleccionado una opcion",
        })
    else:
        selected_choice.votes += 1

        selected_choice.save()
        

        # Siempre devolver un HttpResponseRedirect despues de procesar
        # exitosamente el POST de un form. Esto evita que los datos se
        # puedan postear dos veces si el usuario vuelve atras en su browser.
        return HttpResponseRedirect(reverse('results', args=(p.id,int(b))))

def question_new(request):
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.pub_date=datetime.now()
                question.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = QuestionForm()
        return render(request, 'polls/question_new.html', {'form': form})

def choice_add(request, question_id):
        pregunta = Pregunta.objects.get(id = question_id)
        try:
            choice = Respuesta.objects.get(question = pregunta, correct = 1)
        except Respuesta.DoesNotExist:
            if request.method =='POST':
                form = ChoiceForm(request.POST)
                if form.is_valid():
                    choice = form.save(commit = False)
                    choice.question = pregunta
                    choice.vote = 0
                    choice.save()         
                    #form.save()
            else: 
                form = ChoiceForm()
            return render(request, 'polls/choice_new.html', {'title':'Pregunta:'+ pregunta.question_text,'form': form, 'question': pregunta})
        if request.method =='POST':
            form = ChoiceForm1(request.POST)
            if form.is_valid():
                choice = form.save(commit = False)
                choice.question = pregunta
                choice.correct = False
                choice.vote = 0
                choice.save()         
                #form.save()
        else: 
            form = ChoiceForm1()
        #return render_to_response ('choice_new.html', {'form': form, 'poll_id': poll_id,}, context_instance = RequestContext(request),)
        return render(request, 'polls/choice_new.html', {'title':'Pregunta:'+ pregunta.question_text,'form': form, 'question': pregunta})

def chart(request, question_id):
    q=Pregunta.objects.get(id = question_id)
    qs = Respuesta.objects.filter(question=q)
    dates = [obj.choice_text for obj in qs]
    counts = [obj.votes for obj in qs]
    context = {
        'dates': json.dumps(dates),
        'counts': json.dumps(counts),
    }

    return render(request, 'polls/grafico.html', context)

def user_new(request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = UserForm()
        return render(request, 'polls/user_new.html', {'form': form})

def users_detail(request):
    latest_user_list = User.objects.order_by('email')
    template = loader.get_template('polls/users.html')
    context = {
                'title':'Lista de usuarios',
                'latest_user_list': latest_user_list,
              }
    return render(request, 'polls/users.html', context)

def index(request):        
         
         if request.method =='POST':
            form= IndexForm(request.POST)
                      
            if form.is_valid():
                aux = request.POST.get("Tema")
                latest_question_list = Pregunta.objects.filter(question_tema=aux)
                template = loader.get_template('polls/index.html')
                context = {
                'form': form, 
                'title':'Lista de preguntas de la encuesta',
                'latest_question_list': latest_question_list,
              }
                
                
            return render(request, 'polls/index.html', context)  
                #form.save()
         else: 
            latest_question_list = Pregunta.objects.order_by('-pub_date')
            template = loader.get_template('polls/index.html')
            form= IndexForm(request.GET)
         context = {
                'form': form, 
                'title':'Lista de preguntas de la encuesta',
                'latest_question_list': latest_question_list,
              }
         return render(request, 'polls/index.html', context)

