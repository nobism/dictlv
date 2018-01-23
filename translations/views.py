from django.shortcuts import render, redirect
from translations.forms import SearchForm
from translations.models import English, Latvian
from translations.utils import get_translation

def home_page(request):
    """Returns the homepage
    """
    return render(request, 'home.html', {'form': SearchForm()})

# TODO: This view has a lot of if statements
def search(request):
    """Handles the search form which attempts to retrieve translations from the
    database.
    """
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            # TODO: also trim trailing whitespace, punctuation etc.
            user_in = form.data['text'].lower()
            lv_translations = get_translation(English, Latvian, user_in)
            en_translations = get_translation(Latvian, English, user_in)
            trans = []
            if lv_translations:
                trans = trans + lv_translations
            if en_translations:
                trans = trans + en_translations
            if trans:
                return render(request, 'result.html',
                              {'search_term': user_in, 'translations': trans, 'form': SearchForm()})
            else:
                # Remove special characters
                # if string is different
                    # search with modified string
                    # if result found
                        # return it
                return render(request, 'noresult.html', {'search_term': user_in, 'form': SearchForm()})
