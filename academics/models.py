from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    department_head = models.OneToOneField(
        "users.DepartmentHead", on_delete=models.SET_NULL, null=True
    )
    exam_date = models.DateTimeField(null=True, blank=True)
    exam_location = models.CharField(max_length=1024, null=True, blank=True)
    instructors = models.ManyToManyField("users.Instructor", related_name="departments")

    def __str__(self):
        return self.name
    
     # Getter function for exam_date field
    @property
    def exam_date(self):
        return self._exam_date

    # Setter function for exam_date field
    @exam_date.setter
    def exam_date(self, value):
        self._exam_date = value

    # Getter function for exam_location field
    @property
    def exam_location(self):
        return self._exam_location

    # Setter function for exam_location field
    @exam_location.setter
    def exam_location(self, value):
        self._exam_location = value

    def get_courses(self):
        return self.course_set.all()
    
    def get_department_head_name(self):
        if self.department_head:
            return self.department_head.name
        return None
    
    def get_total_students(self):
        return self.studentprofile_set.count()
    
    def get_related_themes(self):
        return self.theme_set.all()
    
    def get_next_exam_date(self):
        # Assuming the exam_date field contains a valid datetime value
        return self.exam_date
    
    def get_total_students_passed_exam(self):
        return self.studentprofile_set.filter(exam_result="PASSED").count()
    
    def get_total_students_failed_exam(self):
        return self.studentprofile_set.filter(exam_result="FAILED").count()


class Section(models.Model):
    section_text = models.CharField(max_length=10)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.section_text

    # Custom getter for section_text field
    @property
    def section_text(self):
        # Add any custom logic you need before returning the value
        return self._section_text.upper()  # For example, returning the section_text in uppercase

    # Custom setter for section_text field
    @section_text.setter
    def section_text(self, value):
        # Add any custom logic you need before setting the value
        self._section_text = value.lower()  # For example, storing the section_text in lowercase

    # Method to get the department of the section
    def get_department(self):
        return self.department
    
    # Setter method for department field
    def set_department(self, department):
        self.department = department
        self.save()  # Save the section with the new department


class ExitExamDate(models.Model):
    exam_date = models.DateField()

    def __str__(self):
        return "Exit Exam Date"
    
     # Getter method for exam_date field
    @property
    def get_exam_date(self):
        return self.exam_date

    # Setter method for exam_date field
    @get_exam_date.setter
    def set_exam_date(self, new_date):
        self.exam_date = new_date
        self.save()


class ExamRoom(models.Model):
    block = models.CharField(max_length=10, null=True, blank=True)
    room = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.room

    # Getter method for block field
    def get_block(self):
        return self.block

    # Setter method for block field
    def set_block(self, new_block):
        self.block = new_block
        self.save()

    # Getter method for room field
    def get_room(self):
        return self.room

    # Setter method for room field
    def set_room(self, new_room):
        self.room = new_room
        self.save()

class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    # Getter method for name field
    def get_name(self):
        return self.name

    # Setter method for name field
    def set_name(self, new_name):
        self.name = new_name
        self.save()

    # Getter method for description field
    def get_description(self):
        return self.description

    # Setter method for description field
    def set_description(self, new_description):
        self.description = new_description
        self.save()

    # Getter method for department field
    def get_department(self):
        return self.department

    # Setter method for department field
    def set_department(self, new_department):
        self.department = new_department
        self.save()

    def get_courses(self):
        return self.course_set.all()


class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True, help_text="Course Code")
    course_name = models.CharField(max_length=50, help_text="Course name")
    course_description = models.TextField(null=True, blank=True)
    instructor = models.ForeignKey("users.Instructor", on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ManyToManyField("Department")
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.course_name
    
    # Getter method for course_code field
    def get_course_code(self):
        return self.course_code

    # Setter method for course_code field
    def set_course_code(self, new_code):
        self.course_code = new_code
        self.save()

    # Getter method for course_name field
    def get_course_name(self):
        return self.course_name

    # Setter method for course_name field
    def set_course_name(self, new_name):
        self.course_name = new_name
        self.save()

    # Getter method for course_description field
    def get_course_description(self):
        return self.course_description

    # Setter method for course_description field
    def set_course_description(self, new_description):
        self.course_description = new_description
        self.save()

    # Getter method for instructor field
    def get_instructor(self):
        return self.instructor

    # Setter method for instructor field
    def set_instructor(self, new_instructor):
        self.instructor = new_instructor
        self.save()

    # Getter method for department field
    def get_departments(self):
        return self.department.all()

    # Setter method for department field
    def set_departments(self, new_departments):
        self.department.set(new_departments)
        self.save()

    # Getter method for theme field
    def get_theme(self):
        return self.theme

    # Setter method for theme field
    def set_theme(self, new_theme):
        self.theme = new_theme
        self.save()




