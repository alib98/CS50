from django import forms

class AddForm(forms.Form):
    title = forms.CharField(label="Title", max_length=20)
    content = forms.CharField(widget=forms.Textarea)

class EditForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    content = forms.CharField(widget=forms.Textarea)
    # class Meta:
    #     fields = ['content']
    #     widgets = {
    #         'title': forms.TextInput(attrs={'readonly':'readonly'}),
    #     }