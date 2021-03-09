/*Var doc all document*/
function setDoc(left, doc){
    doc.styles.tableHeader.fontSize = 9;					
    doc.styles.tableHeader.bold = true;
    doc.styles.tableHeader.color = 'white';
    doc.styles.tableHeader.fillColor = '#e74a3b';
    doc.styles.tableHeader.alignment = 'center';
    doc.styles.title.alignment = 'center';
    doc.styles.title.fontSize = '12';
    doc.defaultStyle.fontSize = '9';
    doc.defaultStyle.alignment = ''
    doc.styles.tableBodyEven.fillColor = '';
    doc.styles.tableBodyOdd.fillColor ='#E8E8E8';
    doc.content[1].margin = [left, 0, 5, 0] //left, top, right, bottom
}