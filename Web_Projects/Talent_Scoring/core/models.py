from django.db import models


# Create your models here.

FORMULA_CHOICES = (
        ("1", "1"),
        ("multiply_weight", "multiply_weight"),
        ("average_weight_multiply", "average_weight_multiply"),
    )


class StageModel(models.Model):
    stage_name = models.CharField(verbose_name='stage', max_length=255)
    stage_question_id = models.ManyToManyField(
        "core.Questions", related_name='stage_question', null=True, blank=True)
    order_by = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.stage_name}'


class Questions(models.Model):

    question_title = models.CharField(verbose_name='question', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_by = models.PositiveIntegerField(default=1)
    formula = models.CharField(choices = FORMULA_CHOICES, max_length = 30, null=True, blank=True)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.question_title


class Answers(models.Model):
    question_id = models.ForeignKey(
        "core.Questions", on_delete=models.CASCADE, related_name='question')
    answer_title = models.CharField(max_length=100, null=True, blank=True)
    answer_weight = models.DecimalField(max_digits=9,
                                        decimal_places=4,
                                        null=True,
                                        blank=True)
    related_question = models.ManyToManyField(
        "core.Questions", related_name='related_question', blank=True)
    is_related = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return self.question_id.question_title



class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title



class Contact(models.Model):
    fullname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=100)
    email_data = models.EmailField()
    text = models.TextField()

    def __str__(self):
        return f'{self.fullname}'
