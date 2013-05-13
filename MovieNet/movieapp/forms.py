from django import forms


class SearchForm(forms.Form):
    

    movie_title = forms.CharField(required=False)
    actor_name = forms.CharField(required=False)
    director_name = forms.CharField(required=False)
    show_oscars = forms.BooleanField(required=False)

    start_year = forms.IntegerField(required=False,max_value=2013,min_value=1900)
    end_year = forms.IntegerField(required=False,max_value=2013,min_value=1900)
    
    #min_rating = forms.DecimalField(required=False,max_value=10,min_value=1,max_digits=3, decimal_places=2)
    #max_rating = forms.DecimalField(required=False,max_value=10,min_value=1,max_digits=3,decimal_places=2)
    
    
class BasicSearchForm(forms.Form):
    query = forms.CharField(required=True)
    search_type = forms.ChoiceField(choices=[("movie","Movies"),("actor","Actors"),("director","Directors")])

    