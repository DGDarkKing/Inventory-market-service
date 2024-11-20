from enum import Enum


class ContentTypes:
    class Application(Enum):
        OCTET_STREAM = 'application/octet-stream'
        JS = 'application/javascript'
        ZIP = 'application/gzip'

    class Text(Enum):
        PLAIN = 'text/plain'
        HTML = 'text/html'
        CSS = 'text/css'
        JS = 'text/javascript'
        CSV = 'text/csv'
        XML = 'text/xml'

    class Image(Enum):
        BMP = 'image/bmp'
        PNG = 'image/png'
        JPEG = 'image/jpeg'
        WEBP = 'image/webp'

    class Video(Enum):
        H264 = 'video/h264'
        H265 = 'video/h265'
        MATROSKA = 'video/matroska'
        MP4 = 'video/mp4'

    class Multipart(Enum):
        FORM_DATA = 'multipart/form-data'
        BYTES = 'multipart/byteranges'


UploadedContentType = (
        ContentTypes.Application
        | ContentTypes.Text
        | ContentTypes.Video
        | ContentTypes.Image
)
