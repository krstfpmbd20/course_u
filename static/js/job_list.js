$(document).ready(function () {
    // Handle clicks on job cards with data-job-id and data-field-id attributes
    $('.job-card[data-job-id][data-field-id]').click(function () {
        // Get the job ID and field ID from the data attributes
        var jobId = $(this).data('job-id');
        var fieldId = $(this).data('field-id');
        console.log('Job ID:', jobId);
        console.log('Field ID:', fieldId);
        // Update the URL dynamically
        if (fieldId) {
            window.location.href = `/job_list/field:${fieldId}/job:${jobId}/`;
        } else {
            window.location.href = `/job_list/job:${jobId}/`;
        }
    });
});


$(document).ready(function () {
    $('#job-field-select').change(function () {
        if (this.value) {
            window.location.href = '/job_list/field:' + this.value;
        }
    });
});