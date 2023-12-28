from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from apps.acad.models import Course

# class Survey(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='surveys',
#         verbose_name='User',
#         default = 1
#     )
#     q1 = models.CharField(
#         max_length=100,
#         choices=[('IT', 'Information Technology'), ('CS', 'Computer Science')],
#         verbose_name='1. What was your academic specialization?',
#         default='IT'
#     )

#     q2 = models.CharField(
#         max_length=100,
#         choices=[
#             ('Completely Aligned', 'Completely Aligned'),
#             ('Mostly Aligned', 'Mostly Aligned'),
#             ('Somewhat Aligned', 'Somewhat Aligned'),
#             ('Not Aligned at All', 'Not Aligned at All'),
#         ],
#         verbose_name='2. To what extent do you feel your academic specialization aligns with your current job responsibilities?',
#         default='Completely Aligned'
#     )

#     q3 = models.CharField(
#         max_length=100,
#         choices=[
#             ('Very Well', 'Very Well'),
#             ('Well', 'Well'),
#             ('Neutral', 'Neutral'),
#             ('Poorly', 'Poorly'),
#             ('Not at All', 'Not at All'),
#         ],
#         verbose_name='3. How well did your academic specialization prepare you for your current role?',
#         default='Very Well'
#     )

#     q4 = models.BooleanField(
#         verbose_name='4. Have you pursued any additional certifications or training after graduation to enhance your skills for your current job?',
#         default=False
#     )

#     q5 = models.CharField(
#         max_length=100,
#         choices=[('Yes', 'Yes'), ('No', 'No'), ('Not Sure', 'Not Sure')],
#         verbose_name='5. In hindsight, do you think a different academic specialization might have better prepared you for your current career?',
#         default='No'
#     )

#     q6 = models.CharField(
#         max_length=100,
#         choices=[
#             ('Very Satisfied', 'Very Satisfied'),
#             ('Satisfied', 'Satisfied'),
#             ('Neutral', 'Neutral'),
#             ('Dissatisfied', 'Dissatisfied'),
#             ('Very Dissatisfied', 'Very Dissatisfied'),
#         ],
#         verbose_name='6. How satisfied are you with your current job in terms of alignment with your academic specialization and overall career growth?',
#         default='Satisfied'
#     )

#     q7 = models.CharField(
#         max_length=100,
#         choices=[
#             ('Software Development', 'Software Development'),
#             ('Data Analytics', 'Data Analytics'),
#             ('Design & UI', 'Design & UI'),
#             ('Product Management', 'Product Management'),
#             ('Testing and Quality Assurance', 'Testing and Quality Assurance'),
#             ('Security', 'Security'),
#         ],
#         verbose_name='7. What was the final field recommendation to you by our system?',
#         default='Software Development'
#     )
    
#     q8 = models.CharField(
#         max_length=100,
#         choices=[
#             ('Software Development', 'Software Development'),
#             ('Data Analytics', 'Data Analytics'),
#             ('Design & UI', 'Design & UI'),
#             ('Product Management', 'Product Management'),
#             ('Testing and Quality Assurance', 'Testing and Quality Assurance'),
#             ('Security', 'Security'),
#         ],
#         verbose_name='8. What field is your job currently aligned on?',
#         default='Software Development'
#     )

#     q9 = models.CharField(
#         max_length=100,
#         choices=[
#             ('Male', 'Male'),
#             ('Female', 'Female'),
#         ],
#         verbose_name='9. Sex:',
#         default='Male'
#     )

#     q10 = models.CharField(
#         max_length=100,
#         choices=[
#             ('Single', 'Single'),
#             ('Married', 'Married'),
#             ('Divorced', 'Divorced'),
#             ('Widowed', 'Widowed'),
#         ],
#         verbose_name='10. Civil Status:',
#         default='Single'
#     )

