
function hidePreloader() {
    const preloader = document.querySelector('.preloader');
    const loadedContent = document.querySelector('.loaded-content');
    const tbody = document.querySelector('#myTable tbody');

    if (tbody && tbody.rows.length > 0) {
        preloader.style.display = 'none';
        loadedContent.style.display = 'block';
    } else {
        setTimeout(hidePreloader, 500); 
    }
}

window.addEventListener('load', hidePreloader);


