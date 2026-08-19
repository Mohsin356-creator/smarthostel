from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Student, Room, Fee, Expense, Hostel
from .forms import StudentForm, RoomForm, FeeForm, ExpenseForm


def get_active_hostel(request):
    hostel_id = request.session.get('active_hostel_id')
    if hostel_id:
        hostel = Hostel.objects.filter(pk=hostel_id).first()
        if hostel:
            return hostel
    return Hostel.objects.first()


@login_required
def switch_hostel(request, pk):
    hostel = get_object_or_404(Hostel, pk=pk)
    request.session['active_hostel_id'] = hostel.pk
    return redirect('dashboard')


@login_required
def dashboard(request):
    active_hostel = get_active_hostel(request)
    all_hostels = Hostel.objects.all()

    total_students = Student.objects.filter(hostel=active_hostel, status='active').count()
    total_rooms = Room.objects.filter(hostel=active_hostel).count()
    pending_fees = Fee.objects.filter(student__hostel=active_hostel, status__in=['unpaid', 'partial']).count()

    total_revenue = Fee.objects.filter(student__hostel=active_hostel).aggregate(total=Sum('paid_amount'))['total'] or 0
    total_expenses = Expense.objects.filter(hostel=active_hostel).aggregate(total=Sum('amount'))['total'] or 0
    net_profit = total_revenue - total_expenses

    context = {
        'active_hostel': active_hostel,
        'all_hostels': all_hostels,
        'total_students': total_students,
        'total_rooms': total_rooms,
        'pending_fees': pending_fees,
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
    }
    return render(request, 'hostel/dashboard.html', context)


@login_required
def student_list(request):
    active_hostel = get_active_hostel(request)
    students = Student.objects.filter(hostel=active_hostel)
    return render(request, 'hostel/student_list.html', {'students': students, 'active_hostel': active_hostel, 'all_hostels': Hostel.objects.all()})


@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'hostel/add_student.html', {'form': form})


@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'hostel/add_student.html', {'form': form})


@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'hostel/confirm_delete.html', {'object': student})


@login_required
def room_list(request):
    active_hostel = get_active_hostel(request)
    rooms = Room.objects.filter(hostel=active_hostel)
    return render(request, 'hostel/room_list.html', {'rooms': rooms, 'active_hostel': active_hostel, 'all_hostels': Hostel.objects.all()})


@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'hostel/add_room.html', {'form': form})


@login_required
def edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'hostel/add_room.html', {'form': form})


@login_required
def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('room_list')
    return render(request, 'hostel/confirm_delete.html', {'object': room})


@login_required
def fee_list(request):
    active_hostel = get_active_hostel(request)
    fees = Fee.objects.filter(student__hostel=active_hostel)
    return render(request, 'hostel/fee_list.html', {'fees': fees, 'active_hostel': active_hostel, 'all_hostels': Hostel.objects.all()})


@login_required
def add_fee(request):
    if request.method == 'POST':
        form = FeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fee_list')
    else:
        form = FeeForm()
    return render(request, 'hostel/add_fee.html', {'form': form})


@login_required
def edit_fee(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == 'POST':
        form = FeeForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            return redirect('fee_list')
    else:
        form = FeeForm(instance=fee)
    return render(request, 'hostel/add_fee.html', {'form': form})


@login_required
def delete_fee(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == 'POST':
        fee.delete()
        return redirect('fee_list')
    return render(request, 'hostel/confirm_delete.html', {'object': fee})


@login_required
def expense_list(request):
    active_hostel = get_active_hostel(request)
    expenses = Expense.objects.filter(hostel=active_hostel)
    return render(request, 'hostel/expense_list.html', {'expenses': expenses, 'active_hostel': active_hostel, 'all_hostels': Hostel.objects.all()})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'hostel/add_expense.html', {'form': form})


@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'hostel/add_expense.html', {'form': form})


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'hostel/confirm_delete.html', {'object': expense})