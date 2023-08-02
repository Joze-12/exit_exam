from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from academics.models import *
from django.core.exceptions import ObjectDoesNotExist


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        ACADEMIC_MANAGER = "ACADEMIC_MANAGER", "Academic_Manager"
        DEPARTMENT_HEAD = "DEPARTMENT_HEAD", "Department_Head"
        DATA_CLERK = "DATA_CLERK", "Data_Clerk"
        INSTRUCTOR = "INSTRUCTOR", "Instructor"
        STUDENT = "STUDENT", "Student"

    objects = CustomUserManager()

    password_changed = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=Role.choices)
    email = models.EmailField(unique=True, blank=False, null=False)
    profile_photo = models.ImageField(upload_to="profile_images/",null=True, blank=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def get_profile_url(self):
        return f"/users/profile/{self.pk}/"

    def get_role_display(self):
        return dict(self.Role.choices)[self.role]

    def has_role(self, role_name):
        return self.role == role_name

    def is_academic_manager(self):
        return self.role == self.Role.ACADEMIC_MANAGER

    def is_department_head(self):
        return self.role == self.Role.DEPARTMENT_HEAD

    def is_data_clerk(self):
        return self.role == self.Role.DATA_CLERK

    def is_instructor(self):
        return self.role == self.Role.INSTRUCTOR

    def is_student(self):
        return self.role == self.Role.STUDENT

    def has_profile_photo(self):
        return bool(self.profile_photo)


class AcademicModelManager(models.Manager):
    def create_user(self, role, **kwargs):
        role = User.Role.ACADEMIC_MANAGER
        user = self.model(role=role, **kwargs)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(role=User.Role.ACADEMIC_MANAGER)
        )

    def normalize_email(self, email):
        """
        Normalize the email address by lowercasing the domain part.
        """
        email_name, domain_part = email.strip().rsplit("@", 1)
        return f"{email_name}@{domain_part.lower()}"


class AcademicManager(User):
    objects = AcademicModelManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = User.Role.ACADEMIC_MANAGER
        return super().save(*args, **kwargs)
    
    def create_department(self, name, description=None):
        return Department.objects.create(name=name, description=description)

    def update_department(self, department_id, name=None, description=None):
        department = Department.objects.get(pk=department_id)
        if name:
            department.name = name
        if description:
            department.description = description
        department.save()
        return department

    def delete_department(self, department_id):
        Department.objects.filter(pk=department_id).delete()

    def register_department_head(self, first_name, last_name, username, email, password):
        try:
            department_head = DepartmentHead.objects.get(username=username)
            if department_head.is_department_head():
                raise ValueError(f"Department Head with username '{username}' already registered.")
        except DepartmentHead.DoesNotExist:
            department_head = DepartmentHead.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                role=User.Role.INSTRUCTOR,
            )

        return department_head
    
    def set_department_head_inactive(self, department_head_id):
        try:
            department_head = DepartmentHead.objects.get(pk=department_head_id)
            department_head.is_active = False
            department_head.save()
            return True
        except DepartmentHead.DoesNotExist:
            return False

    def delete_department_head(self, department_head_id):
        DepartmentHead.objects.filter(pk=department_head_id).delete()

    def set_next_exam_date(self, exam_date):
        try:
            exit_exam_date = ExitExamDate.objects.get()
            exit_exam_date.exam_date = exam_date
            exit_exam_date.save()
        except ExitExamDate.DoesNotExist:
            ExitExamDate.objects.create(exam_date=exam_date)
    
    def assign_department_head_to_department(self, department_head_id, department_id):
        department_head = DepartmentHead.objects.get(pk=department_head_id)
        department = Department.objects.get(pk=department_id)
        department_head.department = department
        department_head.save()
        return department_head
    
    def revoke_department_head_assignment(self, department_head_id):
        department_head = DepartmentHead.objects.get(pk=department_head_id)
        department_head.department = None
        department_head.save()
        return department_head
    


class DepartmentHeadManager(models.Manager):
    def create_user(self, role, **kwargs):
        role = User.Role.DEPARTMENT_HEAD
        user = self.model(role=role, **kwargs)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        return (
            super().get_queryset(*args, **kwargs).filter(role=User.Role.DEPARTMENT_HEAD)
        )

    def normalize_email(self, email):
        """
        Normalize the email address by lowercasing the domain part.
        """
        email_name, domain_part = email.strip().rsplit("@", 1)
        return f"{email_name}@{domain_part.lower()}"


