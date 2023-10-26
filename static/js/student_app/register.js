function submitForm() {
	var studentID = document.getElementById("ID").value;
    var parsedID = parseInt(studentID);

    if (Number.isInteger(parsedID) == false || studentID.length != 8) {
        Swal.fire({
            title: "Error !",
            text: "กรุณากรอกรหัสนักศึกษาให้ถูกต้อง",
            icon: "error",
            confirmButtonText: "OK",
        });
        document.getElementById("ID").value = "";
        return false;
    } 
    return true;
}
