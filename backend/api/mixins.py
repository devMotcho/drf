from rest_framework import permissions

from .permissions import IsStaffEditorPermission


class StaffEditorPermissionMixin():
    permission_classes = [
        permissions.IsAdminUser,
        IsStaffEditorPermission
        ]
    
class UserQuerysetMixin():
    user_field = 'user'
    allow_staff_view = False
    
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        # map a dict with all the products
        lookup_data = {}
        lookup_data[self.user_field] = self.request.user
        
        # search for all products with request.user as 'user'
        qs = super().get_queryset(*args, **kwargs)
        if user.is_staff:
            return qs
        return qs.filter(**lookup_data) # self.user_field = self.request.user