class DepartmentHead(User):
    objects = DepartmentHeadManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = User.Role.DEPARTMENT_HEAD
        return super().save(*args, **kwargs)
    
    def get_department(self):
        try:
            return self.department  # Access the related Department object
        except Department.DoesNotExist:
            return None
    
    def create_course(self, name, code, description):
        department = self.get_department()
        if department:
            return Course.objects.create(name=name, code=code, description=description, department=department)
        return None

    def update_course(self, course_id, name=None, code=None, description=None):
        try:
            course = Course.objects.get(pk=course_id, department=self.get_department())
            if name:
                course.name = name
            if code:
                course.code = code
            if description:
                course.description = description
            course.save()
            return course
        except Course.DoesNotExist:
            return None

    def delete_course(self, course_id):
        try:
            course = Course.objects.get(pk=course_id, department=self.get_department())
            course.delete()
            return True
        except Course.DoesNotExist:
            return False

    def create_theme(self, name, description):
        department = self.get_department()
        if department:
            return Theme.objects.create(name=name, description=description, department=department)
        return None

    def update_theme(self, theme_id, name=None, description=None):
        try:
            theme = Theme.objects.get(pk=theme_id, department=self.get_department())
            if name:
                theme.name = name
            if description:
                theme.description = description
            theme.save()
            return theme
        except Theme.DoesNotExist:
            return None

    def delete_theme(self, theme_id):
        try:
            theme = Theme.objects.get(pk=theme_id, department=self.get_department())
            theme.delete()
            return True
        except Theme.DoesNotExist:
            return False

    def assign_instructor_to_course(self, instructor_id, course_id):
        try:
            instructor = Instructor.objects.get(pk=instructor_id)
            course = Course.objects.get(pk=course_id, department=self.get_department())
            course.instructor = instructor
            course.save()
            return course
        except (Instructor.DoesNotExist, Course.DoesNotExist):
            return None

    def revoke_instructor_assignment(self, course_id):
        try:
            course = Course.objects.get(pk=course_id, department=self.get_department())
            course.instructor = None
            course.save()
            return course
        except Course.DoesNotExist:
            return None
    
    def register_instructor(self, first_name, last_name, username, email, password):
        try:
            instructor = Instructor.objects.get(username=username)
            if instructor.is_instructor():
                raise ValueError(f"Instructor with username '{username}' already registered.")
        except Instructor.DoesNotExist:
            instructor = Instructor.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                role=User.Role.INSTRUCTOR,
            )

        return instructor
    
    def set_instructor_inactive(self, instructor_id):
        try:
            instructor = Instructor.objects.get(pk=instructor_id)
            instructor.is_active = False
            instructor.save()
            return True
        except Instructor.DoesNotExist:
            return False


class DataClerkManager(models.Manager):
    def create_user(self, role, **kwargs):
        role = User.Role.DATA_CLERK
        user = self.model(role=role, **kwargs)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.DATA_CLERK)

    def normalize_email(self, email):
        """
        Normalize the email address by lowercasing the domain part.
        """
        email_name, domain_part = email.strip().rsplit("@", 1)
        return f"{email_name}@{domain_part.lower()}"


class DataClerk(User):
    objects = DataClerkManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = User.Role.DATA_CLERK
        return super().save(*args, **kwargs)
    
    def set_approve_student_status(self, student_id, approved):
        try:
            student_profile = StudentProfile.objects.get(pk=student_id)
            student_profile.approved = approved
            student_profile.save()
            return True
        except StudentProfile.DoesNotExist:
            return False
    
    def set_reject_student_status(self, student_id, rejected):
        try:
            student_profile = StudentProfile.objects.get(pk=student_id)
            student_profile.rejected = rejected
            student_profile.save()
            return True
        except StudentProfile.DoesNotExist:
            return False
    
    def set_student_exam_result(self, student_id, exam_result):
        try:
            student_profile = StudentProfile.objects.get(student_id=student_id)
            student_profile.exam_result = exam_result
            student_profile.save()
            return True
        except StudentProfile.DoesNotExist:
            return False

    def set_student_exam_score(self, student_id, exam_score):
        try:
            student_profile = StudentProfile.objects.get(student_id=student_id)
            student_profile.exam_score = exam_score
            student_profile.save()
            return True
        except StudentProfile.DoesNotExist:
            return False

    def set_student_paid_status(self, student_id, paid):
        try:
            student_profile = StudentProfile.objects.get(student_id=student_id)
            student_profile.paid = paid
            student_profile.save()
            return True
        except StudentProfile.DoesNotExist:
            return False

    def set_student_exit_credentials(self, student_id, exit_username, exit_password):
        try:
            student_profile = StudentProfile.objects.get(student_id=student_id)
            student_profile.exit_username = exit_username
            student_profile.exit_password = exit_password
            student_profile.save()
            return True
        except StudentProfile.DoesNotExist:
            return False

    def set_student_exam_room(self, student_id, exam_room_id):
        try:
            student_profile = StudentProfile.objects.get(student_id=student_id)
            exam_room = ExamRoom.objects.get(pk=exam_room_id)
            student_profile.exam_room = exam_room
            student_profile.save()
            return True
        except (StudentProfile.DoesNotExist, ExamRoom.DoesNotExist):
            return False


