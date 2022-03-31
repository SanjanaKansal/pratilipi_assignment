from daily_pass import models
from daily_pass import variables
from daily_pass import exceptions
from daily_pass import connector


def unlock_chapter(user_id, title):
    chapters = connector.get_chapter_details_from_content_service(title)['chapters']
    chapter_ids = [chapter['id'] for chapter in chapters]
    chapter_id_title_map = {}
    for chapter in chapters:
        chapter_id_title_map[chapter['id']] = chapter['title']
    series_id = chapters[0]['series_id']
    last_pass = models.DailyPass.objects.filter(user_id=user_id, series_id=series_id).order_by('created_at').last()
    if not last_pass:
        if len(chapter_ids) <= variables.UNLOCKED_CHAPTERS_BY_DEFAULT:
            raise exceptions.NoLockedChapterException
        chapter_id = chapter_ids[variables.UNLOCKED_CHAPTERS_BY_DEFAULT]
        models.DailyPass.objects.create(user_id=user_id, series_id=series_id, chapter_id=chapter_id)
    else:
        for id, val in enumerate(chapter_ids):
             if val == last_pass.chapter_id:
                 if len(chapter_ids) <= id + 1:
                     raise exceptions.NoLockedChapterException
                 chapter_id = chapter_ids[id+1]
        models.DailyPass.objects.create(user_id=user_id, series_id=series_id, chapter_id=chapter_id)
    return chapter_id_title_map[chapter_id]


def get_unlocked_chapters_for_user(user_id):
    return list(models.DailyPass.objects.filter(user_id=user_id).values('chapter_id', 'created_at', 'series_id'))



