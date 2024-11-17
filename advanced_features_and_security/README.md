# Blog Application Permissions and Groups

This Django application uses custom permissions and groups to control user access to different views.

## Custom Permissions:
- `can_view`: Permission to view a blog post.
- `can_create`: Permission to create a new blog post.
- `can_edit`: Permission to edit an existing blog post.
- `can_delete`: Permission to delete a blog post.

## Groups:
- **Admins**: Full access to all permissions.
- **Editors**: Can create and edit blog posts.
- **Viewers**: Can only view blog posts.

## How to Test:
1. Create users and assign them to different groups in the Django admin.
2. Log in as users with different roles and test access to blog post actions.
