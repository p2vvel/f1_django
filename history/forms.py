from django import forms


class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=255, label="Search", widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Search"}))

    # search_text.widget.attrs.update({'class': 'special'})