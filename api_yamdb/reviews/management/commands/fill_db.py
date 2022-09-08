import csv

from django.core.management.base import BaseCommand

from reviews.models import (Category, Comments, Genre, GenreTitle, Review,
                            Title, User)


class Command(BaseCommand):
    help = 'Fill DB'

    def handle(self, *args, **options):
        models_data = [
            'users', 'category', 'genre', 'titles', 'review', 'comments',
            'genre_title'
        ]

        for model_data in models_data:
            with open(f'static/data/{model_data}.csv') as f:
                reader = csv.reader(f)
                next(reader)

                if model_data == 'users':
                    User.objects.bulk_create(
                        User(
                            id=row[0],
                            username=row[1],
                            email=row[2],
                            role=row[3],
                            bio=row[4],
                            first_name=row[5],
                            last_name=row[6]
                        ) for row in reader
                    )

                if model_data == 'category':
                    Category.objects.bulk_create(
                        Category(
                            id=row[0],
                            name=row[1],
                            slug=row[2],
                        ) for row in reader
                    )

                if model_data == 'genre':
                    Genre.objects.bulk_create(
                        Genre(
                            id=row[0],
                            name=row[1],
                            slug=row[2],
                        ) for row in reader
                    )

                if model_data == 'titles':
                    Title.objects.bulk_create(
                        Title(
                            id=row[0],
                            name=row[1],
                            year=row[2],
                            category=Category.objects.get(id=row[3]),
                        ) for row in reader
                    )

                if model_data == 'review':
                    Review.objects.bulk_create(
                        Review(
                            id=row[0],
                            title=Title.objects.get(id=row[1]),
                            text=row[2],
                            author=User.objects.get(id=row[3]),
                            score=row[4],
                            pub_date=row[5],
                        ) for row in reader
                    )

                if model_data == 'comments':
                    Comments.objects.bulk_create(
                        Comments(
                            id=row[0],
                            review=Review.objects.get(id=row[1]),
                            text=row[2],
                            author=User.objects.get(id=row[3]),
                            pub_date=row[4],
                        ) for row in reader
                    )

                if model_data == 'genre_title':
                    GenreTitle.objects.bulk_create(
                        GenreTitle(
                            id=row[0],
                            title=Title.objects.get(id=row[1]),
                            genre=Genre.objects.get(id=row[2]),
                        ) for row in reader
                    )

        self.stdout.write(self.style.SUCCESS(
            'Data successfully imported into the database'
        ))
