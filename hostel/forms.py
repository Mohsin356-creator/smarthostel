from django import forms
from .models import Student, Room, Fee, Expense


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['hostel', 'room', 'student_id', 'full_name', 'father_name', 'phone', 'cnic', 'admission_date', 'monthly_fee', 'status']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['hostel', 'room_number', 'floor', 'total_beds', 'monthly_rent']


class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['student', 'fee_month', 'monthly_fee', 'paid_amount', 'due_date']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['hostel', 'category', 'description', 'amount', 'expense_date']