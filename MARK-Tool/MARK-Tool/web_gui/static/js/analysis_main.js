window.addEventListener("load", function () {
    // Add the listener to the start_analysis_button
    const start_analysis_button = document.getElementById("start_analysis_btn")
    start_analysis_button.addEventListener("click", async function () {
        start_analysis_button.disabled = true
        document.body.style.cursor = "wait"
        let input_field = document.getElementById("input_field");
        let output_field = document.getElementById("output_field");
        let repo_field = document.getElementById("repo_field");
        try {
            let jsonResp = await requestValidateInputFolder(input_field.value)
            console.log(JSON.stringify(jsonResp))
            jsonResp = await requestValidateOutputFolder(output_field.value)
            console.log(JSON.stringify(jsonResp))
            jsonResp = await requestValidateCSV(repo_field.value)
            console.log(JSON.stringify(jsonResp))
        } catch (error) {
            window.alert(error);
        } finally {
            document.body.style.cursor = "default"
            start_analysis_button.disabled = false
        }
    })
})