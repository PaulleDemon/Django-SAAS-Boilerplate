from django import forms
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.forms.renderers import get_default_renderer
from unfold.contrib.forms.widgets import WysiwygWidget


class JSPath:
    def __html__(self):
        return (
            f'<script src="https://cdn.jsdelivr.net/npm/trix@2.1.1/dist/trix.umd.min.js"></script>'
        )


class JSCode:
    def __html__(self):
        return (
            """
            <script type="text/javascript" src="{% static "templates/js/trix.js" %}">
                
            </script>
            """
        )


class CSSPath:
    def __html__(self):
        return (
            f'<link href="https://cdn.jsdelivr.net/npm/trix@2.1.1/dist/trix.min.css" rel="stylesheet">'
        )


class CSSAdminCode:
    def __html__(self):
        return (
            """
            <style>
                .flex-container:has(trix-editor) {
                    display: block !important;
                }

                .field-body .flex-container{ /* fallback for edge browser */
                    display: block !important;
                }

                .trix-button-row{
                    zindex: 10 !important;
                }
                
                trix-toolbar .trix-button {
                    background-color: #d1d1d1 !important;
                }
                .trix-editor > h2 {
                    font-size: 1.5em !important;
                    line-height: 1.2;
                    font-weight: 500;
                    margin: 0;
                    background: transparent;
                    color: var(--body-fg);
                }
                trix-editor figure {
                    z-index: -1 !important;
                }
            </style>
            """
        )


class TrixEditorWidget(forms.Textarea):
    
    class Media:
        js = [
            # JSCode(),
            JSPath(),
            "js/trix.js"
        ]
        css = {
            'all': [CSSAdminCode(), CSSPath()],
        }
    
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs['hidden'] = True
        html = super().render(name, value, attrs=attrs, renderer=renderer)
        return mark_safe(f'{html}<trix-editor class="trix-editor" input="{attrs["id"]}"></trix-editor>')

    # def format_value(self, value):
    #     return ""


class UnfoldTrix(WysiwygWidget):

    class Media:
        css = {"all": ("unfold/forms/css/trix.css", CSSAdminCode())}
        js = (
            "unfold/forms/js/trix.js",
            "unfold/forms/js/trix.config.js",
            "js/trix.js"
        )