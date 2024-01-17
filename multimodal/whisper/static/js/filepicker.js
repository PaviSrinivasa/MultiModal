
let fileHandle;
let sel = document.getElementById("a")
//sel.onclick = selectOption;
var myVar = document.getElementById("myVar").value;
let opt

function selectOption(){
    opt = sel.options[sel.selectedIndex].text;
    console.log(`$opt`);
}

/*document.querySelector(".read-dir").onclick = async () => {
  dirHandle = await window.showDirectoryPicker();
  console.log(dirHandle);
};*/

document.querySelector(".pick-file").onclick = async () => {
 [fileHandle] = await window.showOpenFilePicker({ startIn: myVar });
 const file = await fileHandle.getFile();
 alert("Name file : " + file.name);
 alert("Type file : " + file.type);
 alert("Size file : " + file.size);
 alert("Timestamp file : " + file.lastModifiedDate);
 alert(content);
 return content;
};





/*let fileHandle;
let dirHandle;

document.querySelector(".read-dir").onclick = async () => {
  dirHandle = await window.showDirectoryPicker();
  console.log(dirHandle);
};

document.querySelector(".pick-file").onclick = async () => {
 [fileHandle] = await window.showOpenFilePicker({ startIn: dirHandle });

 const file = await fileHandle.getFile();
 alert("Name file : " + file.name);
 alert("Type file : " + file.type);
 alert("Size file : " + file.size);
 alert("Timestamp file : " + file.lastModifiedDate);
 //console.log(content);
 alert(content);
 return content;
};*/

