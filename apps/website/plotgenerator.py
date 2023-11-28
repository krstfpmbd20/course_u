import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# from django.shortcuts import render
# from django.http import HttpResponse
from io import BytesIO
import base64
from django.db.models import Count
from apps.survey.models import Survey


# Percentage of respondents who feel their academic specialization is completely aligned 
# with their current job responsibilities, by level of job satisfaction:
def generate_alignment_and_satisfaction():
    try:
        # Generate data for how well users feel their academic specialization aligns with job responsibilities (replace this with your actual data)
        alignment_data = Survey.objects.values('q2', 'q6').annotate(count=Count('q2'))

        # Extract data for the horizontal bar chart
        categories = [entry['q2'] for entry in alignment_data]
        counts = [entry['count'] for entry in alignment_data]
        job_satisfaction_levels = [entry['q6'] for entry in alignment_data]

        # Create a horizontal bar chart
        plt.barh(categories, counts, color='skyblue', label='Very Well')
        plt.xlabel('Count')
        plt.ylabel('Alignment Level')
        plt.title('Alignment of Academic Specialization with Job Responsibilities, by Job Satisfaction')

        # Add legend
        plt.legend(title='Job Satisfaction', bbox_to_anchor=(1, 1), loc='upper left')

        # Save the plot as an image in memory
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png', bbox_inches='tight')
        image_stream.seek(0)
        plt.close()

        # Encode the image to base64
        image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

        return image_base64
    except:
        return None

# Percentage of respondents who feel their academic specialization prepared 
# them very well for their current role, by academic specialization:
def generate_role_satisfaction_by_academic_specialization():
    # Generate data for satisfaction levels with academic specialization preparation (replace this with your actual data)
    satisfaction_data = Survey.objects.values('q3', 'q1').annotate(count=Count('q3'))

    # Extract data for the stacked bar chart
    categories = [entry['q3'] for entry in satisfaction_data]
    counts = [entry['count'] for entry in satisfaction_data]
    academic_specializations = [entry['q1'] for entry in satisfaction_data]

    satisfaction_levels = ['Very Well', 'Well', 'Neutral', 'Poorly', 'Not at All']

    # Create a stacked bar chart
    plt.bar(categories, counts, color='skyblue', label='Very Well')
    bottom = counts
    for level in satisfaction_levels[1:]:
        # Initialize level_counts with zeros
        level_counts = [0 for _ in categories]

        # Fill in the counts for the levels that exist in satisfaction_data
        for entry in satisfaction_data:
            if entry['q3'] == level:
                index = categories.index(entry['q3'])
                level_counts[index] = entry['count']

        plt.bar(categories, level_counts, color='lightblue', bottom=bottom, label=level)
        bottom = [b + l_count for b, l_count in zip(bottom, level_counts)]

    plt.xlabel('Satisfaction Level')
    plt.ylabel('Count')
    plt.title('Satisfaction Levels with Academic Specialization Preparation, by Academic Specialization')

    # Add legend
    plt.legend(title='Satisfaction Level', bbox_to_anchor=(1, 1), loc='upper left')

    # Save the plot as an image in memory
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', bbox_inches='tight')
    image_stream.seek(0)
    plt.close()

    # Encode the image to base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return image_base64


def generate_gender_distribution_plot():
    
    gender_distribution = Survey.objects.values('q9').annotate(count=Count('q9'))

    #bar chart
    categories = [entry['q9'] for entry in gender_distribution]
    counts = [entry['count'] for entry in gender_distribution]

    plt.bar(categories, counts)
    plt.xlabel('Gender')
    plt.ylabel('Count')
    plt.title('Distribution of Users by Gender')

    # Saving plot as an image in memory
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plt.close()

    # Encode the image to base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return image_base64
