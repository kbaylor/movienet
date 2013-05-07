from django import forms


class SearchForm(forms.Form):
    movie_title = forms.CharField(required=False)
    actor_name = forms.CharField(required=False)
    director_name = forms.CharField(required=False)
    show_oscars = forms.BooleanField(required=False)

    start_year = forms.IntegerField(required=False,max_value=2013,min_value=1900)
    end_year = forms.IntegerField(required=False,max_value=2013,min_value=1900)
    
    