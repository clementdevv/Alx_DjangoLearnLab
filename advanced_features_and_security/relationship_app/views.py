from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import CustomUser

@permission_required('relationship_app.can_view_user', raise_exception=True)
def view_users(request):
    users = CustomUser.objects.all()
    return render(request, 'relationship_app/view_users.html', {'users': users})

@permission_required('relationship_app.can_create_user', raise_exception=True)
def create_user(request):
    if request.method == 'POST':
        # Logic to create a new user
        return render(request, 'relationship_app/create_user.html')
    return render(request, 'relationship_app/create_user.html')

@permission_required('relationship_app.can_edit_user', raise_exception=True)
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        # Logic to edit the user
        return render(request, 'relationship_app/edit_user.html', {'user': user})
    return render(request, 'relationship_app/edit_user.html', {'user': user})

@permission_required('relationship_app.can_delete_user', raise_exception=True)
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return render(request, 'relationship_app/delete_user.html')
