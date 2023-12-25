from django.shortcuts import render, redirect
from django.shortcuts import redirect


from apps.acad.models import Course, Subject, Curriculum, StudentProfile, StudentGrades
from apps.acad.forms import StudentGradeForm
from django.contrib.auth.models import User
from apps.website.models import Skill
from apps.recommender.models import UserSkill

from django.http import HttpResponse

def year_level_lable(year):
    if year == 1:
        return "First Year"
    elif year == 2:
        return "Second Year"
    elif year == 3:
        return "Third Year"
    elif year == 4:
        return "Fourth Year"
    else:
        return "Graduate"

def select_course(request):

    courses = Course.objects.all()
    print("Courses: ", courses)
    # return warning if ther are no courses
    return render(request, 'acad/select_course.html', {'courses': courses})

def student_information(request):
    # check if student  have student profile
    student_profile = StudentProfile.objects.filter(user=request.user).first()
    if not student_profile:
        # redirect to success page
        return redirect('select_course')

    course = Course.objects.get(pk=student_profile.enrolled_courses_id).course_name
    year_level = year_level_lable(student_profile.current_year)
    print('year level: ', year_level)

    if year_level != "Graduate":
        print("Student enrolled in course: ", student_profile.enrolled_courses_id," student current year: ", student_profile.current_year,"redirecting to subject grade input" )
        # check if student has grades in this year level
        subject = Curriculum.objects.filter(course_id=student_profile.enrolled_courses_id, year=student_profile.current_year).first()
        subject_grade = StudentGrades.objects.filter(student_id=student_profile.id, subject_id=subject.subject_id).exists()
        print("Subject grade: ", subject_grade)
        if not subject_grade:
            print("No subject grade found for this year level: ", student_profile.current_year)
            # if user haven't input their grades
            return redirect('subjects_grade_input')


    return render(request, 'acad/student_information.html', {
        'student_profile': student_profile,
        'course': course,
        'year_level': year_level,
        })
    
def student_grades(request, year):
    # check if student  have student profile
    student_profile = StudentProfile.objects.filter(user=request.user).first()
    if not student_profile:
        # redirect to success page
        return HttpResponse("No student profile found")

    course = Course.objects.get(pk=student_profile.enrolled_courses_id).course_name
    year_level = year_level_lable(year)
    
    student_subject_grades = User.objects.raw("""
    SELECT acad_subject.id, acad_subject.subject_name, acad_studentgrades.grade, acad_studentgrades.subject_id
    FROM acad_studentgrades
    INNER JOIN acad_subject
    ON acad_studentgrades.subject_id = acad_subject.id
    WHERE acad_studentgrades.student_id = %s
    AND acad_studentgrades.subject_id IN (
        SELECT acad_curriculum.subject_id
        FROM acad_curriculum
        WHERE acad_curriculum.course_id = %s
        AND acad_curriculum.year = %s
    )
    """, [student_profile.id, student_profile.enrolled_courses_id, year])
    
    # print subject and grade
    for grade in student_subject_grades:
        print("Subject: ", grade.subject_name, " Grade: ", grade.grade)


    return render(request, 'acad/student_grades.html', {
        'student_profile': student_profile,
        'course': course,
        'year_level': year_level,
        'subjects': student_subject_grades,
        })



def select_year(request, course_id):
    course = Course.objects.get(pk=course_id)
    print("Selected course: ", course)
        
    # Get the number of years from the selected course
    number_of_years = course.number_of_years
    print("Number of years: ", number_of_years)

    return render(request, 'acad/select_year_level.html', {'course': course, 'number_of_years': number_of_years})

def enroll_student(request, course_id, year_level):
    course = Course.objects.get(pk=course_id)
    
    student, created = StudentProfile.objects.get_or_create(user=request.user)
    student.enrolled_courses_id = course.id
    student.current_year = year_level
    student.save()

    print("Student enrolled in course: ", student.enrolled_courses_id)

    return redirect('subjects_grade_input')


