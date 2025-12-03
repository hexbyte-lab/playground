from django.shortcuts import render, get_object_or_404
from .models import Lesson


ROADMAP_ORDER = ['basics', 'data_structures', 'algorithms', 'interviews', 'other']

def lesson_list(request):
    selected_category = request.GET.get('category')
    category_map = dict(Lesson.CATEGORY_CHOICES)

    # get categories form lessons
    categories_raw = Lesson.objects.values_list('category', flat=True)
    categories_set = set(cat.strip() for cat in categories_raw if cat)

    # Sort categories according to roadmap order
    categories_sorted = [cat for cat in ROADMAP_ORDER if cat in categories_set]

    roadmap_categories = [{'code': cat, 'name': category_map.get(cat, cat)} for cat in categories_sorted]

    lessons_in_category = Lesson.objects.filter(category=selected_category).order_by('created_at') if selected_category else []
    latest_lessons = Lesson.objects.order_by('-created_at')[:5]

    selected_category_name = category_map.get(selected_category) if selected_category else None

    return render(request, 'lessons/lesson_list.html', {
        'roadmap_categories': roadmap_categories,
        'lessons_in_category': lessons_in_category,
        'latest_lessons': latest_lessons,
        'selected_category': selected_category,
        'selected_category_name': selected_category_name,
    })



def feedback(request):
    
    return render(request, 'feedback.html')

def lesson_detail(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug)
    return render(request, 'lessons/lesson_detail.html', {'lesson': lesson})

