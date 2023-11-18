from Recipes.settings import ALLOWED_HOSTS
from django.template.loader import render_to_string


def send_new_comment_notification(comment):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    author = comment.recipe.author
    context = {'author': author, 'host': host, 'comment': comment}
    subject = render_to_string('email/new_comment_letter_subject.txt', context)
    body_text = render_to_string('email/new_comment_letter_body.txt', context)
    author.email_user(subject, body_text)


def upload_path_recipe(instance, filename):
    return f'recipes_images/{instance.title}/{filename}'


def upload_path_step_cooking(instance, filename):
    return f'recipes_images/{instance.recipe.title}/{instance.step}/step_{filename}'
