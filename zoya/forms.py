from django.forms import ModelForm
from zoya.models import CommunityForum
from django.utils.html import strip_tags

class CommunityForumForm(ModelForm):
    class Meta:
        model = CommunityForum
        fields = ["comment"]
        
    def clean_comment(self):
        comment = self.cleaned_data["comment"]
        return strip_tags(comment)