function testSpotify() {
    const url =new URL(location.href)

    const obj = {
        "code" : url.searchParams.get("code")
    }
    console.log(obj)
    console.log("TESTING")
}

function getCookie() {
    document.getElementById("login").innerHTML = document.cookie;
    return document.cookie;
}
