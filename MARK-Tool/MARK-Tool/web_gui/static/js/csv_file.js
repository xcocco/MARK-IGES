import * as Tabs from './tabs.js'

export function createCsvTabContent(csv, filename) {
    const template = document.getElementById("csv-file-template")
    let csvFileNode = template.content.cloneNode(true)
    csvFileNode.querySelector('.csv-file-top-bar > p').textContent = filename
    csvFileNode.querySelector('.csv-file-top-bar > button').addEventListener('click', () => {
        Tabs.removeTab(filename)
    })
    csv.data.rows.forEach((row) => {
        const tableRow = document.createElement("tr")
        let innerHtmlString = ""
        row.forEach((v) => innerHtmlString += `<td>${v}</td>`)
        tableRow.innerHTML = innerHtmlString
        csvFileNode.querySelector('tbody').appendChild(tableRow)
    })
    return csvFileNode.firstElementChild
}