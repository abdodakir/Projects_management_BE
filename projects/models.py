from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Users(models.Model):
    """
        This class represents the User entity (Student or Professor), he extends Django User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    p_phone = models.CharField(max_length=50, default='')
    p_type = models.CharField(max_length=50, default='student')
    p_city = models.CharField(max_length=50, default='')
    p_country = models.CharField(max_length=10, default='')
    p_gender = models.CharField(max_length=10, default='')
    p_zip = models.CharField(max_length=10, default='')

    def create_user(self, **kwargs):
        self.p_phone = kwargs["p_phone"] if "p_phone" in kwargs else "" 
        self.p_type = kwargs["p_type"] if "p_type" in kwargs else "student"
        self.p_city = kwargs["p_city"] if "p_city" in kwargs else ""
        self.p_country = kwargs["p_country"] if "p_country" in kwargs else ""
        self.p_gender = kwargs["p_gender"] if "p_gender" in kwargs else "Male"
        self.p_zip = kwargs["p_zip"] if "p_zip" in kwargs else ""
        self.save()
        return self

    def __unicode__(self):
        return self.user.first_name
    
class Classe(models.Model):
    """
        This class represents the classes in the school
    """
    cl_name = models.CharField(max_length=50, default='')
    cl_cycle = models.CharField(max_length=50, default='')
    cl_created_year = models.DateTimeField(("cl_year"), default=timezone.now)

    def create_classe(self, **kwargs):
        self.cl_name = kwargs["cl_name"] if "cl_name" in kwargs else "" 
        self.cl_cycle = kwargs["cl_cycle"] if "cl_cycle" in kwargs else ""
        self.cl_created_year = kwargs["cl_created_year"] if "cl_created_year" in kwargs else ""
        self.save()
        return self

    class Meta:
        ordering = ('cl_name',)

    def __unicode__(self):
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
    gr_created_by = models.ForeignKey(Users, on_delete=models.CASCADE)

    def create_groupe(self, **kwargs):
        self.gr_name = kwargs["gr_name"] if "gr_name" in kwargs else "" 
        self.gr_student_nbr = kwargs["gr_student_nbr"] if "gr_student_nbr" in kwargs else 2
        self.gr_validated = kwargs["gr_validated"]
        self.gr_created_date = kwargs["gr_created_date"]
        self.gr_school_year = kwargs["gr_school_year"] if "gr_school_year" in kwargs else ""
        self.save()
        return self
    
    def to_dict(self):
        data = {
            "id": self.id,
            "gr_name": self.gr_name,
            "gr_student_nbr": self.gr_student_nbr,
            "gr_validated": self.gr_validated,
            "gr_created_date": self.gr_created_date,
            "gr_school_year": self.gr_school_year
        }
        return data

    def __unicode__(self):
        return self.id

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
    pr_prof_id = models.ForeignKey(Users, verbose_name="pr_prof_id", on_delete=models.CASCADE)

    def create_project(self, **kwargs):
        self.pr_name = kwargs["pr_name"]
        self.pr_description = kwargs["pr_description"]
        self.pr_files = kwargs["pr_files"]
        self.pr_created_date = kwargs["pr_created_date"]
        self.pr_end_date = kwargs["pr_end_date"]
        self.pr_list_classes_id = kwargs["pr_list_classes_id"]
        self.pr_prof_id = kwargs["pr_prof_id"]
        
    def get_projet(self, *args, **kwargs):
        pass

    def update_projet(self, *args, **kwargs):
        pass

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
    
    def create_topic(self, **kwargs):
        self.to_subject = kwargs["pr_name"]
        self.to_group_id = kwargs["pr_description"]
        self.to_group_id = kwargs["pr_files"]
        
    class Meta:
        ordering = ('to_subject',)

    def __str__(self):
        return self.to_subject

class Student_class(models.Model):
    """
        This class represents the relationship between students and the class where they study
    """
    stc_student_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    stc_class_id = models.ForeignKey(Classe, on_delete=models.CASCADE)
    stc_year = models.CharField(("stc_year"), max_length=50, default='')

    def create_SC(self, **kwargs):
        self.stc_student_id = kwargs["stc_student_id"]
        self.stc_class_id = kwargs["stc_class_id"]
        self.stc_year = kwargs["stc_year"]
        
    class Meta:
        ordering = ('stc_year',)

    def __str__(self):
        return self.stc_year

class Professor_class(models.Model):
    """
    """
    pc_prof_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    pc_class_id = models.ForeignKey(Classe, on_delete=models.CASCADE)
    pc_year = models.CharField(("pc_year"), max_length=50, default='')

    def create_PC(self, *args, **kwargs):
        self.pc_prof_id = kwargs["pc_prof_id"]
        self.pc_class_id = kwargs["pc_class_id"]
        self.pc_year = kwargs["pc_year"]
        
    class Meta:
        ordering = ('pc_year',)

    def __str__(self):
        return self.pc_year

class Group_student(models.Model):
    """
    """
    gs_student_id = models.ForeignKey(Users, verbose_name="gs_studentId", on_delete=models.CASCADE)
    gs_group_id = models.ForeignKey(Group, verbose_name="gs_groupId", on_delete=models.CASCADE)
    gs_date = models.DateTimeField(("gs_createdDate"), default=timezone.now)
    
    def create_GS(self, *args, **kwargs):
        self.gs_student_id = kwargs["gs_student_id"]
        self.gs_group_id = kwargs["gs_group_id"]
        self.gs_date = kwargs["gs_date"]
        
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
    
    def create_GP(self, *args, **kwargs):
        self.gp_project_id = kwargs["gp_project_id"]
        self.gp_group_id = kwargs["gp_group_id"]
        self.gp_date = kwargs["gp_date"]
    
    class Meta:
        ordering = ('gp_date',)

    def __str__(self):
        return self.gp_date