def generate_civil_status_distribution_plot():
    # Generate civil status distribution data (replace this with your actual data)
    civil_status_distribution = Survey.objects.values('q10').annotate(count=Count('q10'))

    # Create a bar chart
    categories = [entry['q10'] for entry in civil_status_distribution]
    counts = [entry['count'] for entry in civil_status_distribution]

    plt.bar(categories, counts)
    plt.xlabel('Civil Status')
    plt.ylabel('Count')
    plt.title('Distribution of Users by Civil Status')

    # Save the plot as an image in memory
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plt.close()

    # Encode the image to base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return image_base64

# Add similar functions for other plots (e.g., academic_specialization_distribution_plot, correlation_plot, etc.)
def generate_academic_specialization_distribution_plot():
    # Generate academic specialization distribution data (replace this with your actual data)
    academic_specialization_distribution = Survey.objects.values('q1').annotate(count=Count('q1'))

    # Extract data for the pie chart
    labels = [entry['q1'] for entry in academic_specialization_distribution]
    counts = [entry['count'] for entry in academic_specialization_distribution]

    # Create a pie chart
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Distribution of Academic Specializations')

    # Save the plot as an image in memory
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plt.close()

    # Encode the image to base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return image_base64

def generate_alignment_with_job_responsibilities_plot():
    # Generate data for how well users feel their academic specialization aligns with job responsibilities (replace this with your actual data)
    alignment_data = Survey.objects.values('q2').annotate(count=Count('q2'))

    # Extract data for the horizontal bar chart
    categories = [entry['q2'] for entry in alignment_data]
    counts = [entry['count'] for entry in alignment_data]

    # Create a horizontal bar chart
    plt.barh(categories, counts, color='skyblue')
    plt.xlabel('Count')
    plt.ylabel('Alignment Level')
    plt.title('Alignment of Academic Specialization with Job Responsibilities')

    # Save the plot as an image in memory
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plt.close()

    # Encode the image to base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return image_base64

def generate_satisfaction_levels_plot():
    # Generate data for satisfaction levels with academic specialization preparation (replace this with your actual data)
    satisfaction_data = Survey.objects.values('q3').annotate(count=Count('q3'))

    # Extract data for the stacked bar chart
    categories = [entry['q3'] for entry in satisfaction_data]
    counts = [entry['count'] for entry in satisfaction_data]

    satisfaction_levels = ['Very Well', 'Well', 'Neutral', 'Poorly', 'Not at All']

    # Create a stacked bar chart
    # plt.bar(categories, counts, color='skyblue', label='Very Well')
    # bottom = counts
    # for level in satisfaction_levels[1:]:
    #     level_counts = [entry['count'] for entry in satisfaction_data if entry['q3'] == level]
    #     plt.bar(categories, level_counts, color='lightblue', bottom=bottom, label=level)
    #     bottom = [b + l_count for b, l_count in zip(bottom, level_counts)]

    # Create a stacked bar chart
    plt.bar(categories, counts, color='skyblue', label='Very Well')
    bottom = counts
    for level in satisfaction_levels[1:]:
        # Initialize level_counts with zeros
        level_counts = [0 for _ in categories]

        # Fill in the counts for the levels that exist in satisfaction_data
        for entry in satisfaction_data:
            if entry['q3'] == level:
                index = categories.index(entry['q3'])
                level_counts[index] = entry['count']

        plt.bar(categories, level_counts, color='lightblue', bottom=bottom, label=level)
        bottom = [b + l_count for b, l_count in zip(bottom, level_counts)]

    plt.xlabel('Satisfaction Level')
    plt.ylabel('Count')
    plt.title('Satisfaction Levels with Academic Specialization Preparation')

    # Add legend
    plt.legend(title='Satisfaction Level', bbox_to_anchor=(1, 1), loc='upper left')

    # Save the plot as an image in memory
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', bbox_inches='tight')
    image_stream.seek(0)
    plt.close()

    # Encode the image to base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return image_base64
