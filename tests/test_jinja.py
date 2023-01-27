from connect_ext import jinja


def test_render():
    rendered = jinja.render('hello {{request.name}}', {'name': 'world'})
    assert rendered == 'hello world'
