from django.db import models
from django.utils import timezone

class Student(models.Model):
    """
        This class represents the student entity
    """
    st_name = models.CharField(max_length=50, default='')
    st_username = models.CharField(max_length=50, default='')
    st_password = models.CharField(max_length=100, default='')
    st_created_date = models.DateTimeField(("st_createdDate"), default=timezone.now)
    st_email = models.EmailField(max_length=254, blank=True)
    st_school_year = models.CharField(("st_scYear"), max_length=50, default='')
    st_phone = models.CharField(max_length=50, default='')

    class Meta:
        ordering = ('st_name',)

    def __str__(self):
        return self.st_name

class Classe(models.Model):
    """
        This class represents the classes in the school
    """
    cl_name = models.CharField(max_length=50, default='')
    cl_cycle = models.CharField(max_length=50, default='')
    cl_created_year = models.DateTimeField(("cl_year"), default=timezone.now)

    class Meta:
        ordering = ('cl_name',)

    def __str__(self):
        return self.cl_name

class Group(models.Model):
    """
        This class represents a group of students
    """
    gr_name = models.CharField(max_length=50, default='')
    gr_student_nbr = models.IntegerField()
    gr_validated = models.BooleanField()
    gr_created_date = models.DateTimeField(("gr_createdDate"), default=timezone.now)
    gr_school_year = models.CharField(("gr_scYear"), max_length=50, default='')
    gr_created_by = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        ordering = ('gr_name',)

    def __str__(self):
        return self.gr_name

class Professor(models.Model):
    """
        This class represents the professor entity at school
    """
    prof_name = models.CharField(max_length=50, default='')
    prof_username = models.CharField(max_length=50, default='')
    prof_password = models.CharField(max_length=50, default='')
    prof_created_date = models.DateTimeField(("prof_createdDate"), default=timezone.now)
    prof_email = models.EmailField(max_length=254, blank=True)
    prof_school_year = models.CharField(("prof_scYear"), max_length=50, default='')
    prof_phone = models.CharField(max_length=50, default='')

    class Meta:
        ordering = ('prof_name',)

    def __str__(self):
        return self.prof_name

class Project(models.Model):
    """
        This class represents the projet entity created by professor
    """
    pr_name = models.CharField(max_length=50, default='')
    pr_description = models.CharField(max_length=200, default='')
    pr_files = models.FileField(upload_to=None, max_length=100)
    pr_created_date = models.DateTimeField(("pr_createdDate"), default=timezone.now)
    pr_end_date = models.DateTimeField(("pr_endDate"), default=timezone.now)
    pr_list_classes_id = ""
    pr_prof_id = models.ForeignKey(Professor, verbose_name="pr_prof", on_delete=models.CASCADE)

    class Meta:
        ordering = ('pr_name',)

    def __str__(self):
        return self.pr_name

class Topic(models.Model):
    """
            
    """
    to_subject = models.CharField(max_length=50, default='')
    to_project_id = models.ForeignKey(Project, verbose_name="to_projectId", on_delete=models.CASCADE)
    to_group_id = models.ForeignKey(Group, verbose_name="to_groupId", on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('to_subject',)

    def __str__(self):
        return self.to_subject

class Student_class(models.Model):
    """
        This class represents the relationship between students and the class where they study
    """
    stc_student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    stc_class_id = models.ForeignKey(Classe, on_delete=models.CASCADE)
    stc_year = models.CharField(("stc_year"), max_length=50, default='')

    class Meta:
        ordering = ('stc_year',)

    def __str__(self):
        return self.stc_year

class Professor_class(models.Model):
    """
    """
    pc_prof_id = models.ForeignKey(Professor, on_delete=models.CASCADE)
    pc_class_id = models.ForeignKey(Classe, on_delete=models.CASCADE)
    pc_year = models.CharField(("pc_year"), max_length=50, default='')

    class Meta:
        ordering = ('pc_year',)

    def __str__(self):
        return self.pc_year

class Group_student(models.Model):
    """
    """
    gs_student_id = models.ForeignKey(Student, verbose_name="gs_studentId", on_delete=models.CASCADE)
    gs_group_id = models.ForeignKey(Group, verbose_name="gs_groupId", on_delete=models.CASCADE)
    gs_date = models.DateTimeField(("gs_createdDate"), default=timezone.now)
    
    class Meta:
        ordering = ('gs_date',)

    def __str__(self):
        return self.gs_date

class Group_project(models.Model):
    """
    """
    gp_project_id = models.ForeignKey(Project, verbose_name="gp_projectId", on_delete=models.CASCADE)
    gp_group_id = models.ForeignKey(Group, verbose_name="gp_groupId", on_delete=models.CASCADE)
    gp_date = models.DateTimeField(("gp_createdDate"), default=timezone.now)
    
    class Meta:
        ordering = ('gp_date',)

    def __str__(self):
        return self.gp_date