class Survey(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='surveys',
        verbose_name='User',
        default = 1
    )
 
    academic_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    
    specialization = models.CharField(
        max_length=255,
        verbose_name='1. What specialization did you graduate with?',
        #default='IT',
    )
    employed = models.BooleanField(
        default=False,
        verbose_name='2. Are you currently employed?',
    )
    current_job_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='3. If yes, what is your current job title',
    )

    # Recommendation System Impact
    received_recommendation = models.BooleanField(
        default=False,
        verbose_name='4. In your 4th year, did you receive a recommended specialization from the system?',
    )

    confidence_rating = models.CharField(
        max_length=255,
        choices=[
            ('Very confident', 'Very confident'),
            ('Moderately confident', 'Moderately confident'),
            ('Somewhat confident', 'Somewhat confident'),
            ('Not confident at all', 'Not confident at all'),
        ],
        blank=True,
        verbose_name="5. If yes, how confident were you about the recommended specialization at the time?"
    )

    recommendation_influence = models.CharField(
        max_length=255,
        choices=[
            ('Significantly', 'Significantly'),
            ('Moderately', 'Moderately'),
            ('Slightly', 'Slightly'),
            ('Not at all', 'Not at all'),
        ],
        blank=True,
        verbose_name="6. Did the recommended specialization influence your decision to choose your current field of study?",
    )

    recommendation_influence_reason = models.TextField(
        blank=True,
        verbose_name="7. Why or why not did the recommended specialization influence your decision?",
    )

    system_information_helpfulness = models.CharField(
        max_length=255,
        choices=[
            ('Very helpful', 'Very helpful'),
            ('Moderately helpful', 'Moderately helpful'),
            ('Somewhat helpful', 'Somewhat helpful'),
            ('Not helpful at all', 'Not helpful at all'),
        ],
        blank=True,
        verbose_name="8. How helpful was the information provided by the recommendation system in understanding your potential career paths?",
    )

    recommendation_system_improvements = models.TextField(
        blank=True,
        verbose_name="9. Please share any specific improvements you suggest for the recommendation system."
    )

    # Career Alignment
    job_alignment = models.CharField(
        max_length=255,
        choices=[
            ('Very aligned', 'Very aligned'),
            ('Moderately aligned', 'Moderately aligned'),
            ('Somewhat aligned', 'Somewhat aligned'),
            ('Not at all aligned', 'Not at all aligned'),
        ],
        blank=True,
        verbose_name="10. Do you consider your current job aligned with the recommended specialization?", 
    )

    job_misalignment_reason = models.TextField(
        blank=True,
        verbose_name="11. If your current job is not aligned with the recommended specialization, why not?"
    )

    job_satisfaction = models.CharField(
        max_length=255,
        choices=[
            ('Very satisfied', 'Very satisfied'),
            ('Satisfied', 'Satisfied'),
            ('Neutral', 'Neutral'),
            ('Dissatisfied', 'Dissatisfied'),
            ('Very dissatisfied', 'Very dissatisfied'),
        ],
        blank=True,
        verbose_name="12. How satisfied are you with your current job overall?",
    )
    study_preparation = models.CharField(
        max_length=255,
        choices=[
            ('Very well', 'Very well'),
            ('Moderately', 'Moderately'),
            ('Somewhat', 'Somewhat'),
            ('Not well at all', 'Not well at all'),
        ],
        blank=True,
        verbose_name="13. How well do your skills and knowledge acquired during your studies prepare you for your current job?",
    )

    # Learning Materials Utilization
    explored_learning_materials = models.BooleanField(
        default=False,
        verbose_name="14. Did you explore any of the recommended learning materials (courses, articles, etc.) provided by the system?"
        )
    # most_helpful_materials = models.CharField(
    #     max_length=255,
    #     choices=[
    #         ('Courses', 'Courses'),
    #         ('Articles', 'Articles'),
    #         ('Videos', 'Videos'),
    #         ('Other', 'Other'),
    #     ],
    #     blank=True,
    # )
    material_satisfaction = models.CharField(
        max_length=255,
        choices=[
            ('Very satisfied', 'Very satisfied'),
            ('Moderately satisfied', 'Moderately satisfied'),
            ('Somewhat satisfied', 'Somewhat satisfied'),
            ('Not satisfied at all', 'Not satisfied at all'),
        ],
        blank=True,
        verbose_name="15. How satisfied were you with the quality and relevance of the provided learning materials?",
    )
    material_skill_gain = models.CharField(
        max_length=255,
        choices=[
            ('Significantly', 'Significantly'),
            ('Moderately', 'Moderately'),
            ('Slightly', 'Slightly'),
            ('Not at all', 'Not at all'),
        ],
        blank=True,
        verbose_name="16. Did the learning materials provided by the system help you gain new skills or knowledge relevant to your chosen field?"
    )

    # Job Posting Engagement
    accessed_job_postings = models.BooleanField(
        default=False,
        verbose_name="17. Did you access any of the job postings recommended by the system?"
        )
    
    posting_job_understanding = models.CharField(
        max_length=255,
        choices=[
            ('Very helpful', 'Very helpful'),
            ('Moderately helpful', 'Moderately helpful'),
            ('Somewhat helpful', 'Somewhat helpful'),
            ('Not helpful at all', 'Not helpful at all'), 
            ],
        blank=True,
        verbose_name="18. If yes, how helpful were the job postings in understanding the types of jobs available in your field?"
        )
            
    posting_career_influence = models.CharField(
        max_length=255,
        choices=[
            ('Significantly', 'Significantly'),
            ('Moderately', 'Moderately'),
            ('Slightly', 'Slightly'),
            ('Not at all', 'Not at all'),
            ],
        blank=True,
        verbose_name="19. Did the job postings provided by the system influence your job search process or career goals?"
        )
    
    more_specialized_postings = models.BooleanField(
        default=False,
        verbose_name="20. Would you like to see more specialized job postings tailored to your specific skillset or interests?"
        )

    # Additional Feedback
    additional_feedback = models.TextField(
        blank=True,
        verbose_name="21. Please share any other thoughts or feedback you have about the specialization recommendation system or your career journey."
        )

    # Timestamp
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Graduate Survey from {self.specialization} ({self.timestamp})"

    class Meta:
        ordering = ['-timestamp']