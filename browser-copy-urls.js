// https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx?year=-1&sid=dcabe0e4-ca85-4f1d-bcb3-79ec47df5010&rtid=7
// TODO better to go row-by-row and note which year we are on
// could store as a JSON structure like [{"year": "2023", "urls": [...]},{...}]
let urls = new Set()
document.querySelectorAll('#contentPlaceHolder_tblResult a[href]').forEach(el => {
    if (el.href) urls.add(el.href)
})
copy(Array.from(urls).sort().join('\n'))
