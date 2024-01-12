
import plotly.express as px
from django.db.models import Count
from apps.survey.models import Survey

import pandas as pd
import numpy as np

import plotly.io as py

from io import BytesIO


def tracer_dataframe():
    #survey = Survey.objects.all()
    survey = pd.DataFrame(list(Survey.objects.all().values()))
    return survey

# def print df columns
def print_df_columns(df):
    print("columns:", df.columns)

def to_html(fig):
    return fig.to_html(full_html=False)

def to_html_div(fig):
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

# def to_img(fig):
#     return fig.to_image(format="png")

# def to_img(fig):
#     # Save the plot as an image in memory
#     image_stream = BytesIO()
#     plt.savefig(image_stream, format='png', bbox_inches='tight')
#     image_stream.seek(0)
#     plt.close()

#     # Encode the image to base64
#     image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
#     return image_base64

def to_img(fig):
    #img_bytes = py.to_image(fig, format="png")
    image_buffer = BytesIO()
    fig.write_image(image_buffer, format="png")
    img_bytes = image_buffer.getvalue()
    return img_bytes

# -   **Bar Chart**: 
# Compare the percentage of graduates who felt confident about the recommended
# specialization at different confidence levels 
# (Not confident, Somewhat confident, etc.).
def fig_confidence_rating(df):
    # order by confidence_rating
    confidence_rating = "Not confident at all", "Somewhat confident", "Moderately confident", "Very confident"
    df['confidence_rating'] = pd.Categorical(df['confidence_rating'], categories=confidence_rating, ordered=True)
    df = df.sort_values('confidence_rating')
    #print('fig_confidence_rating:', df)
    #print("columns:", df.columns)
    # unique values of confidence_rating
    #print("unique values of confidence_rating:", df['confidence_rating'].unique())
    fig = px.bar(
        df,
        x="confidence_rating",
        #y="confidence_rating",
        color="confidence_rating",
        #color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig

def html_fig_confidence_rating(df):
    fig = fig_confidence_rating(df)
    return to_html(fig)

def table_confidence_rating(df):
    # order by confidence_rating
    confidence_rating = "Not confident at all", "Somewhat confident", "Moderately confident", "Very confident"
    df['confidence_rating'] = pd.Categorical(df['confidence_rating'], categories=confidence_rating, ordered=True)
    df = df.sort_values('confidence_rating')

    # count of each rating
    count = df['confidence_rating'].value_counts().sort_index()

    # percentage of each rating
    percentage = df['confidence_rating'].value_counts(normalize=True).sort_index() * 100

    # remove decimal place and add % sign
    percentage = percentage.round(0).astype(int).astype(str) + '%'

    # create a DataFrame
    table = pd.DataFrame({'Count': count, 'Percentage': percentage})

    # reset the index
    table.reset_index(inplace=True)

    # rename the index column
    table.rename(columns={'index': 'Confidence Rating'}, inplace=True)

    # add a last row
    total_count = table['Count'].sum()
    table.loc[len(table.index)] = ['Total', total_count, '100%']

    # convert the DataFrame to HTML
    table_html = table.to_html(index=False)
    # print(table_html)
    return table_html


# ***1. Recommendation Impact:***

# -   **Stacked Bar Chart**: Show how the recommended specialization influenced graduates'
# decisions to choose their current field (Not at all, Slightly, Moderately, Significantly) 
# across different specializations.
def fig_recommendation_influence(df):
    fig = px.bar(
        df,
        x="recommendation_influence",
        #y="confidence_rating",
        color="recommendation_influence",
        #color_discrete_sequence=px.colors.qualitative.Pastel
        barmode="stack",
    )
    return fig

def html_fig_recommendation_influence(df):
    fig = fig_recommendation_influence(df)
    return to_html(fig)

def table_recommendation_influence(df):
    # order by confidence_rating
    recommendation_influence = "Not at all", "Slightly", "Moderately", "Significantly"
    df['recommendation_influence'] = pd.Categorical(df['recommendation_influence'], categories=recommendation_influence, ordered=True)
    df = df.sort_values('recommendation_influence')

    # count of each rating
    count = df['recommendation_influence'].value_counts().sort_index()

    # percentage of each rating
    percentage = df['recommendation_influence'].value_counts(normalize=True).sort_index() * 100
    
    # remove decimal place and add % sign
    percentage = percentage.round(0).astype(int).astype(str) + '%'

    # create a DataFrame
    table = pd.DataFrame({'Count': count, 'Percentage': percentage})

    # reset the index
    table.reset_index(inplace=True)

    # rename the index column
    table.rename(columns={'index': 'Recommendation Influence'}, inplace=True)

    # add a last row
    total_count = table['Count'].sum()
    table.loc[len(table.index)] = ['Total', total_count, '100%']

    # convert the DataFrame to HTML
    table_html = table.to_html(index=False)
    return table_html


# displaying reasons of influence remakrs 
# def remakrs_recommendation_influence(df):
#     # get 'recommendation_influence_reason' column
#     df = df[['recommendation_influence', 'recommendation_influence_reason']]
#     # display 3 samples of 'recommendation_influence_reason' for each 'recommendation_influence' if it is not null
#     df = df.groupby('recommendation_influence').apply(lambda x: x.sample(3) if len(x) > 3 else x)
    
#     # empty html
#     remakrs_html = ''

#     # create their own dataframe by recommendation_influence as head and recommendation_influence_reason as rows
#     for recommendation_influence in df['recommendation_influence'].unique():
#         reco = df[df['recommendation_influence'] == recommendation_influence]
#         # make it to html
#         reco_html = reco.to_html(index=False)
#         # add to remakrs_html
#         remakrs_html += reco_html
    
#     return remakrs_html
def remakrs_recommendation_influence(df):
    # get 'recommendation_influence' and 'recommendation_influence_reason' columns and drop rows with null values
    df = df[['recommendation_influence', 'recommendation_influence_reason']].dropna()

    # remove rows where 'recommendation_influence_reason' is NA or NaN
    df = df.dropna(subset=['recommendation_influence_reason'])
    # drop recommendation_influence_reason = '' or ' '
    df = df[df['recommendation_influence_reason'] != '']
    df = df[df['recommendation_influence_reason'] != ' ']

    # get 3 samples of 'recommendation_influence_reason' for each 'recommendation_influence' if it is not null
    df = df.groupby('recommendation_influence').apply(lambda x: x.sample(3) if len(x) > 3 else x).reset_index(drop=True)

    # create their own dataframe by recommendation_influence as head and recommendation_influence_reason as rows
    remakrs_html = ''.join([f'<h3>{recommendation_influence}</h3>{df[df["recommendation_influence"] == recommendation_influence].drop(columns=["recommendation_influence"]).to_html(index=False, header=False)}' 
                            for recommendation_influence in df['recommendation_influence'].unique()])

    return remakrs_html


# -   **Word Cloud**: Analyze open-ended responses about why or why not the recommended 
# specialization influenced graduates' decisions. This can reveal common themes and motivations.
def fig_word_cloud(df):
    fig = None
    return fig

# ***2. Job Alignment and Satisfaction:***

# -   **Scatter Plot**: Visualize the relationship between job alignment (Not aligned, Somewhat aligned, etc.) 
# and overall career satisfaction (Very dissatisfied, Dissatisfied, etc.). Look for any trends or correlations.
def fig_alignment_and_satisfaction(df):
    fig = px.scatter(
        df,
        x="job_alignment",
        y="job_satisfaction",
        color="job_alignment",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig

def html_fig_alignment_and_satisfaction(df):
    fig = fig_alignment_and_satisfaction(df)
    return to_html(fig)


#  -   **Pie Chart**: Show the distribution of graduates across different job alignment categories.
def fig_job_alignment(df):
    fig = px.pie(
        df,
        names="job_alignment",
        color="job_alignment",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig

def html_fig_job_alignment(df):
    fig = fig_job_alignment(df)
    return to_html(fig)


def table_job_alignment(df):
    # order by confidence_rating
    job_alignment = "Not at all aligned", "Somewhat aligned", "Moderately aligned", "Significantly aligned"
    df['job_alignment'] = pd.Categorical(df['job_alignment'], categories=job_alignment, ordered=True)
    df = df.sort_values('job_alignment')

    # count of each rating
    count = df['job_alignment'].value_counts().sort_index()

    # percentage of each rating
    percentage = df['job_alignment'].value_counts(normalize=True).sort_index() * 100
    
    # remove decimal place and add % sign
    percentage = percentage.round(0).astype(int).astype(str) + '%'

    # create a DataFrame
    table = pd.DataFrame({'Count': count, 'Percentage': percentage})

    # reset the index
    table.reset_index(inplace=True)

    # rename the index column
    table.rename(columns={'index': 'Job Alignment'}, inplace=True)

    # add a last row
    total_count = table['Count'].sum()
    table.loc[len(table.index)] = ['Total', total_count, '100%']

    # convert the DataFrame to HTML
    table_html = table.to_html(index=False)
    return table_html


# **Bubble Chart**: Represent job alignment as the bubble size and career satisfaction as the color, 
# with each bubble representing a graduate. This can reveal connections between specific specializations 
# and alignment/satisfaction levels.

# ***3. Time-Series Analysis (if you have data from previous cohorts):***

# -   **Line Chart**: Track the evolution of graduates' confidence in the recommended specialization over time, comparing different cohorts.
#***Line Chart: Tracking Confidence in Recommendations:***
# **Timestamps**: You need a reference point for each data point, usually the graduates' year of graduation (e.g., 2023, 2024, 2025).
# **Cohort Groups**: Separate your data into different groups based on graduation years to observe trends within each cohort.
# **Confidence Rating**: For each graduate in each cohort, store their confidence level in the recommended specialization when they received it (e.g., Not confident, Somewhat confident, etc.). You can average confidence ratings within each cohort and year to create a smooth line.

def fig_confidence_rating_time_series(df):
    fig = px.line(
        df,
        x="timestamp",
        y="confidence_rating",
        color="confidence_rating",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig

def html_fig_confidence_rating_time_series(df):
    fig = fig_confidence_rating_time_series(df)
    return to_html(fig)



# -   **Bar Chart**: Compare the percentage of graduates whose current jobs align with their recommended specialization across different cohorts. This can indicate the long-term effectiveness of the system.
def fig_job_alignment_time_series(df):
    fig = px.bar(
        df,
        x="timestamp",
        y="job_alignment",
        color="job_alignment",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig

def html_fig_job_alignment_time_series(df):
    fig = fig_job_alignment_time_series(df)
    return to_html(fig)

# ***Bar Chart: Job Alignment across Cohorts:***
# **Graduation Cohorts**: Again, group your data based on graduation years.
# **Job Alignment**: For each graduate within a cohort, track whether their current job aligns with their recommended specialization (e.g., Yes/No, Aligned/Not Aligned).
# **Cohort Size**: Calculate the total number of graduates within each cohort for accurate comparison.

def fig_job_alignment_across_cohorts(df):
     # on job_alignment if "Not at all aligned" = 0, "Somewhat aligned" = 1, "Moderately aligned" = 2, "Significantly aligned" = 3
    df['job_alignment'] = df['job_alignment'].replace(['Not at all aligned'], "No")
    df['job_alignment'] = df['job_alignment'].replace(['Somewhat aligned'], "Yes")
    df['job_alignment'] = df['job_alignment'].replace(['Moderately aligned'], "Yes")
    df['job_alignment'] = df['job_alignment'].replace(['Significantly aligned'], "Yes")
   

    # group by graduation year/timestamp(year)
    # convert timestamp to year
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['timestamp'] = df['timestamp'].dt.year

    # group by timestamp
    df = df.groupby('timestamp').count()
   
    #print('fig_job_alignment_across_cohorts:', df)
    
    fig = px.bar(
        df,
        #x="timestamp",
        y="job_alignment",
        # color="job_alignment",
        #color_discrete_sequence=px.colors.qualitative.Pastel
        # barmode="stack",
    )
    return fig

def html_fig_job_alignment_across_cohorts(df):
    fig = fig_job_alignment_across_cohorts(df)
    return to_html(fig)




# ***Data Visualization Ideas:***

# **Stacked Bar Chart**: Show the utilization of different learning materials (courses, articles, videos) by graduates.

# **Scatter Plot**: Analyze the relationship between graduates' satisfaction with learning materials and the perceived improvement in skills/knowledge.

# **Line Graph**: Track the trend of job posting engagement (accessed/not accessed) across different graduating cohorts.

# **Circle Chart**: Represent the percentage of graduates whose job search or career goals were influenced by the recommended job postings.


def remakrs_additional_feedback(df):
    df = df[['additional_feedback']].dropna()

    # get 10 samples of 'additional_feedback' if it is not null/na/''/' 
    df = df.groupby('additional_feedback').apply(lambda x: x.sample(10) if len(x) > 10 else x).reset_index(drop=True)

    # make p tag for each additional_feedback
    remakrs_html = ''.join([f'<p>{additional_feedback}</p>' 
                            for additional_feedback in df['additional_feedback'].unique()])
    return remakrs_html


# general

def general_report():

    #survey = Survey.objects.all()
    survey = tracer_dataframe()

    # figure, html 
    return {
        html_fig_confidence_rating(survey),
        html_fig_recommendation_influence(survey),
        html_fig_alignment_and_satisfaction(survey),
        html_fig_job_alignment(survey),
        html_fig_confidence_rating_time_series(survey),
    }