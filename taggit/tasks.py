from celery.decorators import task


@task(ignore_result=True)
def remove_unused_tags():
	from django.db import connection, transaction
	cursor = connection.cursor()
	cursor.execute("DELETE FROM taggit_tag WHERE id NOT IN (SELECT tag_id FROM taggit_taggeditem)")
	transaction.commit_unless_managed()
