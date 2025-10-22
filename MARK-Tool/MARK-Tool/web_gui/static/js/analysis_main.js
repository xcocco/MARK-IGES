import * as AnalysisRequests from './analysis_requests.js';
import * as FileRequests from './file_requests.js';
import * as LoadingDialog from './loading-dialog-script.js';

window.addEventListener("load", function () {
    // Add the listener to the start_analysis_button
    const start_analysis_button = document.getElementById("start_analysis_btn")
    start_analysis_button.addEventListener("click", startAnalysisButtonClick)
})

async function startAnalysisButtonClick() {
    const start_analysis_button = document.getElementById("start_analysis_btn")
    start_analysis_button.disabled = true

    let input_field = document.getElementById("input_field");
    let output_field = document.getElementById("output_field");
    let repo_field = document.getElementById("repo_field");

    input_field.disabled = true
    output_field.disabled = true
    repo_field.disabled = true

    try {
        await validateInputFields(input_field, output_field, repo_field)
        LoadingDialog.showLoadingPopup()
        let jobId = await startAnalysis(input_field, output_field, repo_field)
        await pollJobStatus(jobId)
    } catch (e) {
        window.alert(e)
    } finally {
        start_analysis_button.disabled = false
        input_field.disabled = false
        output_field.disabled = false
        repo_field.disabled = false
    }
}

async function pollJobStatus(jobId) {
    let status
    try {
        status = await AnalysisRequests.requestStatus(jobId)
        if (status.job.status === 'completed') {
            LoadingDialog.setContentText(status.job.message)
            setTimeout(LoadingDialog.hideLoadingPopup, 1000)
            return
        }
        LoadingDialog.setContentText(status.job.message)
        setTimeout(() => pollJobStatus(jobId), 100)
    } catch (e) {
        LoadingDialog.hideLoadingSpinner()
        LoadingDialog.setContentText(status.job.message)
        LoadingDialog.showTopBar()

    }
}

async function validateInputFields(
    input_field,
    output_field,
    repo_field
) {
    let jsonResp = await FileRequests.requestValidateInputFolder(input_field.value)
    console.log(JSON.stringify(jsonResp))
    jsonResp = await FileRequests.requestValidateOutputFolder(output_field.value)
    console.log(JSON.stringify(jsonResp))
    jsonResp = await FileRequests.requestValidateCSV(repo_field.value)
    console.log(JSON.stringify(jsonResp))
}

async function startAnalysis(
    input_field,
    output_field,
    repo_field
) {
    let jsonResp = await AnalysisRequests.requestStart(
        input_field.value,
        output_field.value,
        repo_field.value
    )
    console.log(jsonResp)

    return jsonResp.job_id
}