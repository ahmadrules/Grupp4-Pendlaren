<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <title>PENDLAREN</title>
    <link rel="stylesheet" href="../static/styles.css">
    <link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
    <script type="text/javascript" src="../static/script.js" defer></script>
    <script src="../static/script.js" defer></script>

    <script type="text/javascript">
        function login() {
            window.open('http://accounts.spotify.com/authorize?client_id=e6740bb7feb04f329db3f1cf4ebffefe&redirect_uri=https://127.0.0.1:8000/callback&response_type=code&scope=playlist-modify-public playlist-modify-private');
        }

        async function getUserID() {
            console.log("Before userID: " + document.cookie);
            let url = "https://api.spotify.com/v1/me";

            let out1 = "";

            await fetch(url, {
                    method: 'GET',
                    headers: {
                        'Authorization': 'Bearer {{access_token}}'
                    }
                }
            ).then(response => response.json())
                .then(out => {document.cookie = "userID=" + out['id'] + "; path=/", out1 = out})
                .catch(err => console.log("Error " + err))
                .then(response => console.log("After userID: " + document.cookie));

            console.log(out1)

            await fillPlaylist();
        }


        async function searchForTracks(genre, tripDuration) {
            var q = 'q=remaster%2520genre%3A' + genre + '&type=track&market=SE&limit=50'
            var url = "https://api.spotify.com/v1/search?" + q

            var json = [];
            var uris = [];
            var duration_ms = 0;

            await fetch(url, {
                    method: 'GET',
                    headers: {
                        'Authorization': 'Bearer ' + `{{access_token}}`
                    }
                }
            ).then(response => response.json())
                .then(out => json = out['tracks']['items'])
                .catch(err => console.log("Error " + err));


            json.forEach((item, index) => {
                for (const [key, value] of Object.entries(item)) {
                    if (key === "uri") {
                        uris.push(value);
                    }

                    if (key === "duration_ms") {
                        duration_ms = duration_ms + value;
                        if (duration_ms >= tripDuration) {
                            break
                        }
                    }
                }
            });

            console.log(uris)
            return uris
        }

        async function createPlaylist() {
            var userID = document.cookie.split('=')[1];
            console.log("Playlist USER ID: " + userID);

            var url = "https://api.spotify.com/v1/users/" + userID + "/playlists"

            const date = new Date();
            const time = date.getDate()  + "/" + (date.getMonth() + 1) + " {{genre}}, {{fromStop}} - {{toStop}}";

            const myHeaders = new Headers();
            myHeaders.append("Authorization", "Bearer " + "{{access_token}}");
            myHeaders.append("Content-Type", "application/json");

            const json = {name: time, description: "Spellista för resa från {{fromStop}} till {{toStop}}"}
            const data = JSON.stringify(json);

            var playlist_id = "";
            var playlistURL = "";
            var images = [];
            var imageURL = "";

            await fetch(url, {
                    method: 'POST',
                    headers: myHeaders,
                    body: data
                }
            ).then(response => response.json())
                .then (function(json) {
                    console.log(" Create playlist JSON: " + json);
                    playlist_id = json['id'];
                    images = json['images'];
                    playlistURL = json['external_urls']['spotify'];
                });

            return playlist_id;
        }

        async function fillPlaylist() {
            const playlistID = await createPlaylist("Lund c", "Malmö C");
            const uris = await searchForTracks("{{genre}}", "{{total_seconds}}");
            const uriArray = uris.map(item => item)
            console.log("URIARRAY: " + uriArray);

            var url = "https://api.spotify.com/v1/playlists/" + playlistID + "/tracks"
            const myHeaders = new Headers();
            myHeaders.append("Authorization", "Bearer " + '{{access_token}}');
            myHeaders.append("Content-Type", "application/json");

            const json = {
                "uris": uriArray,
                "position": 0
            };

            await fetch(url, {
                method: 'POST',
                headers: myHeaders,
                body: JSON.stringify(json)
            }).then(response => response.json())
                .then(json => console.log(json));

            await getPlaylist(playlistID);


        }

        async function getPlaylist(playlistID) {
            var url = "https://api.spotify.com/v1/playlists/" + playlistID

            var imageURL = "";
            var playlistURL = "";

            await fetch(url, {
                method: 'GET',
                headers: { 'Authorization': 'Bearer ' + `{{access_token}}`},
            }).then(response => response.json())
                .then (function(json) {
                    console.log(json);
                    images = json['images'];
                    imageURL = images[0].url
                    playlistURL = json['external_urls']['spotify'];

                    console.log("Playlist ID: " + playlistID);
                    console.log("URL: " + playlistURL);
                    console.log("Image URL: " + images[0].url)

                });

            const playlistInfo = [];
            playlistInfo.push(playlistURL);
            playlistInfo.push(imageURL);

            setUrlAndImage(imageURL, playlistURL);
        }

        function setUrlAndImage(url, imageURL) {
            const image = document.getElementById("playlistImage")
            image.src = url;

            const playBtn = document.getElementById("playBtn")
            playBtn.setAttribute("href", imageURL)
        }

        getUserID();


        </script>
