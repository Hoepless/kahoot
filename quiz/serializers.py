from rest_framework import serializers

from .models import QuizTaker, Quiz, Question, QuizTakerResponse


class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = ('title', 'questions_count',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['completed_users'] = QuizTaker.objects.all().filter(quiz=instance, completed=True).count()

        return representation


class QuizTakerResponseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    question_id = serializers.IntegerField()
    quiz_id = serializers.IntegerField()
    answer = serializers.CharField(max_length=255)
    factual_time = serializers.IntegerField()
    is_submit = serializers.BooleanField(default=False)

    class Meta:
        model = QuizTakerResponse
        fields = ('question_id', 'answer_id', 'score'   , 'answer', 'quiz_id',
                  'factual_time', 'user', 'is_submit')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation['question'] = instance.question.title
        return representation


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class QuizTakerDetailSerializer(serializers.ModelSerializer):

    questions = serializers.ReadOnlyField(source='questions.title')

    class Meta:
        model = QuizTaker
        fields = ('quiz', 'questions', 'answers', 'correct_answers')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['quiz'] = QuizTakerResponse.objects.filter(quiz_taker__user=instance.user).values('quiz_taker__quiz__title').distinct()
        representation['questions'] = QuizTakerResponse.objects.filter(quiz_taker=instance).values_list('question__title')
        representation['answers'] = QuizTakerResponse.objects.filter(quiz_taker=instance).values('question__text', 'answer__text')
        return representation


class QuizTakerSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuizTaker
        fields = ('group', 'tests_passed')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(instance)
        representation['first_name'] = instance.user.first_name
        representation['last_name'] = instance.user.last_name
        representation['phone'] = instance.user.phone
        representation['email'] = instance.user.email
        representation['rating_place'] = instance.user.rating_place
        representation['final_score'] = instance.user.final_score

        return representation
