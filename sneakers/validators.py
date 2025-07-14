from django.core.exceptions import ValidationError


def validate_filetype(value):
    """
    Validates that provided file is a png or jpeg.
    """
    
    extension = value.name.split('.')[-1]

    if extension.lower() not in ('png', 'jpg', 'jpeg'):
        raise ValidationError('File must be a PNG or JPG.')


def validate_filesize(value):
    """
    Validates that provided file is <= 2mb
    """

    MAX_FILESIZE = 2 #mb

    limit = MAX_FILESIZE * 1024 * 1024
    
    if value.size > limit:
        raise ValidationError(f'Filesize exceeds limit of {MAX_FILESIZE}MB.')