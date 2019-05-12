from django.shortcuts import render

# Create your views here.
def add(request):
    if request.method == 'POST':        # If the form has been submitted...
     form = InputForm(request.POST)     # A form bound to the POST data
     if form.is_valid():                # All validation rules pass
        cd = form.cleaned_data     # Process the data in form.cleaned_data
        input1 = cd['x']
        input2 = cd['y']
        output = input1 + input2
        return HttpResponseRedirect('/thanks/{output}/'.format(output=output)) # Redirect to new url
   else:
        form = InputForm()   # An unbound form
   return render(request, 'scraper/base.html', {'form': form })  