import pytest
from _pytest.mark import MarkDecorator

def pytest_namespace():
    # Add in unmark
    return {'unmark': unmarker()}

class unmarker(object):
    def __getattr__(self, item):
        # Return an marker remover
        if item[0] == "_":
            raise AttributeError("Marker name must NOT start with underscore")
        return MarkDecorator("unmark:%s" % item)


class Fauxcals:
    """
    SHould work with the eval() as the set of 'locals'. Will return
    true for any item keyword that begins with unmark. This should only work for
    marks set by 'unmarker', because you can't do `@pytest.mark.namewith:colon`.
    """
    def __init__(self, keywords):
        self.keys = [key.split(":")[1] for key in keywords if "unmark:" in key]

    def __getitem__(self, item):
        return item in self.keys


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    matchexpr = config.option.markexpr
    if not matchexpr:
        return

    remaining = []
    deselected = []
    for colitem in items:
        if matchexpr:
            if eval(matchexpr, {}, Fauxcals(colitem.keywords)):
                print "Deselecting %r (mark removed by @pytest.unmark)" % colitem
                deselected.append(colitem)
                continue
        remaining.append(colitem)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = remaining
