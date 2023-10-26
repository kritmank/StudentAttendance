async function getUserProfile() {
	const profile = await liff.getProfile();
	document.getElementById("pictureUrl").src = profile.pictureUrl;
	document.getElementById("userId").innerHTML =
		"<b>UserId:</b> " + profile.userId;
	document.getElementById("displayName").innerHTML =
		"<b>DisplayName:</b> " + profile.displayName;
	document.getElementById("statusMessage").innerHTML =
		"<b>StatusMessage:</b> " + profile.statusMessage;
	document.getElementById("decodeIDToken").innerHTML =
		"<b>decodeIDToken:</b> " + liff.getDecodedIDToken().email;
}

async function main() {
	await liff.init({
		liffId: "2000479875-DREaGV88",
		withLoginOnExternalBrowser: true,
	});
	if (liff.isLoggedIn()) {
		getUserProfile();
	} else {
		liff.login();
	}
}
main();
