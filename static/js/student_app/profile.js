async function getUserProfile() {
	const profile = await liff.getProfile();
	document.getElementById("pictureUrl").src = profile.pictureUrl;
	document.getElementById("displayName").innerHTML = profile.displayName;
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