class InstructorManager(models.Manager):
    def create_user(self, role, **kwargs):
        role = User.Role.INSTRUCTOR
        user = self.model(role=role, **kwargs)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.INSTRUCTOR)

    def normalize_email(self, email):
        """
        Normalize the email address by lowercasing the domain part.
        """
        email_name, domain_part = email.strip().rsplit("@", 1)
        return f"{email_name}@{domain_part.lower()}"


class Instructor(User):
    objects = InstructorManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = User.Role.INSTRUCTOR
        return super().save(*args, **kwargs)


class StudentManager(models.Manager):
    def create_user(self, role, **kwargs):
        role = User.Role.STUDENT
        user = self.model(role=role, **kwargs)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.STUDENT)

    def normalize_email(self, email):
        """
        Normalize the email address by lowercasing the domain part.
        """
        email_name, domain_part = email.strip().rsplit("@", 1)
        return f"{email_name}@{domain_part.lower()}"


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = User.Role.STUDENT
        return super().save(*args, **kwargs)

    def get_exam_result(self):
        try:
            student_profile = StudentProfile.objects.get(user=self)
            return student_profile.exam_result, student_profile.exam_score
        except StudentProfile.DoesNotExist:
            return None, None

    def get_department(self):
        try:
            student_profile = StudentProfile.objects.get(user=self)
            return student_profile.department
        except StudentProfile.DoesNotExist:
            return None

    def get_program(self):
        try:
            student_profile = StudentProfile.objects.get(user=self)
            return student_profile.get_program_display()
        except StudentProfile.DoesNotExist:
            return None

    def get_student_id(self):
        try:
            student_profile = StudentProfile.objects.get(user=self)
            return student_profile.student_id
        except StudentProfile.DoesNotExist:
            return None

    def get_section(self):
        try:
            student_profile = StudentProfile.objects.get(user=self)
            return student_profile.section
        except StudentProfile.DoesNotExist:
            return None

    def get_exit_username(self):
        try:
            student_profile = StudentProfile.objects.get(user=self)
            return student_profile.exit_username
        except StudentProfile.DoesNotExist:
            return None

    def get_exit_password(self):
        try:
            student_profile = StudentProfile.objects.get(user=self)
            return student_profile.exit_password
        except StudentProfile.DoesNotExist:
            return None

    def get_exam_room(self):
        try:
            student_profile = StudentProfile.objects.get(user=self)
            return student_profile.exam_room
        except StudentProfile.DoesNotExist:
            return None
        
    def get_courses(self):
        department = self.get_department()
        if department:
            return Course.objects.filter(department=department)
        return []

@receiver(post_save, sender=Student)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "STUDENT":
        StudentProfile.objects.create(user=instance)


class StudentProfile(models.Model):
    class Program(models.TextChoices):
        REGULAR = "REGULAR", "Regular"
        EXTENSION = "EXTENSION", "Extension"

    class ExamResult(models.TextChoices):
        PASSED = "PASSED", "Passed"
        FAILD = "FAILD", "Failed"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(
        "academics.Department", on_delete=models.SET_NULL, null=True
    )
    section = models.ForeignKey(
        "academics.Section", on_delete=models.SET_NULL, null=True
    )
    program = models.CharField(
        max_length=15, choices=Program.choices, default=Program.REGULAR
    )
    exam_resut = models.CharField(
        max_length=6, choices=ExamResult.choices, null=True, blank=True
    )
    exam_score = models.IntegerField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    exit_username = models.CharField(max_length=15, null=True, blank=True)
    exit_password = models.CharField(max_length=15, null=True, blank=True)
    exam_room = models.ForeignKey(
        "academics.ExamRoom", on_delete=models.SET_NULL, null=True, blank=True
    )
    rejected = models.BooleanField(default=True)