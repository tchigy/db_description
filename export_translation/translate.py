# -*- coding: utf-8 -*-
from lxml import etree
import re
from odoo import tools

# A big Thank to Martijn Pieters one of great python developer in stack overflow that save me a lot of searching
# to do something like this witch is to replace an inner method.
# check this link: https://stackoverflow.com/questions/27550228/can-you-patch-just-a-nested-function-with-closure-or-must-the-whole-outer-fun/27550237


def replace_inner_function(outer, new_inner):
    """Replace a nested function code object used by outer with new_inner

    The replacement new_inner must use the same name and must at most use the
    same closures as the original.

    """
    if hasattr(new_inner, '__code__'):
        # support both functions and code objects
        new_inner = new_inner.__code__

    # find original code object so we can validate the closures match
    ocode = outer.__code__
    function, code = type(outer), type(ocode)
    iname = new_inner.co_name
    orig_inner = next(
        const for const in ocode.co_consts
        if isinstance(const, code) and const.co_name == iname)
    # you can ignore later closures, but since they are matched by position
    # the new sequence must match the start of the old.
    assert (orig_inner.co_freevars[:len(new_inner.co_freevars)] ==
            new_inner.co_freevars), 'New closures must match originals'
    # replace the code object for the inner function
    new_consts = tuple(
        new_inner if const is orig_inner else const
        for const in outer.__code__.co_consts)

    # create a new function object with the new constants
    return function(
        code(ocode.co_argcount, ocode.co_nlocals, ocode.co_stacksize,
             ocode.co_flags, ocode.co_code, new_consts, ocode.co_names,
             ocode.co_varnames, ocode.co_filename, ocode.co_name,
             ocode.co_firstlineno, ocode.co_lnotab, ocode.co_freevars,
             ocode.co_cellvars),
        outer.__globals__, outer.__name__, outer.__defaults__,
        outer.__closure__)



def new_push_translation():
    """ """
    to_translate = None

    def push_translation(module, type, name, id, source, comments=None):
        # empty and one-letter terms are ignored, they probably are not meant to be
        # translated, and would be very hard to translate anyway.
        sanitized_term = (source or '').strip()
        try:
            # verify the minimal size without eventual xml tags
            # wrap to make sure html content like '<a>b</a><c>d</c>' is accepted by lxml
            wrapped = "<div>%s</div>" % sanitized_term
            node = etree.fromstring(wrapped)
            sanitized_term = etree.tostring(node, encoding='UTF-8', method='text')
        except etree.ParseError:
            pass
        from  odoo.http import request
        if request.env.get('translate.dummy', 0) != 0:
             # remove non-alphanumeric unicode
             sanitized_term = re.sub(r'\W+', '', sanitized_term, flags=re.UNICODE)
        else:
            # remove non-alphanumeric No unicode flag
            sanitized_term = re.sub(r'\W+', '', sanitized_term)
        if not sanitized_term or len(sanitized_term) <= 1:
            return

        tnx = (module, source, name, id, type, tuple(comments or ()))
        to_translate.add(tnx)

    return push_translation

# first create the replacement function.
push_translation = new_push_translation()
# get original method
origin_method = tools.trans_generate
# replace push_translation
trans_generate = replace_inner_function(origin_method, push_translation)
# now correct the reference in trans_export because it references to original method.
tools.trans_export.func_globals['trans_generate'] = trans_generate


from odoo import models

class DummyModel(models.AbstractModel):
    """  just a dummy model to check if the module is installed instead of using search method to check
        for every terms that we want to export !!!! """
    _name = 'translate.dummy'