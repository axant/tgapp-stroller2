from tg import expose

@expose('stroller2.templates.little_partial')
def something(name):
    return dict(name=name)