import os
import json
import pytz
from urllib.parse import urlparse
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional, Union

from django import template
from django.conf import settings
from django.utils import timezone
from django.core import exceptions
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError

from django.template.loader import get_template


from django.utils.safestring import SafeText
from django.template.loader import render_to_string
from django.utils.safestring import SafeString
from django.template.base import (NodeList, Parser, Token,
                                    token_kwargs, TextNode, Variable)

from django.template import (Library, Node, RequestContext, loader,
                            TemplateSyntaxError, Template, Context)


from django.template.loader_tags import (construct_relative_path, BlockNode,
                                            IncludeNode, 
                                            BLOCK_CONTEXT_KEY, BlockContext
                                            )


from phonenumber_field.phonenumber import PhoneNumber


register = template.Library()

accessible_settings = [
                        'STATIC_URL',
                        'ANALYTICS_TAG_ID',
                        'PROJECT_TITLE',
                    ]

accessible_settings = [x.lower() for x in accessible_settings]

# settings value
@register.simple_tag
def settings_value(name):
    if name.lower() in accessible_settings:
        return getattr(settings, name, "")

    raise ValidationError("This settings is not accessible from the template, add it to allowed settings")


@register.filter
def phone_number(value):
    """
        extract number only from country code
    """
    try:
        phone = PhoneNumber.from_string(value)
        return phone.national_number

    except Exception:
        return ""

@register.filter
def filename(value):
    """
        returns just the file name
    """
    return os.path.basename(value.name)


@register.filter
def subtract(value, arg):
    return value - arg


@register.simple_tag
def utc_to_local(utc_datetime, user_timezone, date_format="%b. %d, %Y, %I:%M %p"):
    
    if utc_datetime and user_timezone:
        if not isinstance(utc_datetime, str):
            utc_datetime = str(utc_datetime)

        try:
            user_timezone = pytz.timezone(user_timezone)  

        except pytz.UnknownTimeZoneError:
            pass

        utc_datetime_obj = datetime.fromisoformat(utc_datetime)
        utc_datetime_obj = utc_datetime_obj.replace(tzinfo=pytz.UTC)
        
        specific_datetime = utc_datetime_obj.astimezone(user_timezone)
        # print("date: ", specific_datetime, specific_datetime.strftime(date_format), date_format)
        return specific_datetime.strftime(date_format)
    
    else:
        return utc_datetime.strftime(date_format)

@register.filter
def get_key(items: dict, index=0):
    return list(items.keys())[index]

@register.filter
def get_value(items: dict, index=0):
    return list(items.values())[index]


@register.filter
def extract_path(url):
    """
        extracts path from url
    """
    path = urlparse(url).path
    return path[1:]



@register.filter
def strip_html_tags(data: str):
    """
        removes html tags
    """
    return strip_tags(data)


class RenderComponentNode(template.Node):
    def __init__(
        self,
        template_name: str,
        nodelist: NodeList,
        extra_context: Optional[Dict] = None,
        *args,
        **kwargs,
    ):
        self.template_name = template_name
        self.nodelist = nodelist
        self.extra_context = extra_context or {}
        super().__init__(*args, **kwargs)

    def render(self, context: RequestContext) -> str:
        result = self.nodelist.render(context)

        ctx = {name: var.resolve(context) for name, var in self.extra_context.items()}
        ctx.update({"children": result})

        return render_to_string(
            self.template_name,
            request=context.request,
            context=ctx,
        )


@register.tag("component")
def do_component(parser: Parser, token: Token) -> str:
    bits = token.split_contents()

    if len(bits) < 2:
        raise TemplateSyntaxError(
            f"{bits[0]} tag takes at least one argument: the name of the template to be included."
        )

    options = {}
    remaining_bits = bits[2:]

    while remaining_bits:
        option = remaining_bits.pop(0)

        if option in options:
            raise TemplateSyntaxError(
                f"The {option} option was specified more than once."
            )

        if option == "with":
            value = token_kwargs(remaining_bits, parser, support_legacy=False)

            if not value:
                raise TemplateSyntaxError(
                    '"with" in {bits[0]} tag needs at least one keyword argument.'
                )
        else:
            raise TemplateSyntaxError(f"Unknown argument for {bits[0]} tag: {option}.")

        options[option] = value

    nodelist = parser.parse(("endcomponent",))
    template_name = bits[1][1:-1]
    extra_context = options.get("with", {})
    parser.next_token()

    return RenderComponentNode(template_name, nodelist, extra_context)



