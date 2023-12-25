# from django.shortcuts import render
# from django.http import HttpResponse
from django.db.models import Count
from apps.survey.models import Survey

import plotly.express as px

def plotly_alignment_and_satisfaction():
    # Generate data for how well users feel their academic specialization aligns with job responsibilities (replace this with your actual data)
    alignment_data = Survey.objects.values('q2', 'q6').annotate(count=Count('q2'))

    # Extract data for the horizontal bar chart
    categories = [entry['q2'] for entry in alignment_data]
    counts = [entry['count'] for entry in alignment_data]
    job_satisfaction_levels = [entry['q6'] for entry in alignment_data]

    # Create the horizontal bar chart
    fig = px.bar(
        x=counts,
        y=categories,
        orientation='h',
        color=job_satisfaction_levels,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Update the layout
    fig.update_layout(
        title='How well do you feel your academic specialization aligns with your job responsibilities?',
        xaxis_title='Number of Responses',
        yaxis_title='Alignment',
        legend_title='Job Satisfaction',
        font=dict(
            family='Arial',
            size=18,
            color='#7f7f7f'
        )
    )

    # Return the plotly figure as HTML
    return fig.to_html(full_html=False)


def chart_alignment_and_satisfaction():
    # Generate data for how well users feel their academic specialization aligns with job responsibilities (replace this with your actual data)
    alignment_data = Survey.objects.values('q2', 'q6').annotate(count=Count('q2'))

    # Extract data for the horizontal bar chart
    categories = [entry['q2'] for entry in alignment_data]
    counts = [entry['count'] for entry in alignment_data]
    job_satisfaction_levels = [entry['q6'] for entry in alignment_data]
    academic_specializations = ['Computer Science','Information Technology']
    # Create a dictionary to store the data for each academic specialization
    specialization_data = {}
    for category, count, specialization in zip(categories, counts, academic_specializations):
        if specialization not in specialization_data:
            specialization_data[specialization] = {}
        specialization_data[specialization][category] = count

    # Convert the dictionary to a list of tuples for easy plotting
    plot_data = []
    for specialization, data in specialization_data.items():
        for category, count in data.items():
            plot_data.append((specialization, category, count))

    categories = [entry[0] for entry in plot_data]
    # Create a stacked bar chart
    fig = px.bar(
        plot_data,
        x=categories,
        y=[entry[2] for entry in plot_data],
        color=[entry[0] for entry in plot_data],
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Update the layout
    fig.update_layout(
        title='How well do you feel your academic specialization aligns with your job responsibilities?',
        xaxis_title='Alignment',
        yaxis_title='Number of Responses',
        legend_title='Academic Specialization',
        font=dict(
            family='Arial',
            size=18,
            color='#7f7f7f'
        )
    )

    # Return the plotly figure as HTML
    return fig.to_html(full_html=False)