</head>
<body>
<header class="site-header">
    <h1 class="logo-title">PENDLAREN</h1>

</header>

<main class="site-main">
    <div class="main-layout">
        <section class="form-section">
            <form action="https://localhost:8000/search" method="POST" class="trip-form">
                <div class="form-group">
                    <label for="from">Från:</label>
                    <select class="js-example-basic-single" id="from" name="from">
                    </select>
                </div>

                <div class="form-group">
                    <label for="to">Till:</label>
                    <select class="js-example-basic-single" id="to" name="toStop">
                    </select>
                </div>
                <div class="form-group">
                    <label for="genre">Genre:</label>
                    <select class="js-example-basic-single" id="genre" name="genre">
                        <option value=""> Välj genre</option>
                        <option value="Pop">Pop</option>
                        <option value="Rock">Rock</option>
                        <option value="Rap">Rap</option>
                    </select>
                </div>
                <button type="submit" class="btn-search" id="searchBtn">SÖK</button>
            </form>
        </section>

        <section class="playlist-section">
            <div class="playlist-box">
                <img alt="Din spellista visas här" id="playlistImage">
            </div>

            <!-- Tillfällig länk -->
            <a class="btn-play-now" id="playBtn">
                SPELA NU
            </a>
        </section>

        <aside class="playlist-aside" aria-label="Byten längs rutten">
            <h2 class="aside-title">Reseinformation</h2>
            <div class="trip-info">
                <div class="trip-summary">
                    <p><strong>Från:</strong> {{ trip.fromStop }}</p>
                    <p><strong>Avgång:</strong> {{ trip.fromTime[:5] }}</p>
                    <p><strong>Till:</strong> {{ trip.toStop }}</p>
                    <p><strong>Ankomst:</strong> {{ trip.toTime[:5] }}</p>
                    <p><strong>Restid:</strong> {{ trip.totalTime }}</p>
                </div>

            <h3></br>Byten längs rutten</h3>
            {% if transfers and transfers | length > 0 %}
                <ul>
                    {% for t in transfers %}
                        </br><li>
                            <strong>{{ t.station }}</strong><br>
                                Ankomst: {{ t.arrival }}</br>
                            {% if not t.is_final_destination %}
                                Avgång: {{ t.departure }}</br>
                                </br>Bytestid: {{ t.wait_minutes }} minuter</br>
                            {% else %}
                                <em>Slutdestination</em>
                            {% endif %}
                        </li>
                    {% endfor %}
                </ul>
            {% else %}
                <p>Inga byten på denna resa.</p>
            {% endif %}

        </aside>
    </div>
</main>
</body>

<script>

</script>
</html>