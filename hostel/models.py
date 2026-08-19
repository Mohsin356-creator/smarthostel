from django.db import models


class Hostel(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    owner_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    floor = models.CharField(max_length=50, blank=True)
    total_beds = models.PositiveIntegerField(default=1)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Room {self.room_number}"


class Student(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('left', 'Left Hostel'),
        ('suspended', 'Suspended'),
    ]

    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='students')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    student_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    cnic = models.CharField(max_length=20, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"


class Fee(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('partial', 'Partial'),
        ('unpaid', 'Unpaid'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    fee_month = models.DateField()
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid')

    def save(self, *args, **kwargs):
        self.remaining_amount = self.monthly_fee - self.paid_amount
        if self.paid_amount >= self.monthly_fee:
            self.status = 'paid'
        elif self.paid_amount > 0:
            self.status = 'partial'
        else:
            self.status = 'unpaid'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.full_name} - {self.fee_month}"


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('electricity', 'Electricity'),
        ('gas', 'Gas'),
        ('water', 'Water'),
        ('internet', 'Internet'),
        ('food', 'Food'),
        ('salaries', 'Salaries'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other'),
    ]

    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=300, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.amount}"