def subjects_grade_input(request):
    # Get the Student Profile
    student = StudentProfile.objects.get(user=request.user)

    # Get the enrolled course of the student and year level
    course = student.enrolled_courses_id
    course_name = Course.objects.get(pk=course)
    year_level = student.current_year
    print("year level:", year_level)

    if year_level == 0:
        # redirect to success page
        return redirect('success_page')
    else:
            
        # Get the curriculum for the course and year level
        curriculum = Curriculum.objects.filter(course_id=course, year=year_level)

        # Get subject_id from curriculum
        subject_id = []
        for subject in curriculum:
            subject_id.append(subject.subject_id)

        # Get the subjects for the curriculum
        subjects = Subject.objects.filter(pk__in=subject_id)


        print("Subjects: ", subjects)

        if request.method == 'POST':
            forms = [StudentGradeForm(request.POST, prefix=str(subject.id)) for subject in subjects]
            if all(form.is_valid() for form in forms):
                for form, subject in zip(forms, subjects):
                    grade_value = form.cleaned_data.get('grade')
                    if grade_value is not None:
                        grade, created = StudentGrades.objects.get_or_create(student=student, subject=subject)
                        grade.grade = grade_value
                        grade.save()
                    else:
                        print(f"Grade value for subject {subject.id} is None or 0")
                return redirect('success_page')
            else:
                # Handle errors or form validation errors
                for form in forms:
                    print(form.errors)
        else:
            forms = [StudentGradeForm(prefix=str(subject.id)) for subject in subjects]
        
        # return warning if there are no subjects available

        return render(request, 'acad/subject_grade_input.html', {'form_subject_pairs': zip(forms, subjects), 'course': course_name, 'year_level': year_level})
    


def success_page(request):
    # Get the Student Profile
    student = StudentProfile.objects.get(user=request.user)


    user_id = request.user.id

    # Get the enrolled course of the student and year
    course = student.enrolled_courses_id
    year_level = student.current_year
    course_name = Course.objects.get(pk=course).course_name
    
    if year_level == 0:
        year_level = "First Year"
        return render(request, 'acad/success_page.html', {
                #'student': student,
                'course': course_name,
                'year_level': year_level,
            })
    else:
        curriculum = Curriculum.objects.filter(course_id=course, year=year_level)

        corriculum_subjects = []
        for subject in curriculum:
            corriculum_subjects.append(subject.subject_id)
        
        grades = StudentGrades.objects.filter(student=student, subject_id__in=corriculum_subjects)

        # loop through grades and get the score and skills
        for grade in grades:
            # get skils from subject
            subject = Subject.objects.get(pk=grade.subject_id)
            #grade.skills = subject.skills 
            
            # get grade score
            print('grade: ', grade.grade)
            # loop through skills
            for skill in subject.skills.all():
                skill_id = skill.id
                print('skill: ', skill)
                # get or create UserSkill
                # make sure to get only one
                user_skill, created = UserSkill.objects.get_or_create(user_id=user_id, skill_id=skill_id)

                # update score
                level = 0
                if created:
                    print('created user skill: ', user_skill)
                    user_skill.level = level
                else:
                    print('existing user skill: ', user_skill)
                    level = user_skill.level
                if grade.grade == 1.00 or grade.grade == 1:
                    level += 5
                elif grade.grade == 1.25:
                    level += 4
                elif grade.grade == 1.50:
                    level += 3
                elif grade.grade == 1.75:
                    level += 2
                elif grade.grade == 2.00 or grade.grade == 2:
                    level += 1
                elif grade.grade >= 2.25 and grade.grade <= 3.00 or grade.grade >= 2.25 and grade.grade <= 3:
                    level += 1
                else:
                    level += 0
                user_skill.level = level
                user_skill.save()
                print("saved user skill: ", user_skill)
                # add skill source

        course_name = Course.objects.get(pk=course).course_name
        
        year_level = year_level_lable(year_level)
        
        return render(request, 'acad/success_page.html', {
            #'student': student,
            'course': course_name,
            'year_level': year_level,
        })

