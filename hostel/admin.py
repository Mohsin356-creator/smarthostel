from django.contrib import admin
from .models import Hostel, Room, Student, Fee, Expense

admin.site.register(Hostel)
admin.site.register(Room)
admin.site.register(Student)
admin.site.register(Fee)
admin.site.register(Expense)