# class IncludeExtendNode(Node):
#     context_key = "__include_context"

#     def __init__(
#         self, template, parent_name, *args, extra_context=None, isolated_context=False, **kwargs
#     ):
#         self.template = template
#         self.parent_name = parent_name
#         self.extra_context = extra_context or {}

#         print("template: ", template)

#         self.blocks = {}

#         self.isolated_context = isolated_context
#         super().__init__(*args, **kwargs)

#     def __repr__(self):
#         return f"<{self.__class__.__qualname__}: template={self.template!r}>"

#     def find_template(self, template_name, context):
#         """
#         This is a wrapper around engine.find_template(). A history is kept in
#         the render_context attribute between successive extends calls and
#         passed as the skip argument. This enables extends to work recursively
#         without extending the same template twice.
#         """
#         history = context.render_context.setdefault(
#             self.context_key,
#             [self.origin],
#         )
#         template, origin = context.template.engine.find_template(
#             template_name,
#             skip=history,
#         )
#         history.append(origin)
#         return template

#     def get_parent(self, context):
#         parent = self.parent_name.resolve(context)

#         print("context: ", context)

#         if not parent:
#             error_msg = "Invalid template name in 'extends' tag: %r." % parent
#             if self.parent_name.filters or isinstance(self.parent_name.var, Variable):
#                 error_msg += (
#                     " Got this from the '%s' variable." % self.parent_name.token
#                 )
#             raise TemplateSyntaxError(error_msg)
#         if isinstance(parent, Template):
#             # parent is a django.template.Template
#             return parent
#         if isinstance(getattr(parent, "template", None), Template):
#             # parent is a django.template.backends.django.Template
#             return parent.template
#         return self.find_template(parent, context)

#     def render(self, context):
#         """
#         Render the specified template and context. Cache the template object
#         in render_context to avoid reparsing and loading when used in a for
#         loop.
#         """
      
#         print("context: ", self.extra_context)

#         template = self.template.resolve(context)
#         # Does this quack like a Template?
#         if not callable(getattr(template, "render", None)):
#             # If not, try the cache and select_template().
#             template_name = template or ()
#             if isinstance(template_name, str):
#                 template_name = (
#                     construct_relative_path(
#                         self.origin.template_name,
#                         template_name,
#                     ),
#                 )
#             else:
#                 template_name = tuple(template_name)
#             cache = context.render_context.dicts[0].setdefault(self, {})
#             template = cache.get(template_name)
#             if template is None:
#                 template = context.template.engine.select_template(template_name)
#                 cache[template_name] = template
#         # Use the base.Template of a backends.django.Template.
#         elif hasattr(template, "template"):
#             template = template.template
#         values = {
#             name: var.resolve(context) for name, var in self.extra_context.items()
#         }
#         # print("context: ", context)

#         self.blocks = {n.name: n for n in template.nodelist.get_nodes_by_type(BlockNode)}

#         if self.parent_name:

#             compiled_parent = self.get_parent(context)

#             if BLOCK_CONTEXT_KEY not in context.render_context:
#                 context.render_context[BLOCK_CONTEXT_KEY] = BlockContext()
#             block_context = context.render_context[BLOCK_CONTEXT_KEY]

#             # Add the block nodes from this node to the block context
#             block_context.add_blocks(self.blocks)

