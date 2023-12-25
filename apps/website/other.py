
def extract_relevant_data(survey_responses):
    # Extract relevant fields from survey responses
    extracted_data = []
    for survey_response in survey_responses:
        #student_name = survey_response.student.name
        #job_title = survey_response.job_title
        #satisfaction = survey_response.satisfaction

        #1.	What was your academic specialization in Information Technology or Computer Science during your undergraduate studies?
        course = survey_response.q1     # IT or CS
        #2.	To what extent do you feel that your academic specialization aligns with your current job responsibilities?
        alignment = survey_response.q2  #  Completely Aligned, Mostly Aligned, Somewhat Aligned, Not Aligned at All
        #3.	How well did your academic specialization prepare you for the specific tasks and challenges you face in your current role?
        preparation = survey_response.q3 # very well, well, neutral, poorly, not at all
        #4.	Have you pursued any additional certifications or training after graduation to enhance your skills for your current job?
        additional_sup = survey_response.q4 # 1 (yes) 0 (no)
        #5.	In hindsight, do you think a different academic specialization might have better prepared you for your current career?
        better_preparation = survey_response.q5 # yes no 
        #6.	How satisfied are you with your current job in terms of alignment with your academic specialization and overall career growth?
        satisfaction = survey_response.q6 # # very satisfied, satisfied, neutral, dissatisfied, very dissatisfied

        extracted_data.append({
            #'student_name': student_name,
            #'job_title': job_title,
            #'satisfaction': satisfaction
            'course': course,
            'alignment': alignment,
            'preparation': preparation,
            'additional_sup': additional_sup,
            'better_preparation': better_preparation,
            'satisfaction': satisfaction
        })

    return extracted_data
def analyze_preparation_by_course(extracted_data):
    it_preparation_counts = {}
    cs_preparation_counts = {}
    for data_item in extracted_data:
        course = data_item['course']
        preparation_level = data_item['preparation']

        if course == 'IT':
            if preparation_level not in it_preparation_counts:
                it_preparation_counts[preparation_level] = 0
            it_preparation_counts[preparation_level] += 1

        elif course == 'CS':
            if preparation_level not in cs_preparation_counts:
                cs_preparation_counts[preparation_level] = 0
            cs_preparation_counts[preparation_level] += 1

    preparation_levels_by_course = {
        'IT': it_preparation_counts,
        'CS': cs_preparation_counts
    }

    return preparation_levels_by_course

def calculate_alignment_percentages(extracted_data):
    alignment_counts = {}
    for data_item in extracted_data:
        alignment_level = data_item['alignment']
        if alignment_level not in alignment_counts:
            alignment_counts[alignment_level] = 0
        alignment_counts[alignment_level] += 1

    alignment_percentages = {}
    for alignment_level, count in alignment_counts.items():
        alignment_percentages[alignment_level] = round(count / len(extracted_data) * 100, 2)

    return alignment_percentages
def analyze_additional_certifications(extracted_data):
    additional_certifications_counts = {}
    for data_item in extracted_data:
        additional_certifications = data_item['additional_sup']
        if additional_certifications not in additional_certifications_counts:
            additional_certifications_counts[additional_certifications] = 0
        additional_certifications_counts[additional_certifications] += 1

    additional_certifications_data = {
        'yes': additional_certifications_counts[1],
        'no': additional_certifications_counts[0]
    }

    return additional_certifications_data
def analyze_better_preparation(extracted_data):
    better_preparation_counts = {}
    for data_item in extracted_data:
        better_preparation = data_item['better_preparation']
        if better_preparation not in better_preparation_counts:
            better_preparation_counts[better_preparation] = 0
        better_preparation_counts[better_preparation] += 1

    better_preparation_data = {
        'yes': better_preparation_counts['Yes'],
        'no': better_preparation_counts['No'],
        'not_sure': better_preparation_counts['Not Sure']
    }

    return better_preparation_data

def analyze_overall_satisfaction(extracted_data):
    satisfaction_counts = {}
    for data_item in extracted_data:
        satisfaction_level = data_item['satisfaction']
        if satisfaction_level not in satisfaction_counts:
            satisfaction_counts[satisfaction_level] = 0
        satisfaction_counts[satisfaction_level] += 1

    overall_satisfaction_percentages = {}
    for satisfaction_level, count in satisfaction_counts.items():
        percentage = round(count / len(extracted_data) * 100, 2)
        overall_satisfaction_percentages[satisfaction_level] = percentage

    return overall_satisfaction_percentages
def analyze_data(extracted_data):
    # Perform data analysis
    alignment_percentages = calculate_alignment_percentages(extracted_data)
    preparation_levels_by_course = analyze_preparation_by_course(extracted_data)
    additional_certifications_data = analyze_additional_certifications(extracted_data)
    better_preparation_data = analyze_better_preparation(extracted_data)
    overall_satisfaction_percentages = analyze_overall_satisfaction(extracted_data)

    # Prepare data for HTML template
    alignment_data = {
        'title': 'Alignment with Academic Specialization',
        'labels': alignment_percentages.keys(),
        'data': alignment_percentages.values()
    }

    preparation_data = {
        'title': 'Preparation Levels by Course',
        'courses': ['IT', 'CS'],
        'preparation_levels': ['Very Well', 'Well', 'Neutral', 'Poorly', 'Not at All'],
        'data': preparation_levels_by_course
    }

    additional_certifications = {
        'title': 'Additional Certifications',
        'labels': ['Yes', 'No'],
        'data': additional_certifications_data
    }

    better_preparation = {
        'title': 'Satisfaction with Better Preparation',
        'labels': ['Yes', 'No', 'Not Sure'],
        'data': better_preparation_data
    }

    overall_satisfaction = {
        'title': 'Overall Satisfaction',
        'labels': overall_satisfaction_percentages.keys(),
        'data': overall_satisfaction_percentages.values()
    }

    # Return analyzed data for use in HTML template
    return {
        'alignment_data': alignment_data,
        'preparation_data': preparation_data,
        'additional_certifications': additional_certifications,
        'better_preparation': better_preparation,
        'overall_satisfaction': overall_satisfaction
    }
def process_survey_data(survey_responses):
    # Extract relevant data from survey responses
    # This may involve filtering, aggregating, or transforming data
    extracted_data = extract_relevant_data(survey_responses)

    # Calculate statistics or generate visualizations
    # This may involve using data analysis libraries or charting tools
    processed_data = analyze_data(extracted_data)

    return processed_data
