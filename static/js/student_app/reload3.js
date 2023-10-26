// Define the URL you want to redirect to
var redirectUrl = '/student/';

function reload() {
  window.location.href = redirectUrl;
}

function redirect(time) {
  window.setTimeout(reload, time*1000);
}