#             # If this block's parent doesn't have an extends node it is the root,
#             # and its block nodes also need to be added to the block context.
#             for node in compiled_parent.nodelist:
#                 # The ExtendsNode has to be the first non-text node.
#                 if not isinstance(node, TextNode):
#                     if not isinstance(node, ExtendsNode):
#                         blocks = {
#                             n.name: n
#                             for n in compiled_parent.nodelist.get_nodes_by_type(BlockNode)
#                         }
#                         block_context.add_blocks(blocks)
#                     break

#             # Call Template._render explicitly so the parser context stays
#             # the same.
#             # with context.render_context.push_state(compiled_parent, isolated_context=False):
#             #     return compiled_parent._render(context)
        




#         if self.isolated_context:
#             return template.render(context.new(values))
#         with context.push(**values):
#             return template.render(context)


# @register.tag("include_extends")
# def do_include(parser, token):
#     """
#     Load a template and render it with the current context. You can pass
#     additional context using keyword arguments.

#     Example::

#         {% include "foo/some_include" %}
#         {% include "foo/some_include" with bar="BAZZ!" baz="BING!" %}

#     Use the ``only`` argument to exclude the current context when rendering
#     the included template::

#         {% include "foo/some_include" only %}
#         {% include "foo/some_include" with bar="1" only %}
#     """
#     bits = token.split_contents()
#     print("bits: ", bits)
#     if len(bits) < 4:
#         raise TemplateSyntaxError(
#             "%r tag takes at least two argument: the name of the template to "
#             "be included and the template to be extended" % bits[0]
#         )

#     bits[3] = construct_relative_path(parser.origin.template_name, bits[3])
#     parent_name = parser.compile_filter(bits[3])

#     print("parent name: ", parent_name)

#     options = {}
#     remaining_bits = bits[4:]
#     while remaining_bits:
#         option = remaining_bits.pop(0)
#         if option in options:
#             raise TemplateSyntaxError(
#                 "The %r option was specified more than once." % option
#             )
#         if option == "with":
#             value = token_kwargs(remaining_bits, parser, support_legacy=False)
#             if not value:
#                 raise TemplateSyntaxError(
#                     '"with" in %r tag needs at least one keyword argument.' % bits[0]
#                 )
#         elif option == "only":
#             value = True
#         else:
#             raise TemplateSyntaxError(
#                 "Unknown argument for %r tag: %r." % (bits[0], option)
#             )
#         options[option] = value
#     isolated_context = options.get("only", False)
#     namemap = options.get("with", {})
#     bits[1] = construct_relative_path(parser.origin.template_name, bits[1])


#     return IncludeExtendNode(
#         parser.compile_filter(bits[1]),
#         parent_name=parent_name,
#         extra_context=namemap,
#         isolated_context=isolated_context,
#     )



# @register.tag("extends1")
# def do_extends(parser, token):
#     """
#     Signal that this template extends a parent template.

#     This tag may be used in two ways: ``{% extends "base" %}`` (with quotes)
#     uses the literal value "base" as the name of the parent template to extend,
#     or ``{% extends variable %}`` uses the value of ``variable`` as either the
#     name of the parent template to extend (if it evaluates to a string) or as
#     the parent template itself (if it evaluates to a Template object).
#     """
#     bits = token.split_contents()
#     if len(bits) != 2:
#         raise TemplateSyntaxError("'%s' takes one argument" % bits[0])
#     bits[1] = construct_relative_path(parser.origin.template_name, bits[1])
#     parent_name = parser.compile_filter(bits[1])
#     nodelist = parser.parse()

#     nodelist.extend(collect_blocks(nodelist))

#     # print("include block: ", blocks)

#     if nodelist.get_nodes_by_type(ExtendsNode):
#         raise TemplateSyntaxError(
#             "'%s' cannot appear more than once in the same template" % bits[0]
#         )
    

#     return ExtendsNode(nodelist, parent_name,)
#     # extend_node.must_be_first = False

#     # return extend_node

# def collect_blocks(nodelist):
#     blocks = NodeList()
#     for node in nodelist:
#         # print("node includes: ", node)

#         if isinstance(node, BlockNode):
#             # blocks[node.name] = node

