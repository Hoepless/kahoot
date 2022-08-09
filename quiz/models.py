from django.db import models
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save

from account.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    questions_count = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='quiz_cover')
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=255)
    question_time = models.IntegerField(default=20)

    def __str__(self):
        return self.title

    def get_correct_answer(self):
        return self.answer_set.get(is_correct=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    points = models.IntegerField(default=100)

    def __str__(self):
        return self.text


class QuizTaker(models.Model):
    group = models.ForeignKey(Group, default=None, on_delete=models.CASCADE, null=True, related_name='quiztakergroup')
    tests_passed = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiztakers')
    questions = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='quiztaker', blank=True, null=True)
    answers = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='quiztaker', blank=True, null=True)
    correct_answers = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class QuizTakerResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quiz_taker = models.ForeignKey(QuizTaker, default=None, on_delete=models.CASCADE, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, related_name='taker_response')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    score = models.IntegerField(null=True, blank=True)
    is_submit = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} : {self.score}"

    @staticmethod
    def calculate_final_score(user: User, question_id, quiz_id, answer, is_submit, factual_time):
        question = Question.objects.get(pk=question_id)
        quiz = Quiz.objects.get(pk=quiz_id)
        score = 0
        taker_answer = question.answer_set.get(text=answer)
        if is_submit:
            QuizTakerResponse.quiz_count(user)
        if question.get_correct_answer().text == taker_answer.text:
            if factual_time == 1:
                score = 100 - (100 / question.question_time * factual_time) + (100 / question.question_time)
            else:
                score = 100 - (100 / question.question_time * factual_time)
        user.set_final_score(score)
        user.set_group_rating_place()
        user.set_rating_place()

        return [QuizTakerResponse.objects.create(score=score, user=user, quiz=quiz, answer=taker_answer, group=user.group),
               QuizTaker.objects.create(user=user, quiz=quiz, questions=question, answers=taker_answer, group=user.group)]

    @staticmethod
    def quiz_count(user: User):
        user.set_tests_passed(1)


@receiver(post_save, sender=Quiz)
def set_default_quiz(sender, instance, created, **kwargs):
    quiz = Quiz.objects.filter(id=instance.id)
    quiz.update(questions_count=instance.questions.filter(quiz=instance.pk).count())


@receiver(post_save, sender=Question)
def set_default(sender, instance, created, **kwargs):
    quiz = Quiz.objects.filter(id=instance.quiz.id)
    quiz.update(questions_count=instance.quiz.questions.filter(quiz=instance.pk).count())