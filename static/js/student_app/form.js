function findMyCoordinates() {
	return new Promise((resolve, reject) => {
		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(
				(position) => {
					const latitude = position.coords.latitude;
					const longitude = position.coords.longitude;
					resolve({ latitude, longitude });
				},
				(err) => {
					reject(err.message);
				}
			);
		} else {
			reject("Geolocation is not supported by this browser.");
		}
	});
}

async function check(form_id) {
	try {
		const { latitude, longitude } = await findMyCoordinates();
		console.log("Latitude:", latitude);
		console.log("Longitude:", longitude);
		document.getElementById("lat" + form_id).value = latitude;
		document.getElementById("long" + form_id).value = longitude;
		document.getElementById(form_id).submit();
	} catch (error) {
		alert(error);
	}
}

// document.getElementById("checkbtn").onclick = check;
