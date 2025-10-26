export function createCsvTab(csv, filename) {
    const template = document.getElementById("csv-file-template")
    let csvFileNode = template.content.cloneNode(true)
    csvFileNode.querySelector('.csv-file-top-bar > p').textContent = filename
    csv.data.rows.forEach((row) => {
        const tableRow = document.createElement("tr")
        let innerHtmlString = ""
        row.forEach((v) => innerHtmlString += `<td>${v}</td>`)
        tableRow.innerHTML = innerHtmlString
        csvFileNode.querySelector('tbody').appendChild(tableRow)
    })
    return csvFileNode
}