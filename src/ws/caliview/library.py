from pyramid.view import view_config
from sqlalchemy import create_engine, text as sql

# Adapted from `CREATE VIEW meta` provided by Calibre,
# retrieve schema via `SELECT sql FROM sqlite_master`
query = """\
select title, series.name as series, series_index as number, ratings.rating/2 as rating,
(select group_concat(name, ", ") from authors where authors.id in (select author from books_authors_link where book=books.id)) as author,
(select group_concat(name, ", ") from tags where tags.id in (select tag from books_tags_link where book=books.id)) as tags
from books
left outer join books_series_link sl on sl.book=books.id left outer join series on series.id=sl.series
left outer join books_ratings_link rl on rl.book=books.id left outer join ratings on ratings.id=rl.rating
left outer join books_tags_link tl on tl.book=books.id left outer join tags on tags.id=tl.tag
"""

order = " order by series.name, series_index"


@view_config(
    route_name='home',
    renderer='templates/list.html')
def list(request):
    where = request.GET.get('q', '')
    if where:
        where = ' where ' + where
    engine = create_engine(request.registry.settings['sqlalchemy.url']
                           + '?immutable=1')
    with engine.connect() as con:
        return {'rows': con.execute(sql(query + where + order)).fetchall()}
