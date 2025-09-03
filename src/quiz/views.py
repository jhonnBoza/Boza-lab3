from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Exam, Question, Choice
from .forms import ExamForm, QuestionForm, ChoiceFormSet
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from accounts.models import UserProfile
from .models import ExamAttempt, UserAnswer
import json

@login_required
def take_exam(request, exam_id):
    """View to take an exam"""
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all().prefetch_related('choices')
    
    if not questions:
        messages.error(request, 'This exam has no questions yet.')
        return redirect('exam_detail', exam_id=exam.id)
    
    if request.method == 'POST':
        # Process exam submission
        start_time_str = request.POST.get('start_time')
        start_time = timezone.datetime.fromisoformat(start_time_str)
        time_taken = timezone.now() - start_time
        
        # Create exam attempt
        attempt = ExamAttempt.objects.create(
            user=request.user,
            exam=exam,
            total_questions=questions.count(),
            time_taken=time_taken
        )
        
        score = 0
        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                selected_choice = get_object_or_404(Choice, id=selected_choice_id)
                is_correct = selected_choice.is_correct
                if is_correct:
                    score += 1
                
                # Save user answer
                UserAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_choice=selected_choice,
                    is_correct=is_correct
                )
        
        # Update attempt with final score
        attempt.score = score
        attempt.percentage = (score / questions.count()) * 100
        attempt.save()
        
        # Update user profile stats
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.total_score += score
        profile.exams_taken += 1
        profile.save()
        
        return redirect('exam_result', attempt_id=attempt.id)
    
    context = {
        'exam': exam,
        'questions': questions,
        'start_time': timezone.now().isoformat(),
    }
    return render(request, 'quiz/take_exam.html', context)


@login_required
def exam_result(request, attempt_id):
    """View to show exam results"""
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, user=request.user)
    answers = attempt.answers.all().select_related('question', 'selected_choice')
    
    # Calculate time taken in minutes and seconds
    time_minutes = 0
    time_seconds = 0
    if attempt.time_taken:
        total_seconds = attempt.time_taken.total_seconds()
        time_minutes = int(total_seconds // 60)
        time_seconds = int(total_seconds % 60)
    
    context = {
        'attempt': attempt,
        'answers': answers,
        'time_minutes': time_minutes,
        'time_seconds': time_seconds,
    }
    return render(request, 'quiz/exam_result.html', context)


def exam_list(request):
    """View to display a list of all exams"""
    exams = Exam.objects.all().order_by('-created_date')
    return render(request, 'quiz/exam_list.html', {'exams': exams})

def exam_detail(request, exam_id):
    """View to display the details of an exam with its questions"""
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all().prefetch_related('choices')
    return render(request, 'quiz/exam_detail.html', {'exam': exam, 'questions': questions})

def exam_create(request):
    """View to create a new exam"""
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save()
            messages.success(request, 'Examen creado correctamente.')
            return redirect('question_create', exam_id=exam.id)
    else:
        form = ExamForm()
    
    return render(request, 'quiz/exam_form.html', {'form': form})

def question_create(request, exam_id):
    """View to add questions to an exam"""
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        
        if question_form.is_valid():
            with transaction.atomic():
                # Save the question
                question = question_form.save(commit=False)
                question.exam = exam
                question.save()
                
                # Process the formset for choices
                formset = ChoiceFormSet(request.POST, instance=question)
                if formset.is_valid():
                    formset.save()
                    
                    # Verify that only one option is marked as correct
                    correct_count = question.choices.filter(is_correct=True).count()
                    if correct_count != 1:
                        messages.warning(request, 'Debe haber exactamente una respuesta correcta.')
                    else:
                        messages.success(request, 'Pregunta añadida correctamente.')
                        
                    # Decide where to redirect
                    if 'add_another' in request.POST:
                        return redirect('question_create', exam_id=exam.id)
                    else:
                        return redirect('exam_detail', exam_id=exam.id)
    else:
        question_form = QuestionForm()
        formset = ChoiceFormSet()
    
    return render(request, 'quiz/question_form.html', {
        'exam': exam,
        'question_form': question_form,
        'formset': formset,
    })



