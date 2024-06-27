
from django.forms import forms
from django.db.models import FileField
from django.utils.translation import gettext_lazy as _


def format_bytes(size):
    """ formats the bytes into human readable form """
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'k', 2: 'm', 3: 'g', 4: 't'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {power_labels[n]}b"


class ContentTypeRestrictedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB - 104857600
            250MB - 214958080
            500MB - 429916160
    """
    """
        content_types: list
        max_upload_size: int
    """
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop('content_types', [])
        self.max_upload_size = kwargs.pop('max_upload_size', 0)

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

        try:
            file = data.file
            content_type = file.content_type
         
            if content_type in self.content_types:
                if file.size > self.max_upload_size:

                    raise forms.ValidationError(_(f'Please keep filesize under {format_bytes(self.max_upload_size)}. Current filesize {format_bytes(file.size)}'))
            else:
                raise forms.ValidationError(_('Filetype not supported.'))
        except (AttributeError, Exception):
            pass

        return data