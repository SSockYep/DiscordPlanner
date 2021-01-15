from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import NewPlanForm

# Create your views here.


# class NewPlanView(FormView):
#     template_name = 'new_plan.html'

#     def __init__(self, *args, **kwargs):
#         super(NewPlanView, self).__init__(*args, **kwargs)
#         self.form_class = NewPlanForm(
#             [('1', 'One'), ('2', 'Two'), ('3', 'Three')])

def newPlan(request):
    if request.method == 'POST':
        print(request.POST)
        guild = request.POST['guild']
        plan_name = request.POST['plan_name']
        datetime = request.POST['datetime']
        if request.POST['attendee_num']:
            attendee_num = int(request.POST['attendee_num'])
        else:
            attendee_num = 0
        print(guild, plan_name, datetime, attendee_num)
        return redirect('/')
    else:
        my_form = NewPlanForm()
        my_form.fields['guild'].choices = [
            ('1', 'One'), ('2', 'Two'), ('3', 'Three')]
        context = {
            'form': my_form,
        }
        return render(request, 'new_plan.html', context)
