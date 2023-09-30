from django.shortcuts import render, redirect
from .models import Repair, Tag
from .forms import RepairForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import search_repairs, paginate_repairs
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages


# Create your views here.

def repairs(request):
    pr, search_query = search_repairs(request)
    custom_range, pr = paginate_repairs(request, pr, 3)

    context = {
        'repairs': pr,  # придумаем ключ
        'search_query': search_query,
        # 'paginator': paginator,
        'custom_range': custom_range,
    }
    return render(request, 'repairs/repairs.html', context)


def repair(request, pk):
    repair_obj = Repair.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.repair = repair_obj
        review.owner = request.user.profile
        review.save()

        repair_obj.get_vote_count()

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('repair', pk=repair_obj.id)

    return render(request, 'repairs/single-repair.html', {
        'repair': repair_obj,
        'form': form
    })


@login_required(login_url="login")
def create_repair(request):
    profile = request.user.profile
    form = RepairForm()  # отрабатывает методом get

    # при нажатии на кнопку
    if request.method == 'POST':
        form = RepairForm(request.POST, request.FILES)
        if form.is_valid():
            repair = form.save(commit=False)
            repair.owner = profile
            form.save()
            # когда пользователь заполнит форму то перенаправим на главную страницу
            return redirect('account')

    context = {'form': form}
    return render(request, 'repairs/form-template.html', context)


@login_required(login_url="login")
def update_repair(request, pk):
    profile = request.user.profile
    repair = profile.repair_set.get(id=pk)
    form = RepairForm(instance=repair)

    if request.method == "POST":
        form = RepairForm(request.POST, request.FILES, instance=repair)
        if form.is_valid():
            repair = form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'repairs/form-template.html', context)


@login_required(login_url="login")
def delete_repair(request, pk):
    profile = request.user.profile
    repair = profile.repair_set.get(id=pk)

    if request.method == "POST":
        repair.delete()
        return redirect('repairs')

    context = {'object': repair}
    return render(request, 'repairs/delete.html', context)
