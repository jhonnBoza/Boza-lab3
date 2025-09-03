from django.db import models
#agregado de accounts
from django.contrib.auth.models import User

class Exam(models.Model):
    """Modelo para exámenes"""
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descripción")
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_question_count(self):
        """Retorna el número de preguntas en el examen"""
        return self.questions.count()

class Question(models.Model):
    """Modelo para preguntas"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name="Texto de la pregunta")

    def __str__(self):
        return self.text[:50]  # Retorna los primeros 50 caracteres
    
class Choice(models.Model):
    """Modelo para opciones de respuesta"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200, verbose_name="Texto")
    is_correct = models.BooleanField(default=False, verbose_name="Es correcta")
    
    def __str__(self):
        return self.text
    

# Agregado para rastrear intentos de exámenes y respuestas de usuarios
class ExamAttempt(models.Model):
    """Modelo para rastrear intentos de exámenes por usuarios"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_attempts')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    time_taken = models.DurationField(null=True, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.exam.title} ({self.percentage}%)"

class UserAnswer(models.Model):
    """Modelo para respuestas de usuarios en un intento de examen"""
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.attempt.user.username} - Q{self.question.id}"




    