#             new_node_list = NodeList()
#             for x in node.nodelist:
#                 if isinstance(x, IncludeNode):
#                     included_blocks = resolve_included_blocks(x)
#                     print("Include node", included_blocks)
#                     new_node_list.extend(included_blocks)
#                     # new_node_list.extend(collect_blocks(node.nodelist))

#                 else:
#                     new_node_list.append(x)


#             new_block = BlockNode(node.name, new_node_list, node.parent)
#             blocks.append(new_block)
#             # blocks[node.name] = new_node


#             # blocks.update(collect_blocks(node.nodelist))
            


#         elif isinstance(node, IncludeNode):
#             included_blocks = resolve_included_blocks(node)
#             blocks.append(included_blocks)

#     return blocks

# def resolve_included_blocks(node):
#     """
#     Recursively resolve included template blocks, handling nested includes.
#     """
#     # Attempt to simulate rendering to resolve the template name
#     fake_context = Context()
#     included_template_name = node.template.resolve(fake_context)
#     included_template = loader.get_template(included_template_name)

#     # Collect blocks from the included template
#     return collect_blocks(included_template.template.nodelist)

# class ExtendsNode(Node):
#     must_be_first = False
#     context_key = "extends_context"

#     def __init__(self, nodelist, parent_name, template_dirs=None):
#         self.nodelist = nodelist
#         self.parent_name = parent_name
#         self.template_dirs = template_dirs
#         self.blocks = {n.name: n for n in nodelist.get_nodes_by_type(BlockNode)}

#         # self.included_blocks = included_blocks
#         print("blocks: ", self.blocks)
#         # print("blocks: ", [type(z)  for x,y in blocks.items() for z in y.nodelist], blocks)

#     def __repr__(self):
#         return "<%s: extends %s>" % (self.__class__.__name__, self.parent_name.token)

#     def find_template(self, template_name, context):
#         """
#         This is a wrapper around engine.find_template(). A history is kept in
#         the render_context attribute between successive extends calls and
#         passed as the skip argument. This enables extends to work recursively
#         without extending the same template twice.
#         """
#         history = context.render_context.setdefault(
#             self.context_key,
#             [self.origin],
#         )
#         template, origin = context.template.engine.find_template(
#             template_name,
#             skip=history,
#         )
#         history.append(origin)
#         return template

#     def get_parent(self, context):
#         parent = self.parent_name.resolve(context)
#         if not parent:
#             error_msg = "Invalid template name in 'extends' tag: %r." % parent
#             if self.parent_name.filters or isinstance(self.parent_name.var, Variable):
#                 error_msg += (
#                     " Got this from the '%s' variable." % self.parent_name.token
#                 )
#             raise TemplateSyntaxError(error_msg)
#         if isinstance(parent, Template):
#             # parent is a django.template.Template
#             return parent
#         if isinstance(getattr(parent, "template", None), Template):
#             # parent is a django.template.backends.django.Template
#             return parent.template
#         return self.find_template(parent, context)

#     def render(self, context):
#         compiled_parent = self.get_parent(context)

#         if BLOCK_CONTEXT_KEY not in context.render_context:
#             context.render_context[BLOCK_CONTEXT_KEY] = BlockContext()
#         block_context = context.render_context[BLOCK_CONTEXT_KEY]

#         # Add the block nodes from this node to the block context
#         block_context.add_blocks(self.blocks)

#         # If this block's parent doesn't have an extends node it is the root,
#         # and its block nodes also need to be added to the block context.
#         for node in compiled_parent.nodelist:
#             # The ExtendsNode has to be the first non-text node.
#             if not isinstance(node, TextNode):
#                 if not isinstance(node, ExtendsNode):
#                     blocks = {
#                         n.name: n
#                         for n in compiled_parent.nodelist.get_nodes_by_type(BlockNode)
#                     }
#                     block_context.add_blocks(blocks)
#                 break

#         # Call Template._render explicitly so the parser context stays
#         # the same.
#         with context.render_context.push_state(compiled_parent, isolated_context=False):
#             return compiled_parent._render(context)


