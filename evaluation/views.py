from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls.base import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from .models import Instructor, Evaluation
from .filters import InstructorFilter
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    View,
    DeleteView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from data import departments


class InstructorListView(ListView):

    model = Instructor
    paginate_by = 10

    def get_context_data(self, **kwargs):
        name = self.request.GET.get("name__icontains", default="")
        department = self.request.GET.get("department", default="")

        filter_qs = InstructorFilter(self.request.GET, Instructor.objects.all().order_by('name'))
        context = super().get_context_data(**kwargs, object_list = filter_qs.qs)
        context['departments'] = departments
        context['selected_department'] = department
        context['selected_name'] = name
        context['selected_search'] = f"name__icontains={name}&department={department}"

        return context


class Evaluate(UpdateView):

    model = Instructor

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        rating_1 = int(request.POST.get("rating", 0)) * 20
        rating_2 = int(request.POST.get("ratingtwo", 0)) * 20
        rating_3 = int(request.POST.get("ratingthree", 0)) * 20
        comment = request.POST["comment"]

        if Evaluation.objects.filter(user=request.user, instructor=self.object):
            messages.success(request, """You have RATED this instructor before, 
                click `My Evaluations` from your profile to edit it""")
            return redirect(reverse("evaluation:detail", kwargs={"pk": self.object.pk}))
        
        rating = Evaluation.objects.create(
            comment=comment,
            grading=rating_1,
            teaching=rating_2,
            personality=rating_3,
            user=request.user,
            instructor=self.object,
        )

        messages.success(request, "Evaluation Was Submitted.")
        return redirect(reverse("evaluation:detail", kwargs={"pk": self.object.pk}))


class InstructorCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):

    permission_required = ["evaluation.add_instructor"]
    model = Instructor
    fields = ["name", "department", "profile_pic"]
    success_url = reverse_lazy("evaluation:instructors")
    success_message = "The instructor was added"


class InstructorDeleteView(PermissionRequiredMixin, DeleteView):

    permission_required = ["evaluation.delete_instructor"]
    permission_denied_message = "403; You do not have the permission :("
    raise_exception = True
    model = Instructor
    success_url = reverse_lazy("evaluation:index")


class InstructorDetailView(DetailView):

    model = Instructor


class EvaluationListView(ListView):

    model = Evaluation


class EvaluationUpdateView(UpdateView):

    model = Evaluation
    fields = ["grading", "teaching", "personality", "comment"]
    success_url = reverse_lazy("evaluation:instructors")

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        messages.success(request, "Evaluation Was Updated.")
        return redirect(reverse("evaluation:evaluation_list", kwargs={"pk": request.user.pk}))