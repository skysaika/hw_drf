from rest_framework import serializers

# ссылку на видео должна быть с youtube.com
class YouTubeOnlyURLValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value.get('video_link'):
            if 'youtube.com' not in value.get('video_link'):
                raise serializers.ValidationError('Ссылка на видео должна быть только с youtube.com')
