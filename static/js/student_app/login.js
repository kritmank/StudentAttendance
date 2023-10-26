async function getUserProfile() {
	const profile = await liff.getProfile();
	document.getElementById("userID-form").value = profile.userId;

	while (true) {
		if (document.getElementById("userID-form").value != "") {
			console.log("submit");
			document.getElementById("form").submit();
			break;
		}
	}
}

async function main() {
	await liff.init({
		liffId: "LIFF_ID", // Use own liffId
		withLoginOnExternalBrowser: true,
	});
	if (liff.isLoggedIn()) {
		getUserProfile();
	} else {
		liff.login();
	}
}
main();