def generate_certifications_training_percentage_plot():
    # Generate data for the percentage of users who pursued additional certifications or training (replace this with your actual data)
    certifications_training_data = Survey.objects.values('q4').annotate(count=Count('q4'))

    # Extract data for the pie chart
    categories = [entry['q4'] for entry in certifications_training_data]
    counts = [entry['count'] for entry in certifications_training_data]

    # Create a pie chart
    plt.pie(counts, labels=categories, autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'lightcoral'])
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Percentage of Users Who Pursued Additional Certifications or Training')

    # Save the plot as an image in memory
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plt.close()

    # Encode the image to base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return image_base64

def generate_different_specialization_percentage_plot():
    # Generate data for the percentage of users who think a different academic specialization might have better prepared them (replace this with your actual data)
    different_specialization_data = Survey.objects.values('q5').annotate(count=Count('q5'))

    # Extract data for the pie chart
    categories = [entry['q5'] for entry in different_specialization_data]
    counts = [entry['count'] for entry in different_specialization_data]

    # Create a pie chart
    plt.pie(counts, labels=categories, autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightcoral', 'lightgreen'])
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Percentage of Users Thinking a Different Specialization Might Have Better Prepared Them')

    # Save the plot as an image in memory
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plt.close()

    # Encode the image to base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return image_base64
def generate_overall_satisfaction_plot():
    try:
        # Generate data for overall satisfaction levels with current jobs (replace this with your actual data)
        satisfaction_data = Survey.objects.values('q6').annotate(count=Count('q6'))

        # Extract data for the bar chart
        categories = [entry['q6'] for entry in satisfaction_data]
        counts = [entry['count'] for entry in satisfaction_data]

        # Create a bar chart
        plt.bar(categories, counts, color='lightblue')
        plt.xlabel('Satisfaction Level')
        plt.ylabel('Count')
        plt.title('Overall Satisfaction Levels with Current Jobs')

        # Save the plot as an image in memory
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png', bbox_inches='tight')
        image_stream.seek(0)
        plt.close()

        # Encode the image to base64
        image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
        return image_base64
    except:
            return None

def generate_job_fields_distribution_plot():
    try:
        # Generate data for the distribution of users across different job fields (replace this with your actual data)
        job_fields_data = Survey.objects.values('q7', 'q8').annotate(count=Count('q7'))

        # Extract data for the grouped bar chart
        categories = list(set(entry['q7'] for entry in job_fields_data))
        job_fields = list(set(entry['q8'] for entry in job_fields_data))
        counts = {category: [entry['count'] for entry in job_fields_data if entry['q7'] == category] for category in categories}

        # Create a grouped bar chart
        bar_width = 0.35
        fig, ax = plt.subplots()
        for i, (category, count_list) in enumerate(counts.items()):
            positions = [x + i * bar_width for x in range(len(job_fields))]
            ax.bar(positions, count_list, bar_width, label=category)

        ax.set_xlabel('Job Fields')
        ax.set_ylabel('Count')
        ax.set_title('Distribution of Users Across Different Job Fields')
        ax.set_xticks([x + bar_width for x in range(len(job_fields))])
        ax.set_xticklabels(job_fields)
        ax.legend()

        # Save the plot as an image in memory
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png', bbox_inches='tight')
        image_stream.seek(0)
        plt.close()

        # Encode the image to base64
        image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
        return image_base64
    except:
        return None

def generate_user_engagement_plot():
    # Generate data for the number of surveys completed by each user (replace this with your actual data)
    user_engagement_data = Survey.objects.values('user').annotate(count=Count('user'))

    # Extract data for the bar chart
    users = [entry['user'] for entry in user_engagement_data]
    counts = [entry['count'] for entry in user_engagement_data]

    # Create a bar chart
    plt.bar(users, counts, color='lightblue')
    plt.xlabel('User ID')
    plt.ylabel('Number of Surveys Completed')
    plt.title('User Engagement: Number of Surveys Completed by Each User')

    # Save the plot as an image in memory
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', bbox_inches='tight')
    image_stream.seek(0)
    plt.close()

    # Encode the image to base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return image_base64



