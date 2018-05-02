from django.contrib import admin
from .models import Grocery

# Register your models here.
admin.site.register(Grocery)

"""
class Grocery(admin.ModelAdmin):
    '''Adds search functionality'''
    '''
    search_fields = [
        "title"
        ]
    '''

    def save_model(self, request, obj, form, change):
        super(Grocery, self).save_model(request, obj, form, change)

MODEL_ADMIN_DICT = {
    User:UserAdmin,
    moocadmin_models.Course:CourseAdmin,
    moocadmin_models.Task:TaskAdmin,
    moocadmin_models.Student:AdminStudent,
    moocadmin_models.StudentProfileInformation:AdminStudentInfo,
    moocadmin_models.StudentCourseTask:AdminStudentCourseTaskInfo,
    moocadmin_models.StudentCourseTracking:AdminTrackingInfo,
    moocadmin_models.InfoSession:InfoSession,
    moocadmin_models.StudentStories:StudentStoriesAdmin,
    moocadmin_models.CompletedTask:CompletedTaskAdmin,
    moocadmin_models.CourseSegment:CourseSegmentAdmin,
}

for _model in dir(moocadmin_models):
    exec('''
if isinstance(moocadmin_models.{0},type) and issubclass(moocadmin_models.{0},django_models.Model):
    if moocadmin_models.{0} in MODEL_ADMIN_DICT.keys():
        admin.site.register(moocadmin_models.{0},MODEL_ADMIN_DICT[moocadmin_models.{0}])
    else:
        admin.site.register(moocadmin_models.{0})
        '''.format(_model)
        )
"""