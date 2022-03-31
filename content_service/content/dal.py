from content import models
from django.core.exceptions import ObjectDoesNotExist
from content import exceptions
from content import connector


def save_content(series_title, chapters):
    series, _ = models.Series.objects.get_or_create(title=series_title)
    for chapter in chapters:
        models.Chapter.objects.update_or_create(
            title=chapter.get('title'),
            series=series
        )


def get_content():
    chapters = list(models.Chapter.objects.values('series__title', 'title'))
    series_chapter_mapping = {}
    for chapter in chapters:
        if chapter['series__title'] not in series_chapter_mapping:
            series_chapter_mapping[chapter['series__title']] = [chapter['title']]
        else:
            series_chapter_mapping[chapter['series__title']].append(chapter['title'])

    content = []
    for series, chapters in series_chapter_mapping.items():
        content.append({'title': series, 'chapters': [{'title': chapter_title} for chapter_title in chapters]})
    return content


def get_series(title):
    try:
        return models.Series.objects.get(title=title)
    except ObjectDoesNotExist:
        raise exceptions.SeriesDoesNotExistException


def get_chapter_details(series):
    return list(
        models.Chapter.objects.filter(
            series__title=series
        ).order_by('created_at').order_by('id').values('id', 'title', 'series_id')
    )


def get_content_for_user(user_id):
    chapters = list(models.Chapter.objects.order_by('created_at').order_by('id').values('series__title', 'title', 'series_id', 'id', 'created_at'))
    user_content = {}
    for chapter in chapters:
        if chapter['series_id'] not in user_content:
            user_content[chapter['series_id']] = {
                'title': chapter['series__title'],
                'chapters': {chapter['id']: {'title': chapter['title'], 'locked': False, 'release_date': chapter['created_at']}}
            }
        else:
            series_chapters = user_content[chapter['series_id']]['chapters']
            if len(series_chapters) >= 4:
                series_chapters[chapter['id']] = {'title': chapter['title'], 'locked': True}
            else:
                series_chapters[chapter['id']] = {'title': chapter['title'], 'locked': False, 'release_date': chapter['created_at']}


    unlocked_chapters = connector.get_unlocked_chapters_for_user(user_id)['chapters']
    for pas in unlocked_chapters:
        series_id = pas['series_id']
        chapter_id = pas['chapter_id']
        user_content[series_id]['chapters'][chapter_id]['locked'] = False
        user_content[series_id]['chapters'][chapter_id]['release_date'] = pas['created_at']

    user_content_to_display = []

    for id, val in user_content.items():
        locked_chapters = 0
        unlocked_chapters = 0
        chapters_list = []
        for chapter_id, chapter in val['chapters'].items():
            if chapter['locked'] == True:
                locked_chapters +=1
            else:
                unlocked_chapters += 1
            chapters_list.append(chapter)
        val['total_chapters'] = locked_chapters + unlocked_chapters
        val['unlocked_chapters'] = unlocked_chapters
        val['chapters'] = chapters_list
        user_content_to_display.append(val)

    return user_content_to_display









