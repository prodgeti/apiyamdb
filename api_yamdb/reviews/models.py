from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import validate_actual_year

MIN_VALUE = 1
MAX_VALUE = 10

User = get_user_model()


class ReviewCommentBase(models.Model):
    """Базовая модель для отзывов и комменатриев."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s',
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Review(ReviewCommentBase):
    """Описание модели 'Отзыв'."""
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_VALUE),
            MaxValueValidator(MAX_VALUE)
        ],
        verbose_name='Оценка'
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )
        ]


class Comment(ReviewCommentBase):
    """Описание модели 'Комментарий'."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class CategoryGenreBase(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='ID',
        unique=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(CategoryGenreBase):
    """Категории 'произведений'."""

    class Meta(CategoryGenreBase.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreBase):
    """Жанры 'произведений'."""

    class Meta(CategoryGenreBase.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Произведение культуры. Конкретный объект.

    Поля 'name', 'year', 'category', 'description'.
    name - Авторское или исторически сложившееся название. Обязательное.
    year - Год издания/публикации произведения. Обязательное.
    category - ссылка на категорию. Обязательное. При удалении категории,
    принимает дефоптное значение.
    Значение по умолчанию - 'Null'.
    description - Краткое представление произведения.
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=256

    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=[validate_actual_year],
        db_index=True
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'

    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name
