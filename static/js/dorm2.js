const roomSearch = () => {
    const input = document.getElementById("finder");
    const filter = input.value.toUpperCase();
    const table = document.getElementById("myTable");
    const tr = table.getElementsByTagName("tr");
  
    // Loop through all table rows, and hide those who don't match the search query
    console.log(tr.length);
    for (let i = 0; i < tr.length; i++) {
      const td = tr[i].getElementsByTagName("td")[0];
      if (td) {
        const txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
};
